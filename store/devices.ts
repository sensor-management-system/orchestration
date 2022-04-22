import { Device } from '@/models/Device'
import { Commit } from 'vuex'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'

interface devicesState {
  devices: Device[],
  device: Device | null,
  deviceContacts:Contact[],
  deviceAttachments:Attachment[],
  deviceAttachment:Attachment|null,
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  devices: [],
  device: null,
  deviceContacts:[],
  deviceAttachments:[],
  deviceAttachment:null,
  pageNumber: 1,
  pageSize: 20,
  totalPages: 1,
}

const getters = {}

const actions = {
  async searchDevicesPaginated ({ commit, state }: { commit: Commit, state: devicesState }, searchParams: IDeviceSearchParams) {

    let email = null;
    if (searchParams.onlyOwnDevices) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }

    // @ts-ignore
    const { elements, totalCount } = await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchPaginated(state.pageNumber, state.pageSize)
    commit('setDevices', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadDevice({ commit }: { commit: Commit },
    {deviceId,includeContacts,includeCustomFields,includeDeviceProperties,includeDeviceAttachments}:
      {deviceId:number,includeContacts:boolean,includeCustomFields:boolean,includeDeviceProperties:boolean,includeDeviceAttachments:boolean}){
    const device= await this.$api.devices.findById(deviceId, {
      includeContacts: includeContacts,
      includeCustomFields: includeCustomFields,
      includeDeviceProperties: includeDeviceProperties,
      includeDeviceAttachments: includeDeviceAttachments
    });
    commit('setDevice',device);
  },
  async loadDeviceContacts({commit}:{commit:Commit},id:number){
    const deviceContacts = await this.$api.devices.findRelatedContacts(id)
    commit('setDeviceContacts',deviceContacts)
  },
  async loadDeviceAttachments({ commit }: { commit: Commit },id:number){
    const deviceAttachments = await this.$api.devices.findRelatedDeviceAttachments(id)
    commit('setDeviceAttachments',deviceAttachments)
  },
  async loadDeviceAttachment({ commit }: { commit: Commit },id:number){
    const deviceAttachment = await this.$api.deviceAttachments.findById(id)
    commit('setDeviceAttachment',deviceAttachment)
  },
  async deleteDeviceAttachment({ commit }: { commit: Commit },attachmentId:number): Promise<void>{
    return this.$api.deviceAttachments.deleteById(attachmentId);
  },
  async addDeviceContact({ commit }: { commit: Commit },{deviceId,contactId}:{deviceId:number,contactId:number}):Promise<void>{
    return this.$api.devices.addContact(deviceId,contactId)
  },
  async removeDeviceContact({ commit }: { commit: Commit },{deviceId,contactId}:{deviceId:number,contactId:number}):Promise<void>{
    return this.$api.devices.removeContact(deviceId, contactId);
  },
  async saveDevice({commit}:{commit:Commit},device:Device):Promise<Device>{
    return this.$api.devices.save(device)
  },
  async deleteDevice({ commit }: { commit: Commit }, id: number){
    await this.$api.devices.deleteById(id)
  },
  async exportAsCsv({ commit}: { commit: Commit}, searchParams: IDeviceSearchParams):Promise<Blob>{
    let email = null;
    if (searchParams.onlyOwnDevices) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }
    //@ts-ignore
    return await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchMatchingAsCsvBlob()
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  }
}

const mutations = {
  setDevices (state: devicesState, devices: Device[]) {
    state.devices = devices
  },
  setDevice (state: devicesState, device: Device) {
    state.device = device
  },
  setPageNumber (state: devicesState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: devicesState, count: number) {
    state.totalPages = count
  },
  setDeviceContacts(state:devicesState,contacts:Contact[]){
    state.deviceContacts=contacts
  },
  setDeviceAttachments(state:devicesState,attachments:Attachment[]){
    state.deviceAttachments=attachments
  },
  setDeviceAttachment(state:devicesState,attachment:Attachment){
    state.deviceAttachment=attachment
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
