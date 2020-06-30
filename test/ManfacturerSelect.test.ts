import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ManufacturerSelect from '../components/ManufacturerSelect.vue'
import Manufacturer from '~/models/Manufacturer'

Vue.use(Vuetify)

describe('ManufacturerSelect', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(ManufacturerSelect, {
      localVue,
      vuetify,
      propsData: {
        selectedManufacturers: [
          Manufacturer.createWithData(1, 'name1', 'uri1')
        ]
      },
      data () {
        return {
          manufacturers: [
            Manufacturer.createWithData(1, 'name1', 'uri1'),
            Manufacturer.createWithData(2, 'name2', 'uri2')
          ]
        }
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  it('should render one chip', () => {
    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(1)
  })

  /*
   * removing
   */

  it('should trigger an update event when a manufacturer is removed', () => {
    wrapper.vm.removeManufacturer(1)
    expect(wrapper.emitted('update:selectedManufacturers')).toBeTruthy()
  })

  it('should trigger an event with a manufacturer array with a length decreased by 1 when a manufacturer is removed', () => {
    wrapper.vm.removeManufacturer(1)
    expect(wrapper.emitted('update:selectedManufacturers')[0][0]).toHaveLength(0)
  })

  /*
   * adding
   */

  it('should trigger an update event when a manufacturer is added', () => {
    wrapper.vm.addManufacturer(2)
    expect(wrapper.emitted('update:selectedManufacturers')).toBeTruthy()
  })

  it('should trigger an event with a manufacturer array with a length increased by 1 when a manufacturer is added', () => {
    wrapper.vm.addManufacturer(2)
    expect(wrapper.emitted('update:selectedManufacturers')[0][0]).toHaveLength(2)
  })
})
