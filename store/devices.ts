import { Device } from '@/models/Device'
import { Commit, Dispatch } from 'vuex'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

interface devicesState {
  devices: Device[],
  device: Device | null,
  deviceContacts:Contact[],
  deviceAttachments:Attachment[],
  deviceAttachment:Attachment|null,
  deviceGenericActions:GenericAction[],
  deviceSoftwareUpdateActions: SoftwareUpdateAction[],
  deviceMountActions:DeviceMountAction[],
  deviceUnmountActions:DeviceUnmountAction[],
  deviceCalibrationActions:DeviceCalibrationAction[]
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
  deviceGenericActions:[],
  deviceSoftwareUpdateActions:[],
  deviceMountActions:[],
  deviceUnmountActions:[],
  deviceCalibrationActions:[],
  pageNumber: 1,
  pageSize: 20,
  totalPages: 1,
}

const getters = {
  actions:(state:devicesState)=>{ //Todo actions sortieren, wobei ehrlich gesagt, eine extra route im Backend mit allen Actions (sortiert) besser wäre
    return [
      ...state.deviceGenericActions,
      ...state.deviceSoftwareUpdateActions,
      ...state.deviceMountActions,
      ...state.deviceUnmountActions,
      ...state.deviceCalibrationActions
    ]
  }
}

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
  async loadAllDeviceActions({dispatch}:{dispatch:Dispatch},id:number){
    await dispatch('loadDeviceGenericActions',id)
    await dispatch('loadDeviceSoftwareUpdateActions',id)
    await dispatch('loadDeviceMountActions',id)
    await dispatch('loadDeviceUnmountActions',id)
    await dispatch('loadDeviceCalibrationActions',id)
  },
  async loadDeviceGenericActions({commit}:{commit:Commit},id:number){
    const deviceGenericActions = await this.$api.devices.findRelatedGenericActions(id)
    commit('setDeviceGenericActions',deviceGenericActions)
  },
  async loadDeviceSoftwareUpdateActions({commit}:{commit:Commit},id:number){
    const deviceSoftwareUpdateActions = await this.$api.devices.findRelatedSoftwareUpdateActions(id)
    commit('setDeviceSoftwareUpdateActions',deviceSoftwareUpdateActions)
  },
  async loadDeviceMountActions({commit}:{commit:Commit},id:number){
    const deviceMountActions = await this.$api.devices.findRelatedMountActions(id)
    commit('setDeviceMountActions',deviceMountActions)
  },
  async loadDeviceUnmountActions({commit}:{commit:Commit},id:number){
    const deviceUnmountActions = await this.$api.devices.findRelatedUnmountActions(id)
    commit('setDeviceUnmountActions',deviceUnmountActions)
  },
  async loadDeviceCalibrationActions({commit}:{commit:Commit},id:number){
    const deviceCalibrationActions = await this.$api.devices.findRelatedCalibrationActions(id)
    commit('setDeviceCalibrationActions',deviceCalibrationActions)
  },
  async deleteDeviceAttachment({ commit }: { commit: Commit },attachmentId:number): Promise<void>{
    return this.$api.deviceAttachments.deleteById(attachmentId);
  },
  async addDeviceAttachment({ commit }: { commit: Commit },{deviceId,attachment}:{deviceId:number,attachment:Attachment}):Promise<void>{
    return this.$api.deviceAttachments.add(deviceId, attachment);
  },
  updateDeviceAttachment({ commit }: { commit: Commit },{deviceId,attachment}:{deviceId:number,attachment:Attachment}):Promise<void>{
    return this.$api.deviceAttachments.update(deviceId, attachment);
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
  },
  setDeviceGenericActions(state:devicesState,deviceGenericActions:GenericAction[]){
    state.deviceGenericActions=deviceGenericActions;
  },
  setDeviceSoftwareUpdateActions(state:devicesState,deviceSoftwareUpdateActions:SoftwareUpdateAction[]){
    state.deviceSoftwareUpdateActions=deviceSoftwareUpdateActions;
  },
  setDeviceMountActions(state:devicesState,deviceMountActions:DeviceMountAction[]){
    state.deviceMountActions=deviceMountActions;
  },
  setDeviceUnmountActions(state:devicesState,deviceUnmountActions:DeviceUnmountAction[]){
    state.deviceUnmountActions=deviceUnmountActions;
  },
  setDeviceCalibrationActions(state:devicesState,deviceCalibrationActions:DeviceCalibrationAction[]){
    state.deviceCalibrationActions=deviceCalibrationActions;
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
