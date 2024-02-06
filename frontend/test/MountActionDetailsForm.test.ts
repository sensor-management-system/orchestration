/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

import Vue from 'vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'

import { DateTime } from 'luxon'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

Vue.use(Vuetify)

describe('MountActionDetailsForm', () => {
  let store: any
  let localVue: any
  let vuetify: any

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Vuex)
    vuetify = new Vuetify()
    const vocabulary = {
      namespaced: true,
      state: {
        epsgCodes: [],
        elevationData: []
      },
      mutations: {
      },
      actions: {
        loadElevationData: () => {},
        loadEpsgCodes: () => {}
      }
    }
    store = new Vuex.Store({
      modules: { vocabulary }
    })
  })

  const createWrapper = (propsData?: any) => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const contact1 = new Contact()
    contact1.id = '1'
    contact1.givenName = 'Max'
    contact1.familyName = 'Mustermann'
    contact1.email = 'max@mustermann.mail'

    const contact2 = new Contact()
    contact2.id = '2'
    contact2.givenName = 'Eva'
    contact2.familyName = 'Musterfrau'
    contact2.email = 'eva@musterfrau.mail'

    const mountAction = new PlatformMountAction(
      '1',
      platform1,
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      null,
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      contact1,
      null,
      'begin of mount',
      null
    )

    return mount(MountActionDetailsForm, {
      localVue,
      vuetify,
      store,
      propsData: {
        value: mountAction,
        readonly: false,
        withUnmount: false,
        withDates: false,
        contacts: [contact1, contact2],
        ...propsData
      },
      mocks: {
        $auth: {
          user: {
            email: 'max@mustermann.mail'
          }
        }
      }
    })
  }

  it('should display endContact and endDescription fields when an end date is given', () => {
    const wrapper: any = createWrapper({ withUnmount: true })
    expect(wrapper.findComponent('[data-role="select-end-contact"]').exists()).toBe(true)
    expect(wrapper.findComponent('[data-role="textarea-end-description"]').exists()).toBe(true)
  })

  it('should trigger an event when the value of offset-x changes', async () => {
    const wrapper: any = createWrapper()
    const newValue = 1
    const component = await wrapper.findComponent('[data-role="textfield-offset-x"]')
    await component.setValue(newValue)
    expect(wrapper.emitted('input')).toBeTruthy()
    expect(wrapper.emitted('input').length).toBe(1)
    const inputPayload = wrapper.emitted('input')[0]
    expect(inputPayload.length).toEqual(1)
    const inputPayloadContent = inputPayload[0]
    expect(inputPayloadContent.offsetX).toBeCloseTo(newValue)
  })

  it('should trigger an event when the value of offset-y changes', async () => {
    const wrapper: any = createWrapper()
    const newValue = 2
    const component = await wrapper.findComponent('[data-role="textfield-offset-y"]')
    await component.setValue(newValue)
    expect(wrapper.emitted('input')).toBeTruthy()
    expect(wrapper.emitted('input').length).toBe(1)
    const inputPayload = wrapper.emitted('input')[0]
    expect(inputPayload.length).toEqual(1)
    const inputPayloadContent = inputPayload[0]
    expect(inputPayloadContent.offsetY).toBeCloseTo(newValue)
  })

  it('should trigger an event when the value of offset-z changes', async () => {
    const wrapper: any = createWrapper()
    const newValue = 3
    const component = await wrapper.findComponent('[data-role="textfield-offset-z"]')
    await component.setValue(newValue)
    expect(wrapper.emitted('input')).toBeTruthy()
    expect(wrapper.emitted('input').length).toBe(1)
    const inputPayload = wrapper.emitted('input')[0]
    expect(inputPayload.length).toEqual(1)
    const inputPayloadContent = inputPayload[0]
    expect(inputPayloadContent.offsetZ).toBeCloseTo(newValue)
  })

  // I don't know how to test the autocomplete field. nothing works...

  // it('should trigger an event when the value of beginContact changes', async () => {
  //   const wrapper: any = createWrapper()
  //   const contacts = wrapper.props().contacts
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   const contact2 = new Contact()
  //   contact2.id = '2'
  //   contact2.givenName = 'Eva'
  //   contact2.familyName = 'Musterfrau'
  //   contact2.email = 'eva@musterfrau.mail'
  //   const newValue = contact2
  //   const component = await wrapper.find('[data-role="select-begin-contact"]')
  //   console.log(component)

  //   const input = component.find('input')
  //   console.log('input:', input)
  //   await input.setValue(newValue)
  //   await input.trigger('change')

  //   // console.log('component.data:', component.data)

  //   // component.setData({ value: newValue })
  //   // console.log(component.data)

  //   await component.trigger('change')
  //   // await component.trigger('input')
  //   // await wrapper.vm.add()

  //   await wrapper.vm.$nextTick()

  //   // expect(wrapper.vm.beginContact).toEqual(contact2)

  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(2)
  //   const addPayload = wrapper.emitted('add')[1]
  //   expect(addPayload.length).toEqual(1)
  //   console.log('addPayload:', addPayload)

  //   const addPayloadContent = addPayload[0]
  //   expect(addPayloadContent.beginContact).toEqual(newValue)
  // })

  // it('should trigger an add event when an input changes', () => {
  //   const wrapper: any = createWrapper({ withUnmount: true })
  //   const contacts = wrapper.props().contacts
  //   const contact1 = wrapper.vm.beginContact
  //   const contact2 = wrapper.props().contacts[1]

  //   let addPayload, addPayloadContent

  //   wrapper.findComponent('[data-role="textfield-offset-x"]').setValue('1')
  //   expect(wrapper.vm.offsetX).toBeCloseTo(1)
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.offsetX).toBe(1)

  //   wrapper.findComponent('[data-role="textfield-offset-y"]').setValue('2')
  //   expect(wrapper.vm.offsetY).toBeCloseTo(2)
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.offsetY).toBe(2)

  //   wrapper.findComponent('[data-role="textfield-offset-z"]').setValue('3')
  //   expect(wrapper.vm.offsetZ).toBeCloseTo(3)
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.offsetZ).toBe(3)
  //   console.log('before begin change const', contact1._email, contact2._email)
  //   console.log('before begin change array', contacts[0]._email, contacts[1]._email)
  //   console.log('before begin change vm', wrapper.vm.beginContact, wrapper.vm.endContact)

  //   wrapper.findComponent('[data-role="select-begin-contact"]').setValue(contact1)
  //   expect(wrapper.vm.beginContact).toEqual(contacts[0])
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.beginContact).toBe(contacts[0])

  //   wrapper.findComponent('[data-role="select-end-contact"]').setValue(contact2)
  //   expect(wrapper.vm.endContact).toEqual(contact2)
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   expect(addPayloadContent.endContact).toBe(wrapper.vm.endContact)

  //   // TODO: figure out why these tests dont work
  //   wrapper.find('[data-role="textarea-begin-description"]').setValue('begin description')
  //   expect(wrapper.vm.beginDescription).toBe('begin description')
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.beginDescription).toBe(wrapper.vm.beginDescription)

  //   wrapper.findComponent('[data-role="textarea-end-description"]').setValue('end description')
  //   expect(wrapper.vm.endDescription).toBe('end description')
  //   expect(wrapper.emitted('add')).toBeTruthy()
  //   expect(wrapper.emitted('add').length).toBe(1)
  //   expect(addPayload.length).toEqual(1)
  //   addPayload = wrapper.emitted('add')[0]
  //   expect(addPayload.length).toEqual(1)
  //   addPayloadContent = addPayload[0]
  //   // expect(addPayloadContent.endDescription).toBe(wrapper.vm.endDescription)
  // })
})
