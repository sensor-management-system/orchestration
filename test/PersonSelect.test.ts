import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import PersonSelect from '../components/PersonSelect.vue'
import Person from '@/models/Person'

Vue.use(Vuetify)

describe('PersonSelect', () => {
  let wrapper: any

  /*
   * setup
   */

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

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  it('should have a property localSelectedPersons with length 1', () => {
    expect(wrapper.vm.$data.localSelectedPersons).toHaveLength(1)
  })

  it('should render one chip', () => {
    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(1)
  })

  /*
   * removing
   */

  it('should have a property localSelectedPersons with a length decreased by 1 when a person is removed', () => {
    const oldLength = wrapper.vm.$data.localSelectedPersons.length
    wrapper.vm.removePerson(1)
    expect(wrapper.vm.$data.localSelectedPersons).toHaveLength(oldLength - 1)
  })

  it('should trigger an update event when a person is removed', () => {
    wrapper.vm.removePerson(1)
    expect(wrapper.emitted('update:selectedPersons')).toBeTruthy()
  })

  it('should remove a chip when a person is removed', async () => {
    const chipsNum = wrapper.findAll({ name: 'v-chip' }).length
    const chip = wrapper.find({ name: 'v-chip' })
    await chip.find('button').trigger('click')

    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(chipsNum - 1)
  })

  /*
   * adding
   */

  it('should have a property localSelectedPersons with a length increased by 1 when a person is added', () => {
    const oldLength = wrapper.vm.$data.localSelectedPersons.length
    wrapper.vm.addPerson(2)
    expect(wrapper.vm.$data.localSelectedPersons).toHaveLength(oldLength + 1)
  })

  it('should trigger an update event when a person is added', () => {
    wrapper.vm.addPerson(2)
    expect(wrapper.emitted('update:selectedPersons')).toBeTruthy()
  })

  /*
   * TODO: howto trigger an input event on a v-autocomplete?
   *
  it('should fire an update:selectedPersons event ', async () => {
    const autocomplete = wrapper.find('.v-autocomplete')
    autocomplete.setProps({ value: 'Person 2' })
    await autocomplete.trigger('keydown.down')
    await autocomplete.trigger('keydown.enter')

    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(2)
  })
  */
})
