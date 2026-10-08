/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { shallowMount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
// @ts-ignore
import AttachmentImagesForm from '@/components/shared/AttachmentImagesForm.vue'
// @ts-ignore
import AttachmentImagesCarousel from '@/components/shared/AttachmentImagesCarousel.vue'
import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'
import { fetchAttachmentImage, URL_IMAGE_ERROR } from '@/utils/attachmentImage'

jest.mock('@/utils/attachmentImage', () => ({
  fetchAttachmentImage: jest.fn(),
  URL_IMAGE_ERROR: 'This image could not be loaded from its URL. Please add it as a file upload instead.'
}))

Vue.use(Vuetify)

function attachment (id: string, isUpload: boolean): Attachment {
  const result = new Attachment()
  result.id = id
  result.url = `https://example.org/${id}.png`
  result.isUpload = isUpload
  return result
}

function image (attachment: Attachment): Image {
  const result = new Image()
  result.attachment = attachment
  return result
}

describe('attachment preview images', () => {
  const fetchAttachmentImageMock = fetchAttachmentImage as jest.MockedFunction<typeof fetchAttachmentImage>
  const upload = attachment('upload', true)
  const external = attachment('external', false)
  const downloadAttachment = jest.fn().mockResolvedValue(new Blob())
  const commit = jest.fn()

  beforeEach(() => {
    downloadAttachment.mockReset().mockResolvedValue(new Blob())
    commit.mockClear()
    fetchAttachmentImageMock.mockReset().mockResolvedValue('blob:external')
    window.URL.createObjectURL = jest.fn().mockReturnValue('blob:preview')
    window.URL.revokeObjectURL = jest.fn()
  })

  it('offers and directly fetches URL images while retaining uploads', async () => {
    const wrapper = shallowMount(AttachmentImagesForm, {
      propsData: {
        attachments: [upload, external],
        value: [],
        downloadAttachment
      },
      mocks: { $store: { commit } }
    })
    const vm = wrapper.vm as any
    expect(vm.renderableAttachments).toEqual([upload, external])
    await vm.addUrlForAttachment(external)
    expect(downloadAttachment).not.toHaveBeenCalled()
    expect(fetchAttachmentImage).toHaveBeenCalledWith(external.url)
    expect(vm.getUrlForAttachment(external)).toBe('blob:external')
    await vm.addUrlForAttachment(upload)
    expect(downloadAttachment).toHaveBeenCalledWith(upload.url)
    expect(vm.getUrlForAttachment(upload)).toBe('blob:preview')
    wrapper.destroy()
  })

  it('displays URL images and uploaded images in the carousel', async () => {
    const wrapper = shallowMount(AttachmentImagesCarousel, {
      propsData: { value: [image(external), image(upload)], downloadAttachment },
      mocks: { $store: { commit } }
    })
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()
    const vm = wrapper.vm as any
    expect(vm.images).toEqual([image(external), image(upload)])
    expect(vm.visibleImage.attachment).toEqual(external)
    expect(downloadAttachment).toHaveBeenCalledTimes(1)
    expect(downloadAttachment).toHaveBeenCalledWith(upload.url)
    expect(vm.getUrlForAttachment(external)).toBe('blob:external')
    wrapper.destroy()
  })

  it('asks for a file upload when a URL fails in the editable form', async () => {
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    const wrapper = shallowMount(AttachmentImagesForm, {
      propsData: { value: [image(external), image(upload)], attachments: [external, upload], downloadAttachment },
      mocks: { $store: { commit } }
    })
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()
    expect(commit).toHaveBeenCalledWith('snackbar/setError', URL_IMAGE_ERROR)
    expect((wrapper.vm as any).hasAttachmentError(external)).toBe(true)
    expect(downloadAttachment).toHaveBeenCalledWith(upload.url)
    wrapper.destroy()
  })

  it.each([false, true])('silently marks unavailable images in the read-only carousel (upload: %s)', async (isUpload) => {
    const failedAttachment = isUpload ? upload : external
    if (isUpload) {
      downloadAttachment.mockRejectedValue(new Error('Download failed'))
    } else {
      fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    }
    const wrapper = shallowMount(AttachmentImagesCarousel, {
      propsData: { value: [image(failedAttachment)], downloadAttachment },
      mocks: { $store: { commit } }
    })
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()
    const vm = wrapper.vm as any
    expect(vm.hasAttachmentError(failedAttachment)).toBe(true)
    expect(vm.getUrlForAttachment(failedAttachment)).toBe('')
    expect(commit).not.toHaveBeenCalled()
    vm.setAttachmentError(failedAttachment)
    expect(commit).not.toHaveBeenCalled()
    wrapper.destroy()
  })
})
