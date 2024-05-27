/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Commit, Dispatch, GetterTree, ActionTree } from 'vuex'

import { DateTime } from 'luxon'
import { RootState } from '@/store'
import { IncludedRelationships } from '@/services/sms/DeviceApi'

import { Attachment } from '@/models/Attachment'
import { Availability } from '@/models/Availability'
import { ContactRole } from '@/models/ContactRole'
import { CustomTextField } from '@/models/CustomTextField'
import { Device } from '@/models/Device'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { GenericAction } from '@/models/GenericAction'
import { IActionType } from '@/models/ActionType'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { Parameter } from '@/models/Parameter'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import { DeviceMountActionWrapper } from '@/viewmodels/DeviceMountActionWrapper'
import { DeviceUnmountActionWrapper } from '@/viewmodels/DeviceUnmountActionWrapper'

import { getLastPathElement } from '@/utils/urlHelpers'
import { KindOfDeviceActionType } from '@/models/ActionKind'
import {
  filterActions,
  getDistinctContactsOfActions,
  getDistinctYearsOfActions,
  sortActions
} from '@/utils/actionHelper'
import { ContactWithRoles } from '@/models/ContactWithRoles'
import { Image } from '@/models/Image'
import { ExportControl } from '@/models/ExportControl'

export type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfDeviceActionType
}

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface DevicesState {
  chosenKindOfDeviceAction: IOptionsForActionType | null
  device: Device | null
  deviceAttachment: Attachment | null
  deviceAttachments: Attachment[]
  deviceAvailabilities: Availability[]
  deviceCalibrationAction: DeviceCalibrationAction | null
  deviceCalibrationActions: DeviceCalibrationAction[]
  deviceContactRoles: ContactRole[]
  deviceCustomField: CustomTextField | null
  deviceCustomFields: CustomTextField[]
  deviceGenericAction: GenericAction | null
  deviceGenericActions: GenericAction[]
  deviceMeasuredQuantities: DeviceProperty[]
  deviceMeasuredQuantity: DeviceProperty | null
  deviceMountActions: DeviceMountAction[]
  deviceParameter: Parameter | null
  deviceParameterChangeAction: ParameterChangeAction | null
  deviceParameterChangeActions: ParameterChangeAction[]
  deviceParameters: Parameter[]
  devicePresetParameter: Parameter | null
  deviceSoftwareUpdateAction: SoftwareUpdateAction | null
  deviceSoftwareUpdateActions: SoftwareUpdateAction[]
  exportControl: ExportControl | null
  manufacturerModelId: string | null
  devices: Device[]
  pageNumber: number
  pageSize: number
  totalCount: number
  totalPages: number
}

const state = (): DevicesState => ({
  chosenKindOfDeviceAction: null,
  device: null,
  deviceAttachment: null,
  deviceAttachments: [],
  deviceAvailabilities: [],
  deviceCalibrationAction: null,
  deviceCalibrationActions: [],
  deviceContactRoles: [],
  deviceCustomField: null,
  deviceCustomFields: [],
  deviceGenericAction: null,
  deviceGenericActions: [],
  deviceMeasuredQuantities: [],
  deviceMeasuredQuantity: null,
  deviceMountActions: [],
  deviceParameter: null,
  deviceParameterChangeAction: null,
  deviceParameterChangeActions: [],
  deviceParameters: [],
  devicePresetParameter: null,
  deviceSoftwareUpdateAction: null,
  deviceSoftwareUpdateActions: [],
  exportControl: null,
  manufacturerModelId: null,
  devices: [],
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalCount: 0,
  totalPages: 1
})

export type PossibleDeviceActions = GenericAction | SoftwareUpdateAction | DeviceMountActionWrapper | DeviceUnmountActionWrapper | DeviceCalibrationAction | ParameterChangeAction
export type PageSizesGetter = number[]
export type DeviceActions = (PossibleDeviceActions)[]
export type DeviceFilter = {selectedActionTypes: IOptionsForActionType[], selectedYears: number[], selectedContacts: string[]}
export type FilteredActionsGetter = (filter: DeviceFilter) => DeviceActions
export type AvailableContactsOfActionsGetter = string[]
export type AvailableYearsOfActionsGetter = number[]

