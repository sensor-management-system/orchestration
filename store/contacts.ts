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

interface contactsState {
  contacts: Contact[],
  configurationContacts: Contact[],
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

export const state = {
  contacts: [],
  configurationContacts: [],
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}
export const getters = {
  searchContacts: (state: contactsState) => {
    return state.contacts.filter((c: Contact) => !state.configurationContacts.find((rc: Contact) => rc.id === c.id))
  }
}
export const actions = {
  async searchContactsPaginated ({
    commit,
    state
  }: { commit: Commit, state: contactsState }, searchtext: string = '') {
    // @ts-ignore
    const {elements,totalCount} = await this.$api.contacts.searchPaginated(state.pageNumber, state.pageSize, searchtext)
    commit('setContacts', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
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
  async addContactToConfiguration (_context: ActionContext<contactsState, contactsState>,
    {
      configurationId,
      contactId
    }: { configurationId: string, contactId: string }) {
    // @ts-ignore
    await this.$api.configurations.addContact(configurationId, contactId)
  },
  async removeContactFromConfiguration (_context: ActionContext<contactsState, contactsState>,
    {
      configurationId,
      contactId
    }: { configurationId: string, contactId: string }) {
    // @ts-ignore
    await this.$api.configurations.removeContact(configurationId, contactId)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  }
}
export const mutations = {
  setContacts (state: contactsState, contacts: Contact[]) {
    state.contacts = contacts
  },
  setConfigurationContacts (state: contactsState, contacts: Contact[]) {
    state.configurationContacts = contacts
  },
  setPageNumber (state: contactsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: contactsState, count: number) {
    state.totalPages = count
  }
}
