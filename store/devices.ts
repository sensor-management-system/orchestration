import { Device } from '@/models/Device'
import { Commit, Dispatch } from 'vuex'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { IActionType } from '@/models/ActionType'
import { DeviceProperty } from '@/models/DeviceProperty'
import { CustomTextField } from '@/models/CustomTextField'
import CustomFieldCard from '@/components/CustomFieldCard.vue'
import { Platform } from '@/models/Platform'

const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType =
  typeof KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  | typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  | typeof KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
  | typeof KIND_OF_ACTION_TYPE_UNKNOWN

type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

interface devicesState {
  devices: Device[],
  device: Device | null,
  deviceContacts: Contact[],
  deviceAttachments: Attachment[],
  deviceAttachment: Attachment | null,
  deviceMeasuredQuantities: DeviceProperty[],
  deviceMeasuredQuantity: DeviceProperty|null,
  deviceGenericActions: GenericAction[],
  deviceSoftwareUpdateActions: SoftwareUpdateAction[],
  deviceCalibrationActions: DeviceCalibrationAction[],
  deviceGenericAction: GenericAction | null,
  deviceSoftwareUpdateAction: SoftwareUpdateAction | null,
  deviceCalibrationAction: DeviceCalibrationAction | null,
  deviceMountActions: DeviceMountAction[],
  deviceUnmountActions: DeviceUnmountAction[],
  chosenKindOfDeviceAction: IOptionsForActionType | null,
  deviceCustomFields:CustomTextField[],
  deviceCustomField:CustomTextField|null
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  devices: [],
  device: null,
  deviceContacts: [],
  deviceAttachments: [],
  deviceAttachment: null,
  deviceMeasuredQuantities: [],
  deviceMeasuredQuantity:null,
  deviceGenericActions: [],
  deviceSoftwareUpdateActions: [],
  deviceGenericAction: null,
  deviceSoftwareUpdateAction: null,
  deviceCalibrationAction: null,
  deviceCalibrationActions: [],
  deviceMountActions: [],
  deviceUnmountActions: [],
  chosenKindOfDeviceAction: null,
  deviceCustomFields:[],
  deviceCustomField:null,
  pageNumber: 1,
  pageSize: 20,
  totalPages: 1,
}