const getters: GetterTree<DevicesState, RootState> = {
  availableContactsOfActions: (_state: DevicesState, getters): string[] => {
    return getDistinctContactsOfActions(getters.actions)
  },
  availableYearsOfActions: (_state: DevicesState, getters): number[] => {
    return getDistinctYearsOfActions(getters.actions)
  },
  filteredActions: (_state: DevicesState, getters) => (filter: DeviceFilter): DeviceActions => {
    const filteredActions = filterActions(getters.actions, filter)

    const sortedFilteredActions = sortActions(filteredActions) as DeviceActions

    return sortedFilteredActions
  },
  actions: (state: DevicesState): DeviceActions => {
    const actions: DeviceActions = [
      ...state.deviceGenericActions,
      ...state.deviceSoftwareUpdateActions,
      ...state.deviceCalibrationActions,
      ...state.deviceParameterChangeActions
    ]
    for (const deviceMountAction of state.deviceMountActions) {
      actions.push(new DeviceMountActionWrapper(deviceMountAction))
      if (deviceMountAction.basicData.endDate) {
        actions.push(new DeviceUnmountActionWrapper(deviceMountAction))
      }
    }
    return actions
  },
  pageSizes: (): number[] => {
    return PAGE_SIZES
  },
  contactsWithRoles: (state: DevicesState): ContactWithRoles[] => {
    const result: ContactWithRoles[] = []
    for (const contactRole of state.deviceContactRoles) {
      const contact = contactRole.contact
      const contactId = contact?.id
      if (contact && contactId) {
        const foundIndex = result.findIndex(c => c.contact?.id === contact.id)
        if (foundIndex > -1) {
          result[foundIndex].roles.push(contactRole)
        } else {
          result.push(new ContactWithRoles(contact, [contactRole]))
        }
      }
    }
    return result
  },
  deviceParametersSortedAlphabetically: (state: DevicesState): Parameter[] => {
    // @ts-ignore
    return state.deviceParameters.toSorted((a: Parameter, b: Parameter) => a.label.toLowerCase().localeCompare(b.label.toLowerCase()))
  }
}

