/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { shallowMount } from '@vue/test-utils'
// @ts-ignore
import AttachmentBasicDataForm from '@/components/shared/AttachmentBasicDataForm.vue'
import { Attachment } from '@/models/Attachment'
import { fetchAttachmentImage, URL_IMAGE_ERROR } from '@/utils/attachmentImage'

jest.mock('@/components/shared/AutocompleteTextInput.vue', () => ({ render: () => null }))
jest.mock('@/utils/attachmentImage', () => ({
  fetchAttachmentImage: jest.fn(),
  URL_IMAGE_ERROR: 'Please add the image as a file upload.'
}))

describe('edited image URL attachment validation', () => {
  const fetchAttachmentImageMock = fetchAttachmentImage as jest.MockedFunction<typeof fetchAttachmentImage>
  let wrapper: any
  let commit: jest.Mock

  beforeEach(() => {
    commit = jest.fn()
    fetchAttachmentImageMock.mockReset().mockResolvedValue('blob:checked')
    window.URL.revokeObjectURL = jest.fn()
    const attachment = new Attachment()
    attachment.url = 'https://example.org/image.PNG?download=1'
    wrapper = shallowMount(AttachmentBasicDataForm, {
      render: h => h('div'),
      propsData: { value: attachment, isUsedAsImage: true, originalUrl: 'https://example.org/original.png' },
      mocks: { $store: { commit } }
    })
    wrapper.vm.$refs.form = { validate: jest.fn().mockReturnValue(true) }
  })

  afterEach(() => wrapper.destroy())

  it('checks image URLs before saving and releases the temporary preview', async () => {
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).toHaveBeenCalledWith(wrapper.vm.value.url)
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:checked')
  })

  it('blocks saving and shows file-upload guidance on failure', async () => {
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    expect(await wrapper.vm.validateForm()).toBe(false)
    expect(wrapper.vm.imageUrlError).toBe(URL_IMAGE_ERROR)
    expect(commit).toHaveBeenCalledWith('snackbar/setError', URL_IMAGE_ERROR)
  })

  it('leaves ordinary document links unchanged', async () => {
    await wrapper.setProps({ isUsedAsImage: false })
    wrapper.vm.value.url = 'https://example.org/document.pdf'
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('accepts changed image links without fetching when not used as an image', async () => {
    await wrapper.setProps({ isUsedAsImage: false })
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('allows metadata edits without checking an unchanged image URL', async () => {
    await wrapper.setProps({ originalUrl: wrapper.vm.value.url })
    wrapper.vm.value.label = 'Updated label'
    fetchAttachmentImageMock.mockRejectedValue(new Error('CORS'))
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('checks changed preview URLs regardless of their filename extension', async () => {
    wrapper.vm.value.url = 'https://example.org/image'
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).toHaveBeenCalledWith('https://example.org/image')
  })

  it('does not fetch uploaded attachments', async () => {
    wrapper.vm.value.isUpload = true
    expect(await wrapper.vm.validateForm()).toBe(true)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('does not fetch when normal form validation fails', async () => {
    wrapper.vm.$refs.form.validate.mockReturnValue(false)
    expect(await wrapper.vm.validateForm()).toBe(false)
    expect(fetchAttachmentImage).not.toHaveBeenCalled()
  })

  it('blocks saving if the URL changes while the check is pending', async () => {
    const validation = wrapper.vm.validateForm()
    wrapper.vm.value.url = 'https://example.org/other.png'
    expect(await validation).toBe(false)
  })
})
