/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
import { Commit, ActionContext } from 'vuex/types'
import { Contact } from '@/models/Contact'
import { Api } from '@/services/Api'

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface ContactsState {
  contacts: Contact[],
  contact: Contact | null,
  configurationContacts: Contact[],
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = () => ({
  contacts: [],
  contact: null,
  configurationContacts: [],
  totalPages: 1,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0]
})

const getters = {
  searchContacts: (state: ContactsState) => {
    return state.contacts.filter((c: Contact) => !state.configurationContacts.find((rc: Contact) => rc.id === c.id))
  },
  // TODO: Do we need it in the future? We allow multiple contact roles per contact & device.
  contactsByDifference: (state: ContactsState) => (contactsToSubtract: Contact[]) => {
    return state.contacts.filter((contact) => {
      return !contactsToSubtract.find((contactToSubtract) => {
        return contactToSubtract.id === contact.id
      })
    })
  },
  pageSizes: () => {
    return PAGE_SIZES
  }
}

// @ts-ignore
const actions: {
  [key: string]: any;
  $api: Api
} = {
  async searchContactsPaginated ({
    commit,
    state
  }: { commit: Commit, state: ContactsState }, searchtext: string = '') {
    // @ts-ignore
    const { elements, totalCount } = await this.$api.contacts.searchPaginated(state.pageNumber, state.pageSize, searchtext)
    commit('setContacts', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadContact ({ commit }: { commit: Commit }, id: string) {
    // @ts-ignore
    const contact = await this.$api.contacts.findById(id)
    commit('setContact', contact)
  },
  async loadAllContacts ({ commit }: { commit: Commit }) {
    // @ts-ignore
    const contacts = await this.$api.contacts.findAll()
    commit('setContacts', contacts)
  },
  async loadConfigurationContacts ({ commit }: { commit: Commit }, id: string) {
    // @ts-ignore
    const contacts = await this.$api.configurations.findRelatedContacts(id)
    commit('setConfigurationContacts', contacts)
  },
  async addContactToConfiguration (_context: ActionContext<ContactsState, ContactsState>,
    {
      configurationId,
      contactId
    }: { configurationId: string, contactId: string }) {
    // @ts-ignore
    await this.$api.configurations.addContact(configurationId, contactId)
  },
  async removeContactFromConfiguration (_context: ActionContext<ContactsState, ContactsState>,
    {
      configurationId,
      contactId
    }: { configurationId: string, contactId: string }) {
    // @ts-ignore
    await this.$api.configurations.removeContact(configurationId, contactId)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  async deleteContact ({ _commit }: { _commit: Commit }, id: string) {
    // @ts-ignore
    await this.$api.contacts.deleteById(id)
  },
  saveContact ({ _commit }: { _commit: Commit }, contact: Contact): Promise<Contact> {
    // @ts-ignore
    return this.$api.contacts.save(contact)
  }
}

const mutations = {
  setContacts (state: ContactsState, contacts: Contact[]) {
    state.contacts = contacts
  },
  setContact (state: ContactsState, contact: Contact) {
    state.contact = contact
  },
  setConfigurationContacts (state: ContactsState, contacts: Contact[]) {
    state.configurationContacts = contacts
  },
  setPageNumber (state: ContactsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setPageSize (state: ContactsState, newPageSize: number) {
    state.pageSize = newPageSize
  },
  setTotalPages (state: ContactsState, count: number) {
    state.totalPages = count
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
