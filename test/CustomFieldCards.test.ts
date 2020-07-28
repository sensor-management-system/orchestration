import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import CustomFieldCards from '@/components/CustomFieldCards.vue'
import { CustomTextField } from '@/models/CustomTextField'

Vue.use(Vuetify)

describe('CustomFieldCards', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()
    // disable "[Vuetify] Unable to locate target [data-app]" warnings:
    document.body.setAttribute('data-app', 'true')

    wrapper = mount(CustomFieldCards, {
      localVue,
      vuetify,
      propsData: {
        value: [
          CustomTextField.createFromObject({
            key: 'foo',
            value: 'bar'
          })
        ] as CustomTextField[]
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
   * adding
   */

  it('should trigger an input event when add button is clicked', async () => {
    await wrapper.get('[data-role="add-field"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a fields array length increased by 1 when the add button is clicked', async () => {
    await wrapper.get('[data-role="add-field"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })

  /*
   * removing
   */

  it('should trigger an input event when delete button is clicked', async () => {
    await wrapper.get('[data-role="delete-field"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a fields array length decreased by 1 when the delete buttom is clicked', async () => {
    await wrapper.get('[data-role="delete-field"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(0)
  })
})
