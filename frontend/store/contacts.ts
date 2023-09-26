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
import { Commit, GetterTree, ActionTree } from 'vuex/types'

import { RootState } from '@/store'
import { Contact } from '@/models/Contact'

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
  totalCount: number
}

const state = (): ContactsState => ({
  contacts: [],
  contact: null,
  configurationContacts: [],
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalPages: 1,
  totalCount: 0
})

export type SearchContactsGetter = Contact[]
export type ContactsByDifferenceGetter = (contactsToSubtract: Contact[]) => Contact[]
export type PageSizesGetter = number[]

const getters: GetterTree<ContactsState, RootState> = {
  searchContacts: (state: ContactsState): Contact[] => {
    return state.contacts.filter((c: Contact) => !state.configurationContacts.find((rc: Contact) => rc.id === c.id))
  },
  // TODO: Do we need it in the future? We allow multiple contact roles per contact & device.
  contactsByDifference: (state: ContactsState) => (contactsToSubtract: Contact[]): Contact[] => {
    return state.contacts.filter((contact) => {
      return !contactsToSubtract.find((contactToSubtract) => {
        return contactToSubtract.id === contact.id
      })
    })
  },
  pageSizes: (): number[] => {
    return PAGE_SIZES
  }
}

export type SearchContactsPaginatedAction = (searchText: string) => Promise<void>
export type LoadContactAction = (id: string) => Promise<void>
export type LoadAllContactsAction = () => Promise<void>
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type DeleteContactAction = (id: string) => Promise<void>
export type SaveContactAction = (contact: Contact) => Promise<Contact>

const actions: ActionTree<ContactsState, RootState> = {
  async searchContactsPaginated ({
    commit,
    state
  }: { commit: Commit, state: ContactsState }, searchtext: string = ''): Promise<void> {
    const { elements, totalCount } = await this.$api.contacts.searchPaginated(state.pageNumber, state.pageSize, searchtext)
    commit('setContacts', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
    commit('setTotalCount', totalCount)
  },
  async loadContact ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const contact = await this.$api.contacts.findById(id)
    commit('setContact', contact)
  },
  async loadAllContacts ({ commit }: { commit: Commit }): Promise<void> {
    const contacts = await this.$api.contacts.findAll()
    commit('setContacts', contacts)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number): void {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number): void {
    commit('setPageSize', newPageSize)
  },
  deleteContact (_context, id: string): Promise<void> {
    return this.$api.contacts.deleteById(id)
  },
  saveContact (_context, contact: Contact): Promise<Contact> {
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
  },
  setTotalCount (state: ContactsState, count: number) {
    state.totalCount = count
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
