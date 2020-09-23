import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import CustomFieldForm from '@/components/CustomFieldForm.vue'
import { CustomTextField } from '@/models/CustomTextField'

Vue.use(Vuetify)

describe('CustomFieldForm', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(CustomFieldForm, {
      localVue,
      vuetify,
      propsData: {
        value: CustomTextField.createFromObject({
          id: '2',
          key: 'foo',
          value: 'bar'
        })
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.vm).toBeTruthy()
  })

  it('should trigger an input event on change', () => {
    wrapper.get('input[type="text"]').setValue('baz')
    expect(wrapper.emitted('input')).toBeTruthy()
  })
})
