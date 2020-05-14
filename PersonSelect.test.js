import Vue from 'vue'
import Vuetify from 'vuetify'

import { shallowMount, createLocalVue } from '@vue/test-utils'

import PersonSelect from '@/components/PersonSelect.vue'
import Person from '@/models/Person'

Vue.use(Vuetify)
const localVue = createLocalVue()

const createComponent = () => {
  const vuetify = new Vuetify()
  return shallowMount(PersonSelect, {
    localVue,
    vuetify,
    propsData: {
      selectedPersons: [Person.createWithIdAndName(1, 'Foo'), Person.createWithIdAndName(2, 'Bar')]
    }
  })
}

describe('PersonSelect', () => {

  it('should be a Vue instance', () => {
    const component = createComponent()
    expect(component.isVueInstance()).toBeTruthy()
  })
})
