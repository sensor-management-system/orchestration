import { Commit, ActionContext } from 'vuex/types'
import { Contact } from '@/models/Contact'

interface contactsState{
  allContacts: Contact[],
  configurationContacts: Contact[]
}

export const state = {
  allContacts: [],
  configurationContacts: []
}
export const getters = {
  searchContacts: (state:contactsState) => {
    return state.allContacts.filter((c:Contact) => !state.configurationContacts.find((rc:Contact) => rc.id === c.id))
  }
}
export const actions = {
  async loadAllContacts ({ commit }: { commit: Commit }) {
    // @ts-ignore
    const contacts = await this.$api.contacts.findAll()
    commit('setAllContacts', contacts)
  },
  async loadConfigurationContacts ({ commit }: { commit: Commit }, id:string) {
    // @ts-ignore
    const contacts = await this.$api.configurations.findRelatedContacts(id)
    commit('setConfigurationContacts', contacts)
  },
  async addContactToConfiguration (_context:ActionContext<contactsState, contactsState>,
    { configurationId, contactId }:{configurationId:string, contactId:string}) {
    // @ts-ignore
    await this.$api.configurations.addContact(configurationId, contactId)
  },
  async removeContactFromConfiguration (_context:ActionContext<contactsState, contactsState>,
    { configurationId, contactId }:{configurationId:string, contactId:string}) {
    // @ts-ignore
    await this.$api.configurations.removeContact(configurationId, contactId)
  }
}
export const mutations = {
  setAllContacts (state:contactsState, contacts:Contact[]) {
    state.allContacts = contacts
  },
  setConfigurationContacts (state:contactsState, contacts:Contact[]) {
    state.configurationContacts = contacts
  }
}
