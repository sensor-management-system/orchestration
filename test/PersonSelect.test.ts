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

  it('should render one chip', () => {
    expect(wrapper.findAll({ name: 'v-chip' })).toHaveLength(1)
  })

  /*
   * removing
   */

  it('should trigger an update event when a person is removed', () => {
    wrapper.vm.removePerson(1)
    expect(wrapper.emitted('update:selectedPersons')).toBeTruthy()
  })

  it('should trigger an event with a persons array with a length decreased by 1 when a person is removed', async () => {
    wrapper.vm.removePerson(1)
    expect(wrapper.emitted('update:selectedPersons')[0][0]).toHaveLength(0)
  })

  /*
   * adding
   */

  it('should trigger an update event when a person is added', () => {
    wrapper.vm.addPerson(2)
    expect(wrapper.emitted('update:selectedPersons')).toBeTruthy()
  })

  it('should trigger an event with a persons array with a length increased by 1 when a person is added', () => {
    wrapper.vm.addPerson(2)
    expect(wrapper.emitted('update:selectedPersons')[0][0]).toHaveLength(2)
  })

})