export type AddDeviceAttachmentAction = (params: { deviceId: string, attachment: Attachment }) => Promise<Attachment>
export type AddDeviceCalibrationAction = (params: { deviceId: string, calibrationAction: DeviceCalibrationAction }) => Promise<DeviceCalibrationAction>
export type AddDeviceContactRoleAction = (params: { deviceId: string, contactRole: ContactRole }) => Promise<void>
export type AddDeviceCustomFieldAction = (params: { deviceId: string, deviceCustomField: CustomTextField }) => Promise<CustomTextField>
export type AddDeviceGenericAction = (params: { deviceId: string, genericAction: GenericAction }) => Promise<GenericAction>
export type AddDeviceMeasuredQuantityAction = (params: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }) => Promise<DeviceProperty>
export type AddDeviceParameterAction = (params: { deviceId: string, parameter: Parameter }) => Promise<Parameter>
export type AddDeviceParameterChangeActionAction = (params: { parameterId: string, action: ParameterChangeAction }) => Promise<ParameterChangeAction>
export type AddDeviceSoftwareUpdateAction = (params: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }) => Promise<SoftwareUpdateAction>
export type ArchiveDeviceAction = (id: string) => Promise<void>
export type ClearDeviceAvailabilitiesAction = () => void
export type ClearDeviceAttachmentsAction = () => void
export type CopyDeviceAction = (params: {device: Device, copyContacts: boolean, copyAttachments: boolean, copyMeasuredQuantities: boolean, copyParameters: boolean, copyCustomFields: boolean, originalDeviceId: string}) => Promise<string>
export type CreatePidAction = (id: string | null) => Promise<string>
export type DeleteDeviceAction = (id: string) => Promise<void>
export type DeleteDeviceAttachmentAction = (attachmentId: string) => Promise<void>
export type DeleteDeviceCalibrationAction = (calibrationActionId: string) => Promise<void>
export type DeleteDeviceCustomFieldAction = (customFieldId: string) => Promise<void>
export type DeleteDeviceGenericAction = (genericActionId: string) => Promise<void>
export type DeleteDeviceImageAction = (imageId: string) => Promise<void>
export type DeleteDeviceMeasuredQuantityAction = (measuredQuantityId: string) => Promise<void>
export type DeleteDeviceParameterAction = (parameterId: string) => Promise<void>
export type DeleteDeviceParameterChangeActionAction = (actionId: string) => Promise<void>
export type DeleteDeviceSoftwareUpdateAction = (softwareUpdateActionId: string) => Promise<void>
export type DownloadAttachmentAction = (attachmentUrl: string) => Promise<Blob>
export type ExportAsCsvAction = (searchParams: IDeviceSearchParams) => Promise<Blob>
export type ExportAsSensorMLAction = (id: string) => Promise<Blob>
export type GetSensorMLUrlAction = (id: string) => string
export type LoadAllDeviceActionsAction = (id: string) => Promise<void>
export type LoadDeviceAction = (params: { deviceId: string } & IncludedRelationships) => Promise<void>
export type LoadDeviceAttachmentAction = (id: string) => Promise<void>
export type LoadDeviceAttachmentsAction = (id: string) => Promise<void>
export type LoadDeviceAvailabilitiesAction = (params: {ids: (string | null)[], from: DateTime, until: DateTime | null}) => Promise<void>
export type LoadDeviceCalibrationActionAction = (actionId: string) => Promise<void>
export type LoadDeviceCalibrationActionsAction = (id: string) => Promise<void>
export type LoadDeviceContactRolesAction = (id: string) => Promise<void>
export type LoadDeviceCustomFieldAction = (id: string) => Promise<void>
export type LoadDeviceCustomFieldsAction = (id: string) => Promise<void>
export type LoadDeviceGenericActionAction = (actionId: string) => Promise<void>
export type LoadDeviceGenericActionsAction = (id: string) => Promise<void>
export type LoadDeviceMeasuredQuantitiesAction = (id: string) => Promise<void>
export type LoadDeviceMeasuredQuantityAction = (id: string) => Promise<void>
export type LoadDeviceMountActionsAction = (id: string) => Promise<void>
export type LoadDeviceParameterAction = (id: string) => Promise<void>
export type LoadDeviceParameterChangeActionAction = (actionId: string) => Promise<void>
export type LoadDeviceParameterChangeActionsAction = (id: string) => Promise<void>
export type LoadDeviceParametersAction = (id: string) => Promise<void>
export type LoadDeviceSoftwareUpdateActionAction = (actionId: string) => Promise<void>
export type LoadDeviceSoftwareUpdateActionsAction = (id: string) => Promise<void>
export type LoadExportControlAction = (params: { deviceId: string}) => Promise<void>
export type LoadManufacturerModelIdAction = (params: { deviceId: string}) => Promise<void>
export type RemoveDeviceContactRoleAction = (params: { deviceContactRoleId: string }) => Promise<void>
export type ReplaceDeviceInDevicesAction = (newDevice: Device) => void
export type RestoreDeviceAction = (id: string) => Promise<void>
export type SaveDeviceAction = (device: Device) => Promise<Device>
export type SaveDeviceImagesAction = (params: {deviceId: string, deviceImages: Image[], deviceCopyImages: Image[]}) => Promise<Image[]>
export type SearchDevicesPaginatedAction = (searchParams: IDeviceSearchParams) => Promise<void>
export type SetChosenKindOfDeviceActionAction = (newval: IOptionsForActionType | null) => void
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type SetDevicePresetParameterAction = (parameter: Parameter | null) => void
export type UpdateDeviceAttachmentAction = (params: { deviceId: string, attachment: Attachment }) => Promise<Attachment>
export type UpdateDeviceCalibrationAction = (params: { deviceId: string, calibrationAction: DeviceCalibrationAction }) => Promise<DeviceCalibrationAction>
export type UpdateDeviceCustomFieldAction = (params: { deviceId: string, deviceCustomField: CustomTextField }) => Promise<CustomTextField>
export type UpdateDeviceGenericAction = (params: { deviceId: string, genericAction: GenericAction }) => Promise<GenericAction>
export type UpdateDeviceMeasuredQuantityAction = (params: { deviceId: string, deviceMeasuredQuantity: DeviceProperty }) => Promise<DeviceProperty>
export type UpdateDeviceParameterAction = (params: { deviceId: string, parameter: Parameter }) => Promise<Parameter>
export type UpdateDeviceParameterChangeActionAction = (params: { parameterId: string, action: ParameterChangeAction }) => Promise<ParameterChangeAction>
export type UpdateDeviceSoftwareUpdateAction = (params: { deviceId: string, softwareUpdateAction: SoftwareUpdateAction }) => Promise<SoftwareUpdateAction>

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
      .setSearchIncludeArchivedDevices(searchParams.includeArchivedDevices)
      .setSearchManufacturerName(searchParams.manufacturerName)
      .setSearchModel(searchParams.model)
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
    commit('setTotalCount', totalCount)
  },
  async loadDevice ({ commit }: { commit: Commit },
    {
      deviceId,
      includeContacts,
      includeCustomFields,
      includeDeviceProperties,
      includeDeviceAttachments,
      includeImages,
      includeDeviceParameters,
      includeCreatedBy,
      includeUpdatedBy
    }: { deviceId: string } & IncludedRelationships
  ): Promise<void> {
    const device = await this.$api.devices.findById(deviceId, {
      includeContacts,
      includeCustomFields,
      includeDeviceProperties,
      includeDeviceAttachments,
      includeImages,
      includeDeviceParameters,
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
      dispatch('loadDeviceCalibrationActions', id),
      dispatch('loadDeviceParameterChangeActions', id)
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
  async loadDeviceParameterChangeActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const actions = await this.$api.devices.findRelatedParameterChangeActions(id)
    commit('setDeviceParameterChangeActions', actions)
  },
  async loadDeviceParameterChangeAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const action = await this.$api.deviceParameterChangeActions.findById(actionId)
    commit('setDeviceParameterChangeAction', action)
  },
  async loadDeviceCustomFields ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const deviceCustomFields = await this.$api.devices.findRelatedCustomFields(id)
    commit('setDeviceCustomFields', deviceCustomFields)
  },
  async loadDeviceCustomField ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const deviceCustomField = await this.$api.deviceCustomfields.findById(id)
    commit('setDeviceCustomField', deviceCustomField)
  },
  async loadDeviceAvailabilities ({ commit }: {commit: Commit}, {
    ids,
    from,
    until
  }: {
    ids: (string|null)[];
    from: DateTime;
    until: DateTime | null
  }): Promise<void> {
    const deviceAvailabilities = await this.$api.devices.checkAvailability(ids, from, until)
    commit('setDeviceAvailabilities', deviceAvailabilities)
  },
  async loadDeviceParameters ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const deviceParameters = await this.$api.devices.findRelatedDeviceParameters(id)
    commit('setDeviceParameters', deviceParameters)
  },
  async loadDeviceParameter ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const parameter = await this.$api.deviceParameters.findById(id)
    commit('setDeviceParameter', parameter)
  },
  async loadExportControl ({ commit }: { commit: Commit }, { deviceId }: { deviceId: string }) {
    const exportControl = await this.$api.devices.findExportControlByManufacturerModelIdOrNewOne(deviceId)
    commit('setExportControl', exportControl)
  },
  async loadManufacturerModelId ({ commit }: { commit: Commit }, { deviceId }: { deviceId: string }) {
    const device = await this.$api.devices.findById(deviceId)
    const manufacturerName = device.manufacturerName
    const model = device.model
    const manufacturerModel = await this.$api.manufacturerModels.findByManufacturerNameAndModel(manufacturerName, model, { includeExportControl: false })
    if (manufacturerModel) {
      commit('setManufacturerModelId', manufacturerModel.id)
    } else {
      commit('setManufacturerModelId', null)
    }
  },
  deleteDeviceParameter (_, parameterId: string): Promise<void> {
    return this.$api.deviceParameters.deleteById(parameterId)
  },
  addDeviceParameter (_, {
    deviceId,
    parameter
  }: { deviceId: string, parameter: Parameter }): Promise<Parameter> {
    return this.$api.deviceParameters.add(deviceId, parameter)
  },
  updateDeviceParameter (_, {
    deviceId,
    parameter
  }: { deviceId: string, parameter: Parameter }): Promise<Parameter> {
    return this.$api.deviceParameters.update(deviceId, parameter)
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
  addDeviceCalibrationAction (_, {
    deviceId,
    calibrationAction
  }: { deviceId: string, calibrationAction: DeviceCalibrationAction }): Promise<DeviceCalibrationAction> {
    return this.$api.deviceCalibrationActions.add(deviceId, calibrationAction)
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
  addDeviceParameterChangeAction (_, {
    parameterId,
    action
  }: { parameterId: string, action: ParameterChangeAction }): Promise<ParameterChangeAction> {
    return this.$api.deviceParameterChangeActions.add(parameterId, action)
  },
  updateDeviceParameterChangeAction (_, {
    parameterId,
    action
  }: { parameterId: string, action: ParameterChangeAction }): Promise<ParameterChangeAction> {
    return this.$api.deviceParameterChangeActions.update(parameterId, action)
  },
  deleteDeviceParameterChangeAction (_, actionId: string): Promise<void> {
    return this.$api.deviceParameterChangeActions.deleteById(actionId)
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
  deleteDeviceCustomField (_, customFieldId: string): Promise<void> {
    return this.$api.deviceCustomfields.deleteById(customFieldId)
  },
  addDeviceCustomField (_, {
    deviceId,
    deviceCustomField
  }: { deviceId: string, deviceCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.deviceCustomfields.add(deviceId, deviceCustomField)
  },
  updateDeviceCustomField (_, {
    deviceId,
    deviceCustomField
  }: { deviceId: string, deviceCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.deviceCustomfields.update(deviceId, deviceCustomField)
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
  deleteDeviceImage (_, imageId: string): Promise<void> {
    return this.$api.deviceImages.deleteById(imageId)
  },
  updateDeviceImage (_, {
    deviceId,
    deviceImage
  }: { deviceId: string, deviceImage: Image }): Promise<Image> {
    return this.$api.deviceImages.update(deviceId, deviceImage)
  },
  addDeviceImage (_, {
    deviceId,
    deviceImage
  }: { deviceId: string, deviceImage: Image }): Promise<Image> {
    return this.$api.deviceImages.add(deviceId, deviceImage)
  },
  async saveDeviceImages (
    { dispatch }: { dispatch: Dispatch }, {
      deviceId,
      deviceImages,
      deviceCopyImages
    }: {deviceId: string, deviceImages: Image[], deviceCopyImages: Image[]}): Promise<Image[]> {
    const imagesToDelete = deviceImages.filter(el => !deviceCopyImages.map(i => i.id).includes(el.id))
    imagesToDelete.forEach(async (deviceImage) => {
      await dispatch('deleteDeviceImage', deviceImage.id)
    })
    const images = deviceCopyImages
    for (const i in images) {
      const imageId = images[i].id
      if (!imageId) {
        images[i].id = (await dispatch('addDeviceImage', { deviceId, deviceImage: images[i] })).id
      } else if (deviceImages.find(i => i.id === imageId)?.orderIndex !== images[i].orderIndex) {
        images[i].id = (await dispatch('updateDeviceImage', { deviceId, deviceImage: images[i] })).id
      }
    }

    return images
  },
  saveDevice (_, device: Device): Promise<Device> {
    return this.$api.devices.save(device)
  },
  createPid (_, id: string | null): Promise<string> {
    return this.$api.pids.create(id, 'device')
  },
  async copyDevice (
    { dispatch }: { dispatch: Dispatch },
    { device, copyContacts, copyAttachments, copyMeasuredQuantities, copyParameters, copyCustomFields, originalDeviceId }:
      {device: Device, copyContacts: boolean, copyAttachments: boolean, copyMeasuredQuantities: boolean, copyParameters: boolean, copyCustomFields: boolean, originalDeviceId: string}
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

    const deviceImages = device.images.map(Image.createFromObject)
    const deviceAttachments = device.attachments.map(Attachment.createFromObject)
    for (const attachment of deviceAttachments) {
      // copy if attachments should be copied or copied images include attachment
      if (!copyAttachments && !deviceImages.map(i => i.attachment?.id).includes(attachment.id)) {
        continue
      }

      const oldAttachmentId = attachment.id
      attachment.id = null

      if (attachment.isUpload) {
        const blob = await dispatch('downloadAttachment', attachment.url)
        const filename = getLastPathElement(attachment.url)
        const uploadResult = await dispatch('files/uploadBlob', { blob, filename }, { root: true })
        const newUrl = uploadResult.url
        attachment.url = newUrl
      }
      const savedAttachment = await dispatch('addDeviceAttachment', { deviceId: savedDeviceId, attachment })

      const deviceImageToCopy = deviceImages.find(i => i.attachment?.id && i.attachment.id === oldAttachmentId)
      if (!deviceImageToCopy) { continue }
      const deviceImage = Image.createFromObject(deviceImageToCopy)
      deviceImage.id = ''
      deviceImage.attachment = savedAttachment
      related.push(dispatch('addDeviceImage', { deviceId: savedDeviceId, deviceImage }))
    }

    if (copyMeasuredQuantities) {
      const measuredQuantities = device.properties.map(DeviceProperty.createFromObject)
      for (const measuredQuantity of measuredQuantities) {
        measuredQuantity.id = null
        related.push(dispatch('addDeviceMeasuredQuantity', { deviceId: savedDeviceId, deviceMeasuredQuantity: measuredQuantity }))
      }
    }
    if (copyParameters) {
      const parameters = device.parameters.map(Parameter.createFromObject)
      for (const parameter of parameters) {
        parameter.id = null
        related.push(dispatch('addDeviceParameter', { deviceId: savedDeviceId, parameter }))
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
  async archiveDevice (_, id: string): Promise<void> {
    await this.$api.devices.archiveById(id)
  },
  async restoreDevice (_, id: string): Promise<void> {
    await this.$api.devices.restoreById(id)
  },
  async downloadAttachment (_, attachmentUrl: string): Promise<Blob> {
    return await this.$api.deviceAttachments.getFile(attachmentUrl)
  },
  getSensorMLUrl (_, id: string): string {
    return this.$api.devices.getSensorMLUrl(id)
  },
  async exportAsSensorML (_, id: string): Promise<Blob> {
    return await this.$api.devices.getSensorML(id)
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
      .setSearchIncludeArchivedDevices(searchParams.includeArchivedDevices)
      .searchMatchingAsCsvBlob()
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  setDevicePresetParameter ({ commit }: { commit: Commit }, parameter: Parameter | null) {
    commit('setDevicePresetParameter', parameter)
  },
  setChosenKindOfDeviceAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfDeviceAction', newval)
  },
  replaceDeviceInDevices ({ commit, state }: {commit: Commit, state: DevicesState}, newDevice: Device) {
    const result = []
    for (const oldDevice of state.devices) {
      if (oldDevice.id !== newDevice.id) {
        result.push(oldDevice)
      } else {
        result.push(newDevice)
      }
    }
    commit('setDevices', result)
  },
  clearDeviceAvailabilities ({ commit }: { commit: Commit }) {
    commit('setDeviceAvailabilities', [])
  },
  clearDeviceAttachments ({ commit }: { commit: Commit }): void {
    commit('setDeviceAttachments', [])
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
  setTotalCount (state: DevicesState, count: number) {
    state.totalCount = count
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
  },
  setDeviceAvailabilities (state: DevicesState, deviceAvailabilities: Availability[]) {
    state.deviceAvailabilities = deviceAvailabilities
  },
  setDeviceParameters (state: DevicesState, deviceParameters: Parameter[]) {
    state.deviceParameters = deviceParameters
  },
  setDeviceParameter (state: DevicesState, deviceParameter: Parameter) {
    state.deviceParameter = deviceParameter
  },
  setDevicePresetParameter (state: DevicesState, devicePresetParameter: Parameter | null) {
    state.devicePresetParameter = devicePresetParameter
  },
  setDeviceParameterChangeActions (state: DevicesState, deviceParameterChangeActions: ParameterChangeAction[]) {
    state.deviceParameterChangeActions = deviceParameterChangeActions
  },
  setDeviceParameterChangeAction (state: DevicesState, deviceParameterChangeAction: ParameterChangeAction) {
    state.deviceParameterChangeAction = deviceParameterChangeAction
  },
  setExportControl (state: DevicesState, exportControl: ExportControl) {
    state.exportControl = exportControl
  },
  setManufacturerModelId (state: DevicesState, manufacturerModelId: string | null) {
    state.manufacturerModelId = manufacturerModelId
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
