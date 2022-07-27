/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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

import { Commit, Dispatch, GetterTree, ActionTree } from 'vuex'

import { RootState } from '@/store'

import { Device } from '@/models/Device'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { ContactRole } from '@/models/ContactRole'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { IActionType } from '@/models/ActionType'
import { DeviceProperty } from '@/models/DeviceProperty'
import { CustomTextField } from '@/models/CustomTextField'
import { DeviceUnmountActionWrapper } from '@/viewmodels/DeviceUnmountActionWrapper'
import { DeviceMountActionWrapper } from '@/viewmodels/DeviceMountActionWrapper'
import { IDateCompareable } from '@/modelUtils/Compareables'

import { IncludedRelationships } from '@/services/sms/DeviceApi'

const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType =
  typeof KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  | typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  | typeof KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
  | typeof KIND_OF_ACTION_TYPE_UNKNOWN

export type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface DevicesState {
  devices: Device[],
  device: Device | null,
  deviceContactRoles: ContactRole[],
  deviceAttachments: Attachment[],
  deviceAttachment: Attachment | null,
  deviceMeasuredQuantities: DeviceProperty[],
  deviceMeasuredQuantity: DeviceProperty | null,
  deviceGenericActions: GenericAction[],
  deviceSoftwareUpdateActions: SoftwareUpdateAction[],
  deviceCalibrationActions: DeviceCalibrationAction[],
  deviceGenericAction: GenericAction | null,
  deviceSoftwareUpdateAction: SoftwareUpdateAction | null,
  deviceCalibrationAction: DeviceCalibrationAction | null,
  deviceMountActions: DeviceMountAction[],
  chosenKindOfDeviceAction: IOptionsForActionType | null,
  deviceCustomFields: CustomTextField[],
  deviceCustomField: CustomTextField | null
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = (): DevicesState => ({
  devices: [],
  device: null,
  deviceContactRoles: [],
  deviceAttachments: [],
  deviceAttachment: null,
  deviceMeasuredQuantities: [],
  deviceMeasuredQuantity: null,
  deviceGenericActions: [],
  deviceSoftwareUpdateActions: [],
  deviceGenericAction: null,
  deviceSoftwareUpdateAction: null,
  deviceCalibrationAction: null,
  deviceCalibrationActions: [],
  deviceMountActions: [],
  chosenKindOfDeviceAction: null,
  deviceCustomFields: [],
  deviceCustomField: null,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalPages: 1
})

export type ActionsGetter = (GenericAction | SoftwareUpdateAction | DeviceMountActionWrapper | DeviceUnmountActionWrapper | DeviceCalibrationAction)[]
export type PageSizesGetter = number[]

const getters: GetterTree<DevicesState, RootState> = {
  actions: (state: DevicesState): (GenericAction | SoftwareUpdateAction | DeviceMountActionWrapper | DeviceUnmountActionWrapper | DeviceCalibrationAction)[] => { // Todo actions sortieren, wobei ehrlich gesagt, eine extra route im Backend mit allen Actions (sortiert) besser wäre
    let actions: (GenericAction | SoftwareUpdateAction | DeviceMountActionWrapper | DeviceUnmountActionWrapper | DeviceCalibrationAction)[] = [
      ...state.deviceGenericActions,
      ...state.deviceSoftwareUpdateActions,
      ...state.deviceCalibrationActions
    ]
    for (const deviceMountAction of state.deviceMountActions) {
      actions.push(new DeviceMountActionWrapper(deviceMountAction))
      if (deviceMountAction.basicData.endDate) {
        actions.push(new DeviceUnmountActionWrapper(deviceMountAction))
      }
    }
    // TODO: Extra deviceUnmountActionWrapper befüllen
    // sort the actions
    actions = actions.sort((a: IDateCompareable, b: IDateCompareable): number => {
      if (a.date === null || b.date === null) { return 0 }
      return a.date < b.date ? 1 : a.date > b.date ? -1 : 0
    })
    return actions
  },
  pageSizes: (): number[] => {
    return PAGE_SIZES
  }
}

export type LoadDeviceAction = (params: { deviceId: string } & IncludedRelationships) => Promise<void>
export type SearchDevicesPaginatedAction = (searchParams: IDeviceSearchParams) => Promise<void>
export type SearchDevicesAction = (id: string) => Promise<void>
export type LoadDeviceContactRolesAction = (id: string) => Promise<void>
export type LoadDeviceAttachmentsAction = (id: string) => Promise<void>
export type LoadDeviceAttachmentAction = (id: string) => Promise<void>
export type LoadDeviceMeasuredQuantitiesAction = (id: string) => Promise<void>
export type LoadDeviceMeasuredQuantityAction = (id: string) => Promise<void>
export type LoadAllDeviceActionsAction = (id: string) => Promise<void>
export type LoadDeviceGenericActionsAction = (id: string) => Promise<void>
export type LoadDeviceGenericActionAction = (actionId: string) => Promise<void>
export type LoadDeviceSoftwareUpdateActionsAction = (id: string) => Promise<void>
export type LoadDeviceSoftwareUpdateActionAction = (actionId: string) => Promise<void>
export type LoadDeviceCalibrationActionsAction = (id: string) => Promise<void>
export type LoadDeviceCalibrationActionAction = (actionId: string) => Promise<void>
export type LoadDeviceMountActionsAction = (id: string) => Promise<void>
export type LoadDeviceCustomFieldsAction = (id: string) => Promise<void>
export type LoadDeviceCustomFieldAction = (id: string) => Promise<void>
export type AddDeviceSoftwareUpdateAction = (params: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }) => Promise<SoftwareUpdateAction>
export type AddDeviceGenericAction = (params: { deviceId: string, genericAction: GenericAction }) => Promise<GenericAction>
export type AddDeviceCalibrationAction = (params: { deviceId: string, calibrationAction: DeviceCalibrationAction }) => Promise<DeviceCalibrationAction>
export type UpdateDeviceSoftwareUpdateAction = (params: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }) => Promise<SoftwareUpdateAction>
export type UpdateDeviceGenericAction = (params: { deviceId: string, genericAction: GenericAction }) => Promise<GenericAction>
export type UpdateDeviceCalibrationAction = (params: { deviceId: string, calibrationAction: DeviceCalibrationAction }) => Promise<DeviceCalibrationAction>
export type DeleteDeviceSoftwareUpdateAction = (softwareUpdateActionId: string) => Promise<void>
export type DeleteDeviceGenericAction = (genericActionId: string) => Promise<void>
export type DeleteDeviceCalibrationAction = (calibrationActionId: string) => Promise<void>
export type DeleteDeviceAttachmentAction = (attachmentId: string) => Promise<void>
export type AddDeviceAttachmentAction = (params: { deviceId: string, attachment: Attachment }) => Promise<Attachment>
export type UpdateDeviceAttachmentAction = (params: { deviceId: string, attachment: Attachment }) => Promise<Attachment>
export type DeleteDeviceCustomFieldAction = (customField: string) => Promise<void>
export type AddDeviceCustomFieldAction = (params: { deviceId: string, deviceCustomField: CustomTextField }) => Promise<CustomTextField>
export type UpdateDeviceCustomFieldAction = (params: { deviceId: string, deviceCustomField: CustomTextField }) => Promise<CustomTextField>
export type DeleteDeviceMeasuredQuantityAction = (measuredQuantityId: string) => Promise<void>
export type AddDeviceMeasuredQuantityAction = (params: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }) => Promise<DeviceProperty>
export type UpdateDeviceMeasuredQuantityAction = (params: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }) => Promise<DeviceProperty>
export type AddDeviceContactRoleAction = (params: { deviceId: string, contactRole: ContactRole }) => Promise<void>
export type RemoveDeviceContactRoleAction = (params: { deviceContactRoleId: string }) => Promise<void>
export type SaveDeviceAction = (device: Device) => Promise<Device>
export type CopyDeviceAction = (params: {device: Device, copyContacts: boolean, copyAttachments: boolean, copyMeasuredQuantities: boolean, copyCustomFields: boolean, originalDeviceId: string}) => Promise<string>
export type DeleteDeviceAction = (id: string) => Promise<void>
export type ExportAsCsvAction = (searchParams: IDeviceSearchParams) => Promise<Blob>
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type SetChosenKindOfDeviceActionAction = (newval: IOptionsForActionType | null) => void

