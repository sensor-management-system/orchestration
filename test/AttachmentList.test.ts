import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import AttachmentList from '@/components/AttachmentList.vue'
import { Attachment } from '@/models/Attachment'

Vue.use(Vuetify)

describe('AttachmentList', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()
    // disable "[Vuetify] Unable to locate target [data-app]" warnings:
    document.body.setAttribute('data-app', 'true')

    wrapper = mount(AttachmentList, {
      localVue,
      vuetify,
      propsData: {
        value: [
          Attachment.createFromObject({
            id: '1',
            url: 'https://foo.pdf',
            label: 'Manual'
          }),
          Attachment.createFromObject({
            id: '2',
            url: 'https://bar.png',
            label: 'Product Image'
          })
        ] as Attachment[]
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.vm).toBeTruthy()
  })

  /*
   * add by URL
   */

  it('should trigger an input event when add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('https://foo.bar/document.docx')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('must not trigger an input event when the url is empty and the add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeFalsy()
  })

  it('should trigger an input event with a attachment array length increased by 1 when the add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('https://foo.bar/document.docx')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(3)
  })

  /*
   * removing
   */

  it('should trigger an input event when delete button is clicked', async () => {
    await wrapper.get('[data-role="delete-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a fields array length decreased by 1 when the delete buttom is clicked', async () => {
    await wrapper.get('[data-role="delete-attachment"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(1)
  })
})
