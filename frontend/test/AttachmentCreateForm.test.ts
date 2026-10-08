/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { shallowMount } from '@vue/test-utils'
// @ts-ignore
import AttachmentCreateForm from '@/components/shared/AttachmentCreateForm.vue'
import { Attachment } from '@/models/Attachment'
import { fetchAttachmentImage, URL_IMAGE_ERROR } from '@/utils/attachmentImage'

jest.mock('@/components/shared/AutocompleteTextInput.vue', () => ({ render: () => null }))
jest.mock('@/utils/attachmentImage', () => ({
  fetchAttachmentImage: jest.fn(),
  URL_IMAGE_ERROR: 'Please add the image as a file upload.'
}))

describe('image URL attachment creation validation', () => {
  const fetchAttachmentImageMock = fetchAttachmentImage as jest.MockedFunction<typeof fetchAttachmentImage>
  let wrapper: any
  let commit: jest.Mock

  beforeEach(() => {
    commit = jest.fn()
    fetchAttachmentImageMock.mockReset().mockResolvedValue('blob:checked')
    window.URL.revokeObjectURL = jest.fn()
    const attachment = new Attachment()
    attachment.url = 'https://example.org/image.PNG?download=1'
    wrapper = shallowMount(AttachmentCreateForm, {
      render: h => h('div'),
      propsData: {
        value: { attachmentType: 'url', attachment, file: null, imageWillBeCreated: false }
      },
      mocks: { $store: { commit } }
    })
    wrapper.vm.$refs.form = { validate: jest.fn().mockReturnValue(true) }
  })

  afterEach(() => wrapper.destroy())

  it('accepts image links without fetching when not selected for basic-tab preview', async () => {
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('checks URLs selected for basic-tab preview', async () => {
    wrapper.vm.value.imageWillBeCreated = true
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).toHaveBeenCalledWith('https://example.org/image.PNG?download=1')
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:checked')
  })

  it('blocks saving and shows upload guidance when the image cannot be fetched', async () => {
    wrapper.vm.value.imageWillBeCreated = true
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    expect(await wrapper.vm.validateForm()).toBe(false)
    expect(wrapper.vm.imageUrlError).toBe(URL_IMAGE_ERROR)
    expect(commit).toHaveBeenCalledWith('snackbar/setError', URL_IMAGE_ERROR)
  })

  it('keeps ordinary document links unchanged', async () => {
    wrapper.vm.value.attachment.url = 'https://example.org/document.pdf'
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('checks extensionless URLs selected for image preview', async () => {
    wrapper.vm.value.attachment.url = 'https://example.org/image'
    wrapper.vm.value.imageWillBeCreated = true
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).toHaveBeenCalled()
  })

  it('does not fetch file uploads', async () => {
    wrapper.vm.value.attachmentType = 'file'
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('does not fetch if normal form validation fails', async () => {
    wrapper.vm.$refs.form.validate.mockReturnValue(false)
    expect(await wrapper.vm.validateForm()).toBe(false)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })
})
