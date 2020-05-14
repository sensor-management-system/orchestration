import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import PersonSelect from '../components/PersonSelect.vue'
import Person from '@/models/Person'

Vue.use(Vuetify)

describe('PersonSelect', () => {
  let wrapper: any

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(PersonSelect, {
      localVue,
      vuetify,
      propsData: {
        selectedPersons: [Person.createWithIdAndName(1, 'Person 1')]
      },
      data () {
        return {
          persons: [Person.createWithIdAndName(1, 'Person 1'), Person.createWithIdAndName(2, 'Person 2')]
        }
      }
    })
  })

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  it('should render one chip', () => {
    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(1)
  })

  it('should remove one chip', async () => {
    const chip = wrapper.find({ name: 'v-chip' })
    chip.find('button').trigger('click')
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(0)
  })

  /*
  it('should add a second chip', async () => {
    const autocomplete = wrapper.find('.v-autocomplete')
    const input = autocomplete.find('input[type="text"]')
    input.setValue('Person 2')
    input.trigger('input')
    await wrapper.vm.$nextTick()
    autocomplete.trigger('keydown.enter')
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(2)
  })
  */
})
