import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ContactSelect from '../components/ContactSelect.vue'
import Concact from '~/models/Contact'

Vue.use(Vuetify)

describe('ContactSelect', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(ContactSelect, {
      localVue,
      vuetify,
      propsData: {
        selectedPersons: [Concact.createWithIdEMailAndNames(1, 'p1@mail.org', 'Person 1', 'Per', 'son 1')]
      },
      data () {
        return {
          persons: [
            Concact.createWithIdEMailAndNames(1, 'p1@mail.org', 'Person 1', 'Per', 'son 1'),
            Concact.createWithIdEMailAndNames(2, 'p2@mail.org', 'Person 2', 'Pers', 'On 2')]
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

  it('should trigger an update event when a contact is removed', () => {
    wrapper.vm.removeConcact(1)
    expect(wrapper.emitted('update:selectedContacts')).toBeTruthy()
  })

  it('should trigger an event with a contact array with a length decreased by 1 when a contact is removed', () => {
    wrapper.vm.removeContact(1)
    expect(wrapper.emitted('update:selectedContacts')[0][0]).toHaveLength(0)
  })

  /*
   * adding
   */

  it('should trigger an update event when a contact is added', () => {
    wrapper.vm.addContact(2)
    expect(wrapper.emitted('update:selectedContacts')).toBeTruthy()
  })

  it('should trigger an event with a contact array with a length increased by 1 when a contact is added', () => {
    wrapper.vm.addContact(2)
    expect(wrapper.emitted('update:selectedContacts')[0][0]).toHaveLength(2)
  })
})