const getters = {
  actions: (state: devicesState) => { //Todo actions sortieren, wobei ehrlich gesagt, eine extra route im Backend mit allen Actions (sortiert) besser wäre
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
  async searchDevicesPaginated ({
    commit,
    state
  }: { commit: Commit, state: devicesState }, searchParams: IDeviceSearchParams) {

    let email = null
    if (searchParams.onlyOwnDevices) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }

    // @ts-ignore
    const {
      elements,
      totalCount
    } = await this.$api.devices
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
  async searchDevices ({
    commit,
    state
  }: { commit: Commit, state: devicesState }, searchParams: IDeviceSearchParams) {

    // @ts-ignore
    const devices = await this.$api.devices
      .setSearchText(searchParams.searchText)
      .searchAll()
    commit('setDevices', devices)
  },
  async loadDevice ({ commit }: { commit: Commit },
    {
      deviceId,
      includeContacts,
      includeCustomFields,
      includeDeviceProperties,
      includeDeviceAttachments
    }:
      { deviceId: number, includeContacts: boolean, includeCustomFields: boolean, includeDeviceProperties: boolean, includeDeviceAttachments: boolean }) {
    const device = await this.$api.devices.findById(deviceId, {
      includeContacts: includeContacts,
      includeCustomFields: includeCustomFields,
      includeDeviceProperties: includeDeviceProperties,
      includeDeviceAttachments: includeDeviceAttachments
    })
    commit('setDevice', device)
  },
  async loadDeviceContacts ({ commit }: { commit: Commit }, id: number) {
    const deviceContacts = await this.$api.devices.findRelatedContacts(id)
    commit('setDeviceContacts', deviceContacts)
  },
  async loadDeviceAttachments ({ commit }: { commit: Commit }, id: number) {
    const deviceAttachments = await this.$api.devices.findRelatedDeviceAttachments(id)
    commit('setDeviceAttachments', deviceAttachments)
  },
  async loadDeviceAttachment ({ commit }: { commit: Commit }, id: number) {
    const deviceAttachment = await this.$api.deviceAttachments.findById(id)
    commit('setDeviceAttachment', deviceAttachment)
  },
  async loadDeviceMeasuredQuantities ({ commit }: { commit: Commit }, id: number) {
    const deviceMeasuredQuantities = await this.$api.devices.findRelatedDeviceProperties(id)
    commit('setDeviceMeasuredQuantities', deviceMeasuredQuantities)
  },
  async loadDeviceMeasuredQuantity ({ commit }: { commit: Commit }, id: number) { // Todo
    const deviceMeasuredQuantity = await this.$api.deviceProperties.findById(id)
    commit('setDeviceMeasuredQuantity', deviceMeasuredQuantity)
  },
  async loadAllDeviceActions ({ dispatch }: { dispatch: Dispatch }, id: number) {
    await dispatch('loadDeviceGenericActions', id)
    await dispatch('loadDeviceSoftwareUpdateActions', id)
    await dispatch('loadDeviceMountActions', id)
    await dispatch('loadDeviceUnmountActions', id)
    await dispatch('loadDeviceCalibrationActions', id)
  },
  async loadDeviceGenericActions ({ commit }: { commit: Commit }, id: number) {
    const deviceGenericActions = await this.$api.devices.findRelatedGenericActions(id)
    commit('setDeviceGenericActions', deviceGenericActions)
  },
  async loadDeviceGenericAction ({ commit }: { commit: Commit }, actionId: number) {
    const deviceGenericAction = await this.$api.genericDeviceActions.findById(actionId)
    commit('setDeviceGenericAction', deviceGenericAction)
  },
  async loadDeviceSoftwareUpdateActions ({ commit }: { commit: Commit }, id: number) {
    const deviceSoftwareUpdateActions = await this.$api.devices.findRelatedSoftwareUpdateActions(id)
    commit('setDeviceSoftwareUpdateActions', deviceSoftwareUpdateActions)
  },
  async loadDeviceSoftwareUpdateAction ({ commit }: { commit: Commit }, actionId: number) {
    const deviceSoftwareUpdateAction = await this.$api.deviceSoftwareUpdateActions.findById(actionId)
    commit('setDeviceSoftwareUpdateAction', deviceSoftwareUpdateAction)
  },
  async loadDeviceCalibrationActions ({ commit }: { commit: Commit }, id: number) {
    const deviceCalibrationActions = await this.$api.devices.findRelatedCalibrationActions(id)
    commit('setDeviceCalibrationActions', deviceCalibrationActions)
  },
  async loadDeviceCalibrationAction ({ commit }: { commit: Commit }, actionId: number) {
    const deviceCalibrationAction = await this.$api.deviceCalibrationActions.findById(actionId)
    commit('setDeviceCalibrationAction', deviceCalibrationAction)
  },
  async loadDeviceMountActions ({ commit }: { commit: Commit }, id: number) {
    const deviceMountActions = await this.$api.devices.findRelatedMountActions(id)
    commit('setDeviceMountActions', deviceMountActions)
  },
  async loadDeviceUnmountActions ({ commit }: { commit: Commit }, id: number) {
    const deviceUnmountActions = await this.$api.devices.findRelatedUnmountActions(id)
    commit('setDeviceUnmountActions', deviceUnmountActions)
  },
  async loadDeviceCustomFields({commit}:{commit:Commit},id:number){
    const deviceCustomFields = await this.$api.devices.findRelatedCustomFields(id)
    commit('setDeviceCustomFields',deviceCustomFields);
  },
  async loadDeviceCustomField({commit}:{commit:Commit},id:number){
    const deviceCustomField = await this.$api.customfields.findById(id)
    commit('setDeviceCustomField',deviceCustomField)
  },
  async addDeviceSoftwareUpdateAction ({ commit }: { commit: Commit }, {
    deviceId,
    softwareUpdateAction
  }: { deviceId: number, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.deviceSoftwareUpdateActions.add(deviceId, softwareUpdateAction)
  },
  async addDeviceGenericAction ({ commit }: { commit: Commit }, {
    deviceId,
    genericDeviceAction
  }: { deviceId: number, genericDeviceAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericDeviceActions.add(deviceId, genericDeviceAction)
  },
  async addDeviceCalibrationAction ({ commit }: { commit: Commit }, {
    deviceId,
    calibrationDeviceAction
  }: { deviceId: number, calibrationDeviceAction: DeviceCalibrationAction }): Promise<DeviceCalibrationAction> {
    return this.$api.deviceCalibrationActions.add(deviceId, calibrationDeviceAction)
  },
  async updateDeviceSoftwareUpdateAction ({ commit }: { commit: Commit }, {
    deviceId,
    softwareUpdateAction
  }: { deviceId: number, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.deviceSoftwareUpdateActions.update(deviceId, softwareUpdateAction)
  },
  async updateDeviceGenericAction ({ commit }: { commit: Commit }, {
    deviceId,
    genericDeviceAction
  }: { deviceId: number, genericDeviceAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericDeviceActions.update(deviceId, genericDeviceAction)
  },
  async updateDeviceCalibrationAction ({ commit }: { commit: Commit }, {
    deviceId,
    calibrationDeviceAction
  }: { deviceId: number, calibrationDeviceAction: DeviceCalibrationAction }): Promise<DeviceCalibrationAction> {
    return  this.$api.deviceCalibrationActions.update(deviceId, calibrationDeviceAction)
  },
  async deleteDeviceAttachment ({ commit }: { commit: Commit }, attachmentId: number): Promise<void> {
    return this.$api.deviceAttachments.deleteById(attachmentId)
  },
  async addDeviceAttachment ({ commit }: { commit: Commit }, {
    deviceId,
    attachment
  }: { deviceId: number, attachment: Attachment }): Promise<void> {
    return this.$api.deviceAttachments.add(deviceId, attachment)
  },
  updateDeviceAttachment ({ commit }: { commit: Commit }, {
    deviceId,
    attachment
  }: { deviceId: number, attachment: Attachment }): Promise<void> {
    return this.$api.deviceAttachments.update(deviceId, attachment)
  },
  async deleteDeviceCustomField ({ commit }: { commit: Commit }, customField: number): Promise<void> {
    return this.$api.customfields.deleteById(customField)
  },
  async addDeviceCustomField ({ commit }: { commit: Commit }, {
    deviceId,
    deviceCustomField
  }: { deviceId: number, deviceCustomField: CustomTextField }): Promise<void> {
    return this.$api.customfields.add(deviceId, deviceCustomField)
  },
  updateDeviceCustomField ({ commit }: { commit: Commit }, {
    deviceId,
    deviceCustomField
  }: { deviceId: number, deviceCustomField: CustomTextField }): Promise<void> {
    return this.$api.customfields.update(deviceId, deviceCustomField)
  },
  async deleteDeviceMeasuredQuantity ({ commit }: { commit: Commit }, measuredQuantityId: number): Promise<void> {
    return this.$api.deviceProperties.deleteById(measuredQuantityId)
  },
  async addDeviceMeasuredQuantity ({ commit }: { commit: Commit }, {
    deviceId,
    deviceMeasuredQuantity
  }: { deviceId: number, deviceMeasuredQuantity: DeviceProperty }): Promise<void> {
    return this.$api.deviceProperties.add(deviceId, deviceMeasuredQuantity)
  },
  updateDeviceMeasuredQuantity ({ commit }: { commit: Commit }, {
    deviceId,
    deviceMeasuredQuantity
  }: { deviceId: number, deviceMeasuredQuantity: DeviceProperty }): Promise<void> {
    return this.$api.deviceProperties.update(deviceId, deviceMeasuredQuantity)
  },
  async addDeviceContact ({ commit }: { commit: Commit }, {
    deviceId,
    contactId
  }: { deviceId: number, contactId: number }): Promise<void> {
    return this.$api.devices.addContact(deviceId, contactId)
  },
  async removeDeviceContact ({ commit }: { commit: Commit }, {
    deviceId,
    contactId
  }: { deviceId: number, contactId: number }): Promise<void> {
    return this.$api.devices.removeContact(deviceId, contactId)
  },
  async saveDevice ({ commit }: { commit: Commit }, device: Device): Promise<Device> {
    return this.$api.devices.save(device)
  },
  async copyDevice(
    {commit,dispatch,state}: { commit: Commit, dispatch:Dispatch, state:devicesState},
    {device,copyContacts,copyAttachments,copyMeasuredQuantities,copyCustomFields}:
      {device:Device,copyContacts:boolean,copyAttachments:boolean,copyMeasuredQuantities:boolean,copyCustomFields:boolean}
  ){
    const savedDevice = await dispatch('saveDevice',device)
    const savedDeviceId = savedDevice.id!
    const related:Promise<any>[]=[]

    if(copyContacts){
      const contacts = device.contacts
      await dispatch('loadDeviceContacts',savedDeviceId)
      const contactsToSave = contacts.filter(c => state.deviceContacts.findIndex((ec: Contact) => { return ec.id === c.id }) === -1)

      for (const contact of contactsToSave) {
        if (contact.id) {
          related.push(dispatch('addDeviceContact',{deviceId:savedDeviceId,contactId:contact.id}))
        }
      }
    }
    if(copyAttachments){
      const attachments = device.attachments.map(Attachment.createFromObject)
      for (const attachment of attachments) {
        attachment.id = null
        related.push(dispatch('addDeviceAttachment',{deviceId:savedDeviceId,attachment:attachment}))
      }
    }
    if(copyMeasuredQuantities){
      console.log('in copyMeasuredQuantities');
      console.log('device',device);
      const measuredQuantities = device.properties.map(DeviceProperty.createFromObject)
      console.log('measuredQuantities',measuredQuantities);
      for (const measuredQuantity of measuredQuantities) {
        measuredQuantity.id = null
        related.push(dispatch('addDeviceMeasuredQuantity',{deviceId:savedDeviceId, deviceMeasuredQuantity:measuredQuantity}))
      }
    }
    if(copyCustomFields){
      const customFields = device.customFields.map(CustomTextField.createFromObject)
      for (const customField of customFields) {
        customField.id = null
        related.push(dispatch('addDeviceCustomField',{
          deviceId:savedDeviceId,
          deviceCustomField:customField}
        ))
      }
    }
    await Promise.all(related)
    return savedDeviceId
  },
  async deleteDevice ({ commit }: { commit: Commit }, id: number) {
    await this.$api.devices.deleteById(id)
  },
  async exportAsCsv ({ commit }: { commit: Commit }, searchParams: IDeviceSearchParams): Promise<Blob> {
    let email = null
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
  },
  setChosenKindOfDeviceAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfDeviceAction', newval)
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
  setDeviceContacts (state: devicesState, contacts: Contact[]) {
    state.deviceContacts = contacts
  },
  setDeviceAttachments (state: devicesState, attachments: Attachment[]) {
    state.deviceAttachments = attachments
  },
  setDeviceAttachment (state: devicesState, attachment: Attachment) {
    state.deviceAttachment = attachment
  },
  setDeviceMeasuredQuantities (state: devicesState, deviceMeasuredQuantities: DeviceProperty[]) {
    state.deviceMeasuredQuantities = deviceMeasuredQuantities
  },
  setDeviceMeasuredQuantity (state: devicesState, deviceMeasuredQuantity: DeviceProperty) {
    state.deviceMeasuredQuantity = deviceMeasuredQuantity
  },
  setDeviceGenericActions (state: devicesState, deviceGenericActions: GenericAction[]) {
    state.deviceGenericActions = deviceGenericActions
  },
  setDeviceGenericAction (state: devicesState, deviceGenericAction: GenericAction) {
    state.deviceGenericAction = deviceGenericAction
  },
  setDeviceSoftwareUpdateActions (state: devicesState, deviceSoftwareUpdateActions: SoftwareUpdateAction[]) {
    state.deviceSoftwareUpdateActions = deviceSoftwareUpdateActions
  },
  setDeviceSoftwareUpdateAction (state: devicesState, deviceSoftwareUpdateAction: SoftwareUpdateAction) {
    state.deviceSoftwareUpdateAction = deviceSoftwareUpdateAction
  },
  setDeviceMountActions (state: devicesState, deviceMountActions: DeviceMountAction[]) {
    state.deviceMountActions = deviceMountActions
  },
  setDeviceUnmountActions (state: devicesState, deviceUnmountActions: DeviceUnmountAction[]) {
    state.deviceUnmountActions = deviceUnmountActions
  },
  setDeviceCalibrationActions (state: devicesState, deviceCalibrationActions: DeviceCalibrationAction[]) {
    state.deviceCalibrationActions = deviceCalibrationActions
  },
  setDeviceCalibrationAction (state: devicesState, deviceCalibrationAction: DeviceCalibrationAction) {
    state.deviceCalibrationAction = deviceCalibrationAction
  },
  setChosenKindOfDeviceAction (state: devicesState, newVal: IOptionsForActionType | null) {
    state.chosenKindOfDeviceAction = newVal
  },
  setDeviceCustomFields(state:devicesState,deviceCustomFields:CustomTextField[]){
    state.deviceCustomFields=deviceCustomFields
  },
  setDeviceCustomField(state:devicesState,deviceCustomField:CustomTextField){
    state.deviceCustomField=deviceCustomField
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