const actions: ActionTree<DevicesState, RootState> = {
  async searchDevicesPaginated ({
    commit,
    state
  }: { commit: Commit, state: DevicesState }, searchParams: IDeviceSearchParams): Promise<void> {
    let userId = null
    if (searchParams.onlyOwnDevices) {
      userId = this.getters['permissions/userId']
    }

    const {
      elements,
      totalCount
    } = await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedPermissionGroups(searchParams.permissionGroups)
      .setSearchedCreatorId(userId)
      .searchPaginated(
        state.pageNumber,
        state.pageSize,
        {
          includeCreatedBy: true
        }
      )
    commit('setDevices', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async searchDevices ({ commit }: { commit: Commit }, searchText: string = ''): Promise<void> {
    const devices = await this.$api.devices
      .setSearchText(searchText)
      .searchAll()
    commit('setDevices', devices)
  },
  async loadDevice ({ commit }: { commit: Commit },
    {
      deviceId,
      includeContacts,
      includeCustomFields,
      includeDeviceProperties,
      includeDeviceAttachments,
      includeCreatedBy,
      includeUpdatedBy
    }: { deviceId: string } & IncludedRelationships
  ): Promise<void> {
    const device = await this.$api.devices.findById(deviceId, {
      includeContacts,
      includeCustomFields,
      includeDeviceProperties,
      includeDeviceAttachments,
      includeCreatedBy,
      includeUpdatedBy
    })
    commit('setDevice', device)
  },
  async loadDeviceContactRoles ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceContactRoles = await this.$api.devices.findRelatedContactRoles(id)
    commit('setDeviceContactRoles', deviceContactRoles)
  },
  async loadDeviceAttachments ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceAttachments = await this.$api.devices.findRelatedDeviceAttachments(id)
    commit('setDeviceAttachments', deviceAttachments)
  },
  async loadDeviceAttachment ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceAttachment = await this.$api.deviceAttachments.findById(id)
    commit('setDeviceAttachment', deviceAttachment)
  },
  async loadDeviceMeasuredQuantities ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceMeasuredQuantities = await this.$api.devices.findRelatedDeviceProperties(id)
    commit('setDeviceMeasuredQuantities', deviceMeasuredQuantities)
  },
  async loadDeviceMeasuredQuantity ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceMeasuredQuantity = await this.$api.deviceProperties.findById(id)
    commit('setDeviceMeasuredQuantity', deviceMeasuredQuantity)
  },
  async loadAllDeviceActions ({ dispatch }: { dispatch: Dispatch }, id: string): Promise<void> {
    await Promise.all([
      dispatch('loadDeviceGenericActions', id),
      dispatch('loadDeviceSoftwareUpdateActions', id),
      dispatch('loadDeviceMountActions', id),
      dispatch('loadDeviceCalibrationActions', id)
    ])
  },
  async loadDeviceGenericActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceGenericActions = await this.$api.devices.findRelatedGenericActions(id)
    commit('setDeviceGenericActions', deviceGenericActions)
  },
  async loadDeviceGenericAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const deviceGenericAction = await this.$api.genericDeviceActions.findById(actionId)
    commit('setDeviceGenericAction', deviceGenericAction)
  },
  async loadDeviceSoftwareUpdateActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceSoftwareUpdateActions = await this.$api.devices.findRelatedSoftwareUpdateActions(id)
    commit('setDeviceSoftwareUpdateActions', deviceSoftwareUpdateActions)
  },
  async loadDeviceSoftwareUpdateAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const deviceSoftwareUpdateAction = await this.$api.deviceSoftwareUpdateActions.findById(actionId)
    commit('setDeviceSoftwareUpdateAction', deviceSoftwareUpdateAction)
  },
  async loadDeviceCalibrationActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceCalibrationActions = await this.$api.devices.findRelatedCalibrationActions(id)
    commit('setDeviceCalibrationActions', deviceCalibrationActions)
  },
  async loadDeviceCalibrationAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const deviceCalibrationAction = await this.$api.deviceCalibrationActions.findById(actionId)
    commit('setDeviceCalibrationAction', deviceCalibrationAction)
  },
  async loadDeviceMountActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceMountActions = await this.$api.devices.findRelatedMountActions(id)
    commit('setDeviceMountActions', deviceMountActions)
  },
  async loadDeviceCustomFields ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const deviceCustomFields = await this.$api.devices.findRelatedCustomFields(id)
    commit('setDeviceCustomFields', deviceCustomFields)
  },
  async loadDeviceCustomField ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const deviceCustomField = await this.$api.customfields.findById(id)
    commit('setDeviceCustomField', deviceCustomField)
  },
  addDeviceSoftwareUpdateAction (_, {
    deviceId,
    softwareUpdateAction
  }: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.deviceSoftwareUpdateActions.add(deviceId, softwareUpdateAction)
  },
  addDeviceGenericAction (_, {
    deviceId,
    genericAction
  }: { deviceId: string, genericAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericDeviceActions.add(deviceId, genericAction)
  },
  addDeviceCalibrationAction (_, {
    deviceId,
    calibrationAction
  }: { deviceId: string, calibrationAction: DeviceCalibrationAction }): Promise<DeviceCalibrationAction> {
    return this.$api.deviceCalibrationActions.add(deviceId, calibrationAction)
  },
  updateDeviceSoftwareUpdateAction (_, {
    deviceId,
    softwareUpdateAction
  }: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.deviceSoftwareUpdateActions.update(deviceId, softwareUpdateAction)
  },
  deleteDeviceSoftwareUpdateAction (_, softwareUpdateActionId: string): Promise<void> {
    return this.$api.deviceSoftwareUpdateActions.deleteById(softwareUpdateActionId)
  },
  updateDeviceGenericAction (_, {
    deviceId,
    genericAction
  }: { deviceId: string, genericAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericDeviceActions.update(deviceId, genericAction)
  },
  deleteDeviceGenericAction (_, genericActionId: string): Promise<void> {
    return this.$api.genericDeviceActions.deleteById(genericActionId)
  },
  updateDeviceCalibrationAction (_, {
    deviceId,
    calibrationAction
  }: { deviceId: string, calibrationAction: DeviceCalibrationAction }): Promise<DeviceCalibrationAction> {
    return this.$api.deviceCalibrationActions.update(deviceId, calibrationAction)
  },
  deleteDeviceCalibrationAction (_, calibrationActionId: string): Promise<void> {
    return this.$api.deviceCalibrationActions.deleteById(calibrationActionId)
  },
  deleteDeviceAttachment (_, attachmentId: string): Promise<void> {
    return this.$api.deviceAttachments.deleteById(attachmentId)
  },
  addDeviceAttachment (_, {
    deviceId,
    attachment
  }: { deviceId: string, attachment: Attachment }): Promise<Attachment> {
    return this.$api.deviceAttachments.add(deviceId, attachment)
  },
  updateDeviceAttachment (_, {
    deviceId,
    attachment
  }: { deviceId: string, attachment: Attachment }): Promise<Attachment> {
    return this.$api.deviceAttachments.update(deviceId, attachment)
  },
  deleteDeviceCustomField (_, customField: string): Promise<void> {
    return this.$api.customfields.deleteById(customField)
  },
  addDeviceCustomField (_, {
    deviceId,
    deviceCustomField
  }: { deviceId: string, deviceCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.customfields.add(deviceId, deviceCustomField)
  },
  updateDeviceCustomField (_, {
    deviceId,
    deviceCustomField
  }: { deviceId: string, deviceCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.customfields.update(deviceId, deviceCustomField)
  },
  deleteDeviceMeasuredQuantity (_, measuredQuantityId: string): Promise<void> {
    return this.$api.deviceProperties.deleteById(measuredQuantityId)
  },
  addDeviceMeasuredQuantity (_, {
    deviceId,
    deviceMeasuredQuantity
  }: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }): Promise<DeviceProperty> {
    return this.$api.deviceProperties.add(deviceId, deviceMeasuredQuantity)
  },
  updateDeviceMeasuredQuantity (_, {
    deviceId,
    deviceMeasuredQuantity
  }: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }): Promise<DeviceProperty> {
    return this.$api.deviceProperties.update(deviceId, deviceMeasuredQuantity)
  },
  addDeviceContactRole (_, {
    deviceId,
    contactRole
  }: { deviceId: string, contactRole: ContactRole }): Promise<string> {
    return this.$api.devices.addContact(deviceId, contactRole)
  },
  removeDeviceContactRole (_, {
    deviceContactRoleId
  }: { deviceContactRoleId: string }): Promise<void> {
    return this.$api.devices.removeContact(deviceContactRoleId)
  },
  saveDevice (_, device: Device): Promise<Device> {
    return this.$api.devices.save(device)
  },
  async copyDevice (
    { dispatch }: { dispatch: Dispatch },
    { device, copyContacts, copyAttachments, copyMeasuredQuantities, copyCustomFields, originalDeviceId }:
      {device: Device, copyContacts: boolean, copyAttachments: boolean, copyMeasuredQuantities: boolean, copyCustomFields: boolean, originalDeviceId: string}
  ): Promise<string> {
    const savedDevice = await dispatch('saveDevice', device)
    const savedDeviceId = savedDevice.id!
    const related: Promise<any>[] = []

    if (copyContacts) {
      // TODO: My basic idea was that the device is the old one. But it is not. It has no id. So what can I do about that?
      const sourceContactRoles = await this.$api.devices.findRelatedContactRoles(originalDeviceId)
      // The system creates the owner automatically when we create the device
      const freshCreatedContactRoles = await this.$api.devices.findRelatedContactRoles(savedDeviceId)
      const contactRolesToSave = sourceContactRoles.filter(c => freshCreatedContactRoles.findIndex((ec: ContactRole) => { return ec.contact!.id === c.contact!.id && ec.roleUri === c.roleUri }) === -1)

      for (const contactRole of contactRolesToSave) {
        const contactRoleToSave = ContactRole.createFromObject(contactRole)
        contactRoleToSave.id = null
        related.push(dispatch('addDeviceContactRole', {
          deviceId: savedDeviceId,
          contactRole: contactRoleToSave
        }))
      }
    }
    if (copyAttachments) {
      const attachments = device.attachments.map(Attachment.createFromObject)
      for (const attachment of attachments) {
        attachment.id = null
        related.push(dispatch('addDeviceAttachment', { deviceId: savedDeviceId, attachment }))
      }
    }
    if (copyMeasuredQuantities) {
      const measuredQuantities = device.properties.map(DeviceProperty.createFromObject)
      for (const measuredQuantity of measuredQuantities) {
        measuredQuantity.id = null
        related.push(dispatch('addDeviceMeasuredQuantity', { deviceId: savedDeviceId, deviceMeasuredQuantity: measuredQuantity }))
      }
    }
    if (copyCustomFields) {
      const customFields = device.customFields.map(CustomTextField.createFromObject)
      for (const customField of customFields) {
        customField.id = null
        related.push(dispatch('addDeviceCustomField', {
          deviceId: savedDeviceId,
          deviceCustomField: customField
        }
        ))
      }
    }
    await Promise.all(related)
    return savedDeviceId
  },
  async deleteDevice (_, id: string): Promise<void> {
    await this.$api.devices.deleteById(id)
  },
  async exportAsCsv (_, searchParams: IDeviceSearchParams): Promise<Blob> {
    let userId = null
    if (searchParams.onlyOwnDevices) {
      userId = this.getters['permissions/userId']
    }
    // @ts-ignore
    return await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedPermissionGroups(searchParams.permissionGroups)
      .setSearchedCreatorId(userId)
      .searchMatchingAsCsvBlob()
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  setChosenKindOfDeviceAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfDeviceAction', newval)
  }
}

const mutations = {
  setDevices (state: DevicesState, devices: Device[]) {
    state.devices = devices
  },
  setDevice (state: DevicesState, device: Device) {
    state.device = device
  },
  setPageNumber (state: DevicesState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setPageSize (state: DevicesState, newPageSize: number) {
    state.pageSize = newPageSize
  },
  setTotalPages (state: DevicesState, count: number) {
    state.totalPages = count
  },
  setDeviceContactRoles (state: DevicesState, contactRoles: ContactRole[]) {
    state.deviceContactRoles = contactRoles
  },
  setDeviceAttachments (state: DevicesState, attachments: Attachment[]) {
    state.deviceAttachments = attachments
  },
  setDeviceAttachment (state: DevicesState, attachment: Attachment) {
    state.deviceAttachment = attachment
  },
  setDeviceMeasuredQuantities (state: DevicesState, deviceMeasuredQuantities: DeviceProperty[]) {
    state.deviceMeasuredQuantities = deviceMeasuredQuantities
  },
  setDeviceMeasuredQuantity (state: DevicesState, deviceMeasuredQuantity: DeviceProperty) {
    state.deviceMeasuredQuantity = deviceMeasuredQuantity
  },
  setDeviceGenericActions (state: DevicesState, deviceGenericActions: GenericAction[]) {
    state.deviceGenericActions = deviceGenericActions
  },
  setDeviceGenericAction (state: DevicesState, deviceGenericAction: GenericAction) {
    state.deviceGenericAction = deviceGenericAction
  },
  setDeviceSoftwareUpdateActions (state: DevicesState, deviceSoftwareUpdateActions: SoftwareUpdateAction[]) {
    state.deviceSoftwareUpdateActions = deviceSoftwareUpdateActions
  },
  setDeviceSoftwareUpdateAction (state: DevicesState, deviceSoftwareUpdateAction: SoftwareUpdateAction) {
    state.deviceSoftwareUpdateAction = deviceSoftwareUpdateAction
  },
  setDeviceMountActions (state: DevicesState, deviceMountActions: DeviceMountAction[]) {
    state.deviceMountActions = deviceMountActions
  },
  setDeviceCalibrationActions (state: DevicesState, deviceCalibrationActions: DeviceCalibrationAction[]) {
    state.deviceCalibrationActions = deviceCalibrationActions
  },
  setDeviceCalibrationAction (state: DevicesState, deviceCalibrationAction: DeviceCalibrationAction) {
    state.deviceCalibrationAction = deviceCalibrationAction
  },
  setChosenKindOfDeviceAction (state: DevicesState, newVal: IOptionsForActionType | null) {
    state.chosenKindOfDeviceAction = newVal
  },
  setDeviceCustomFields (state: DevicesState, deviceCustomFields: CustomTextField[]) {
    state.deviceCustomFields = deviceCustomFields
  },
  setDeviceCustomField (state: DevicesState, deviceCustomField: CustomTextField) {
    state.deviceCustomField = deviceCustomField
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
