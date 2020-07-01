import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import AttachmentListItem from '@/components/AttachmentListItem.vue'
import { Attachment } from '@/models/Attachment'

Vue.use(Vuetify)

describe('AttachmentListItem', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(AttachmentListItem, {
      localVue,
      vuetify,
      propsData: {
        value: Attachment.createFromObject({
          id: 1,
          url: 'https://foo.bar/Document.docx',
          label: 'Assembling Instructions'
        })
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  it('should trigger an input event on change', () => {
    wrapper.get('input[type="text"]').setValue('Disassembling Instructions')
    expect(wrapper.emitted('input')).toBeTruthy()
  })
})
