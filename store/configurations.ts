/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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
import { Commit, Dispatch, GetterTree, ActionTree } from 'vuex/types'

import { DateTime } from 'luxon'

import { RootState } from '@/store'

import { Configuration } from '@/models/Configuration'
import { ConfigurationMountingAction } from '@/models/ConfigurationMountingAction'
import { ContactRole } from '@/models/ContactRole'
import { CustomTextField } from '@/models/CustomTextField'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { StaticLocationAction } from '@/models/StaticLocationAction'

import { byDateOldestLast } from '@/modelUtils/mountHelpers'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'

import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'

import {
  DeviceMountTimelineAction,
  DeviceUnmountTimelineAction,
  DynamicLocationBeginTimelineAction,
  DynamicLocationEndTimelineAction,
  ITimelineAction,
  GenericTimelineAction,
  PlatformMountTimelineAction,
  PlatformUnmountTimelineAction,
  StaticLocationBeginTimelineAction,
  StaticLocationEndTimelineAction
} from '@/utils/configurationInterfaces'
import { dateToDateTimeStringHHMM, sortCriteriaAscending } from '@/utils/dateHelper'
import { getEndLocationTimepointForBeginning } from '@/utils/locationHelper'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { IActionType } from '@/models/ActionType'

export enum LocationTypes {
  staticStart = 'configuration_static_location_begin',
  staticEnd = 'configuration_static_location_end',
  dynamicStart = 'configuration_dynamic_location_begin',
  dynamicEnd = 'configuration_dynamic_location_end',
}

export enum MountingTypes {
  device_mount = 'device_mount',
  platform_mount = 'platform_mount',
  device_unmount = 'device_unmount',
  platform_unmount = 'platform_unmount'
}

export const KIND_OF_ACTION_TYPE_GENERIC_CONFIGURATION_ACTION = 'generic_configuration_action'

export type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: typeof KIND_OF_ACTION_TYPE_GENERIC_CONFIGURATION_ACTION
}

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface ConfigurationsState {
  selectedDate: DateTime | null
  configurations: Configuration[]
  configuration: Configuration | null
  configurationContactRoles: ContactRole[]
  configurationStates: string[]
  projects: string[]
  configurationMountingActions: ConfigurationMountingAction[]
  configurationMountingActionsForDate: ConfigurationsTree | null
  configurationDeviceMountActions: DeviceMountAction[]
  configurationPlatformMountActions: PlatformMountAction[]
  deviceMountAction: DeviceMountAction | null
  platformMountAction: PlatformMountAction | null
  configurationLocationActionTimepoints: ILocationTimepoint[]
  configurationGenericActions: GenericAction[]
  configurationGenericAction: GenericAction | null
  chosenKindOfConfigurationAction: IOptionsForActionType | null
  selectedTimepointItem: ILocationTimepoint| null
  staticLocationAction: StaticLocationAction|null
  dynamicLocationAction: DynamicLocationAction|null
  deviceMountActionsForDynamicLocation: DeviceMountAction []
  selectedLocationDate: DateTime|null
  configurationStaticLocationActions: StaticLocationAction[]
  configurationDynamicLocationActions: DynamicLocationAction[]
  configurationAttachments: Attachment[]
  configurationAttachment: Attachment | null
  configurationCustomFields: CustomTextField[],
  configurationCustomField: CustomTextField | null
  totalPages: number
  pageNumber: number
  pageSize: number
}

const state = (): ConfigurationsState => ({
  selectedDate: DateTime.utc().set({ second: 0, millisecond: 0 }),
  configurations: [],
  configuration: null,
  configurationContactRoles: [],
  configurationStates: [],
  projects: [],
  configurationMountingActions: [],
  configurationMountingActionsForDate: null,
  configurationDeviceMountActions: [],
  configurationPlatformMountActions: [],
  deviceMountAction: null,
  platformMountAction: null,
  configurationLocationActionTimepoints: [],
  configurationGenericActions: [],
  configurationGenericAction: null,
  chosenKindOfConfigurationAction: null,
  selectedTimepointItem: null,
  staticLocationAction: null,
  dynamicLocationAction: null,
  deviceMountActionsForDynamicLocation: [],
  selectedLocationDate: null,
  configurationStaticLocationActions: [],
  configurationDynamicLocationActions: [],
  configurationAttachments: [],
  configurationAttachment: null,
  configurationCustomFields: [],
  configurationCustomField: null,
  totalPages: 1,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0]
})

export type TimelineActionsGetter = ITimelineAction[]

function formatMountActionString (value: ConfigurationMountingAction): string {
  const date = dateToDateTimeStringHHMM(value.timepoint)

  const formatAction = (entity: string, name: string, action: string, timepoint: string): string => `${timepoint} - ${entity} ${name} ${action}`
  switch (value.type) {
    case MountingTypes.device_mount:
      return formatAction('Device', value.attributes.shortName, 'mounted', date)
    case MountingTypes.platform_mount:
      return formatAction('Platform', value.attributes.shortName, 'mounted', date)
    case MountingTypes.device_unmount:
      return formatAction('Device', value.attributes.shortName, 'unmounted', date)
    case MountingTypes.platform_unmount:
      return formatAction('Platform', value.attributes.shortName, 'unmounted', date)
    default:
      return ''
  }
}

const getters: GetterTree<ConfigurationsState, RootState> = {
  timelineActions: (state: ConfigurationsState): ITimelineAction[] => {
    const byDateOldestAndUnmountBeforeMount = (a: ITimelineAction, b: ITimelineAction): number => {
      const result = byDateOldestLast(a, b)
      if (result !== 0) {
        return result
      }
      if (!('isUnmountAction' in a) || !('isUnmountAction' in b)) {
        return result
      }
      // display unmount above mount action when dates are the same
      if (a.isUnmountAction && !b.isUnmountAction) {
        return -1
      }
      // display mount below unmount action when dates are the same
      if (!a.isUnmountAction && b.isUnmountAction) {
        return 1
      }
      return 0
    }

    const result: ITimelineAction[] = []
    const devices = state.configurationDeviceMountActions.map(a => a.device)
    for (const platformMountAction of state.configurationPlatformMountActions) {
      result.push(new PlatformMountTimelineAction(platformMountAction))
      if (platformMountAction.endDate !== null) {
        result.push(new PlatformUnmountTimelineAction(platformMountAction))
      }
    }
    for (const deviceMountAction of state.configurationDeviceMountActions) {
      result.push(new DeviceMountTimelineAction(deviceMountAction))
      if (deviceMountAction.endDate !== null) {
        result.push(new DeviceUnmountTimelineAction(deviceMountAction))
      }
    }

    for (const staticLocationAction of state.configurationStaticLocationActions) {
      result.push(new StaticLocationBeginTimelineAction(staticLocationAction))
      if (staticLocationAction.endDate !== null) {
        result.push(new StaticLocationEndTimelineAction(staticLocationAction))
      }
    }
    for (const dynamicLocationAction of state.configurationDynamicLocationActions) {
      result.push(new DynamicLocationBeginTimelineAction(dynamicLocationAction, devices))
      if (dynamicLocationAction.endDate !== null) {
        result.push(new DynamicLocationEndTimelineAction(dynamicLocationAction))
      }
    }

    for (const genericAction of state.configurationGenericActions) {
      result.push(new GenericTimelineAction(genericAction))
    }

    result.sort(byDateOldestAndUnmountBeforeMount)

    return result
  },
  mountActionDateItems: (state: ConfigurationsState) => {
    return state.configurationMountingActions.map(item => ({
      text: formatMountActionString(item),
      value: item.timepoint
    })).reverse()
  },
  activeDevicesWithPropertiesForDate: (state: ConfigurationsState) => (selectedDate: DateTime | null): Device[] => {
    if (!selectedDate) {
      return []
    }
    if (state.deviceMountActionsForDynamicLocation.length > 0) {
      return state.deviceMountActionsForDynamicLocation.filter((value) => {
        return selectedDate >= value.beginDate && (!value.endDate || selectedDate <= value.endDate) && value.device.properties.length > 0
      }
      ).map((value) => {
        return value.device
      })
    }
    return []
  },
  devicesForDynamicLocation: (state: ConfigurationsState) => {
    if (state.deviceMountActionsForDynamicLocation.length > 0) {
      return state.deviceMountActionsForDynamicLocation.map((value) => {
        return value.device
      })
    }
    return []
  },
  locationActionTimepointsExceptPassedIdAndType: (state: ConfigurationsState) => (id: string | null, type: string | null) => {
    if (id && type) {
      return state.configurationLocationActionTimepoints.filter((item: ILocationTimepoint) => {
        return item.type !== type && item.id !== id
      })
    }
    return state.configurationLocationActionTimepoints
  },
  hasDeviceMountActionsForDynamicLocation: (state: ConfigurationsState) => {
    return state.deviceMountActionsForDynamicLocation.length > 0
  },
  hasMountedDevicesWithProperties: (state: ConfigurationsState) => {
    return state.deviceMountActionsForDynamicLocation.filter((action: DeviceMountAction) => {
      return action.device.properties.length > 0
    }).length > 0
  },
  hasActiveDevicesWithPropertiesForDate: (_state: ConfigurationsState, getters) => (selectedDate: DateTime | null): boolean => {
    const activeDevicesWithProperties = getters.activeDevicesWithPropertiesForDate(selectedDate)
    return activeDevicesWithProperties.length > 0
  },
  activeLocationActionTimepoint: (state: ConfigurationsState): ILocationTimepoint| null => {
    return state.configurationLocationActionTimepoints.find((element: ILocationTimepoint) => {
      if (element.type === LocationTypes.staticEnd || element.type === LocationTypes.dynamicEnd) {
        return false
      }

      const correspondingEndAction = getEndLocationTimepointForBeginning(element, state.configurationLocationActionTimepoints)
      const hasNoEndAction = correspondingEndAction == null

      return (element.type === LocationTypes.staticStart || element.type === LocationTypes.dynamicStart) && hasNoEndAction
    }) ?? null
  },
  hasActiveLocationActionTimepoint: (_state: ConfigurationsState, getters): boolean => {
    if (getters.activeLocationActionTimepoint) {
      return true
    }
    return false
  },
  earliestEndDateOfRelatedDeviceOfDynamicAction: (state: ConfigurationsState) => (action: DynamicLocationAction) => {
    if (state.deviceMountActionsForDynamicLocation.length > 0 && action.beginDate !== null) {
      const deviceMountActionsForDate = state.deviceMountActionsForDynamicLocation.filter((value) => {
        return action.beginDate! >= value.beginDate && (!value.endDate || action.beginDate! <= value.endDate) && value.device.properties.length > 0
      }
      )

      const deviceMountActionsBelongingToDynamicAction = deviceMountActionsForDate.filter((deviceMount: DeviceMountAction) => {
        return deviceMount.endDate !== null && deviceMount.device.properties.some((prop: DeviceProperty) => {
          if (action.x && prop.id === action.x.id) {
            return true
          }
          if (action.y && prop.id === action.y.id) {
            return true
          }
          if (action.z && prop.id === action.z.id) {
            return true
          }
          return false
        })
      })

      // Sort by end date because, earliest first
      deviceMountActionsBelongingToDynamicAction.sort((a: DeviceMountAction, b: DeviceMountAction) => {
        return sortCriteriaAscending(a.endDate!, b.endDate!)
      })

      if (deviceMountActionsBelongingToDynamicAction.length > 0) {
        return deviceMountActionsBelongingToDynamicAction[0].endDate
      }
    }

    return null
  },
  pageSizes: () => {
    return PAGE_SIZES
  }
}

export type ActiveDevicesWithPropertiesForDateGetter = (selectedDate: DateTime | null) => Device[]
export type DevicesForDynamicLocationGetter = Device[]
export type ActiveLocationActionTimepointGetter = ILocationTimepoint | null
export type activeDevicesWithPropertiesForDate = ILocationTimepoint | null
export type HasActiveLocationActionTimepointGetter = boolean
export type HasMountedDevicesWithPropertiesGetter = boolean
export type HasActiveDevicesWithPropertiesForDate = (selectedDate: DateTime | null) => boolean
export type LocationActionTimepointsExceptPassedIdAndTypeTypeGetter = (id: string | null, type: string | null) => ILocationTimepoint[]
export type EarliestEndDateOfRelatedDeviceOfDynamicActionGetter = (action: DynamicLocationAction) => DateTime|null

type IdParamReturnsVoidPromiseAction = (id: string) => Promise<void>

export type SetSelectedDateAction = (params: DateTime | null) => void
export type AddConfigurationContactRoleAction = (params: { configurationId: string, contactRole: ContactRole }) => Promise<void>
export type AddDeviceMountActionAction = (params: { configurationId: string, deviceMountAction: DeviceMountAction }) => Promise<string>
export type AddPlatformMountActionAction = (params: { configurationId: string, platformMountAction: PlatformMountAction }) => Promise<string>
export type DeleteDeviceMountActionAction = IdParamReturnsVoidPromiseAction
export type DeletePlatformMountActionAction = IdParamReturnsVoidPromiseAction
export type AddStaticLocationBeginActionAction = (params: {configurationId: string, staticLocationAction: StaticLocationAction}) => Promise<string>
export type AddStaticLocationEndActionAction = (params: {configurationId: string, staticLocationAction: StaticLocationAction}) => Promise<string>
export type AddDynamicLocationBeginActionAction = (params: {configurationId: string, dynamicLocationAction: DynamicLocationAction}) => Promise<string>
export type AddDynamicLocationEndActionAction = (params: { configurationId: string, dynamicLocationAction: DynamicLocationAction }) => Promise<string>
export type AddConfigurationAttachmentAction = (params: { configurationId: string, attachment: Attachment }) => Promise<Attachment>
export type AddConfigurationGenericAction = (params: { configurationId: string, genericAction: GenericAction }) => Promise<GenericAction>

export type DeleteDynamicLocationActionAction = (id: string) => Promise<void>
export type DeleteStaticLocationActionAction = (id: string) => Promise<void>
export type DeleteConfigurationGenericAction = (genericActionId: string) => Promise<void>

// TODO: load generic or load all
export type LoadConfigurationAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationContactRolesAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationGenericAction = IdParamReturnsVoidPromiseAction
export type LoadDeviceMountActionsAction = IdParamReturnsVoidPromiseAction
export type LoadMountingActionsAction = IdParamReturnsVoidPromiseAction
export type LoadMountingConfigurationForDateAction = (params: { id: string, timepoint: DateTime | null }) => Promise<void>
export type LoadPlatformMountActionsAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationDynamicLocationActionsAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationStaticLocationActionsAction = IdParamReturnsVoidPromiseAction
export type LoadLocationActionTimepointsAction = IdParamReturnsVoidPromiseAction
export type LoadStaticLocationActionAction = IdParamReturnsVoidPromiseAction
export type LoadDynamicLocationActionAction = IdParamReturnsVoidPromiseAction
export type LoadDeviceMountActionsForDynamicLocationAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationAttachmentsAction = (id: string) => Promise<void>
export type LoadConfigurationAttachmentAction = (id: string) => Promise<void>
export type LoadConfigurationCustomFieldsAction = (id: string) => Promise<void>
export type LoadConfigurationCustomFieldAction = (id: string) => Promise<void>
export type LoadProjectsAction = () => Promise<void>

export type DeleteConfigurationAttachmentAction = (attachmentId: string) => Promise<void>
export type LoadConfigurationGenericActionsAction = IdParamReturnsVoidPromiseAction
export type LoadConfigurationGenericActionAction = IdParamReturnsVoidPromiseAction

export type LoadAllConfigurationActionsAction = IdParamReturnsVoidPromiseAction

export type RemoveConfigurationContactRoleAction = (params: { configurationContactRoleId: string }) => Promise<void>
export type ExportAsSensorMLAction = (id: string) => Promise<Blob>
export type GetSensorMLUrlAction = (id: string) => Promise<string>

export type UpdateDeviceMountActionAction = (params: { configurationId: string, deviceMountAction: DeviceMountAction }) => Promise<string>
export type UpdatePlatformMountActionAction = (params: { configurationId: string, platformMountAction: PlatformMountAction }) => Promise<string>
export type ArchiveConfigurationAction = (id: string) => Promise<void>
export type RestoreConfigurationAction = (id: string) => Promise<void>

export type LoadDeviceMountActionAction = IdParamReturnsVoidPromiseAction
export type SetDeviceMountActionAction = (action: DeviceMountAction) => void
export type LoadPlatformMountActionAction = IdParamReturnsVoidPromiseAction
export type SetPlatformMountActionAction = (action: PlatformMountAction) => void
export type UpdateStaticLocationActionAction = (params: {configurationId: string, staticLocationAction: StaticLocationAction}) => Promise<string>
export type UpdateDynamicLocationActionAction = (params: {configurationId: string, dynamicLocationAction: DynamicLocationAction}) => Promise<string>
export type UpdateConfigurationAttachmentAction = (params: { configurationId: string, attachment: Attachment }) => Promise<Attachment>
export type UpdateConfigurationGenericActionAction = (params: {configurationId: string,
  genericAction: GenericAction
}) => Promise<string>

export type SetSelectedTimepointItemAction = (newVal: ILocationTimepoint|null) => void
export type SetSelectedLocationDateAction = (newVal: DateTime | null) => void
export type ReplaceConfigurationInConfigurationsAction = (newConfig: Configuration) => void

export type DeleteConfigurationCustomFieldAction = (customFieldId: string) => Promise<void>
export type AddConfigurationCustomFieldAction = (params: { configurationId: string, configurationCustomField: CustomTextField }) => Promise<CustomTextField>
export type UpdateConfigurationCustomFieldAction = (params: { configurationId: string, configurationCustomField: CustomTextField }) => Promise<CustomTextField>

export type SetChosenKindOfConfigurationActionAction = (newval: IOptionsForActionType | null) => void

export type DownloadAttachmentAction = (attachmentUrl: string) => Promise<Blob>
export type SaveConfigurationAction = (confiuration: Configuration) => Promise<Configuration>
export type CreatePidAction = (id: string | null) => Promise<string>

const actions: ActionTree<ConfigurationsState, RootState> = {
  setSelectedDate ({ commit }: { commit: Commit }, selectedDate: DateTime | null) {
    commit('setSelectedDate', selectedDate)
  },
  async searchConfigurationsPaginated ({
    commit,
    state
  }: { commit: Commit, state: ConfigurationsState }, searchParams: IConfigurationSearchParams) {
    const {
      elements,
      totalCount
    } = await this.$api.configurations
      .setSearchText(searchParams.searchText)
      .setSearchedStates(searchParams.states)
      .setSearchedProjects(searchParams.projects)
      .setSearchPermissionGroups(searchParams.permissionGroups)
      .setSearchedSites(searchParams.sites)
      .setSearchIncludeArchivedConfigurations(searchParams.includeArchivedConfigurations)
      .searchPaginated(
        state.pageNumber,
        state.pageSize,
        {
          includeCreatedBy: true
        }
      )
    commit('setConfigurations', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadConfiguration ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const configuration = await this.$api.configurations.findById(id, {
      includeCreatedBy: true,
      includeUpdatedBy: true
    })
    commit('setConfiguration', configuration)
  },
  async loadConfigurationGenericActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const configurationGenericActions = await this.$api.configurations.findRelatedGenericActions(id)
    commit('setConfigurationGenericActions', configurationGenericActions)
  },
  async loadConfigurationGenericAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const configurationGenericAction = await this.$api.genericConfigurationActions.findById(actionId)
    commit('setConfigurationGenericAction', configurationGenericAction)
  },
  async loadConfigurationContactRoles ({ commit }: { commit: Commit }, id: string) {
    const configurationContactRoles = await this.$api.configurations.findRelatedContactRoles(id)
    commit('setConfigurationContactRoles', configurationContactRoles)
  },
  async loadConfigurationAttachments ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const configurationAttachments = await this.$api.configurations.findRelatedConfigurationAttachments(id)
    commit('setConfigurationAttachments', configurationAttachments)
  },
  async loadConfigurationAttachment ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const configurationAttachment = await this.$api.configurationAttachments.findById(id)
    commit('setConfigurationAttachment', configurationAttachment)
  },
  async addConfigurationAttachment (_, {
    configurationId,
    attachment
  }: { configurationId: string, attachment: Attachment }): Promise<Attachment> {
    return await this.$api.configurationAttachments.add(configurationId, attachment)
  },
  async deleteConfigurationAttachment (_, attachmentId: string): Promise<void> {
    return await this.$api.configurationAttachments.deleteById(attachmentId)
  },
  async updateConfigurationAttachment (_, {
    configurationId,
    attachment
  }: { configurationId: string, attachment: Attachment }): Promise<Attachment> {
    return await this.$api.configurationAttachments.update(configurationId, attachment)
  },
  async loadConfigurationsStates ({ commit }: { commit: Commit }) {
    const configurationStates = await this.$api.configurationStates.findAll()
    commit('setConfigurationStates', configurationStates)
  },
  async loadProjects ({ commit }: { commit: Commit }) {
    const projects = await this.$api.autocomplete.getSuggestions('configuration-projects')
    commit('setProjects', projects)
  },
  async loadStaticLocationAction ({ commit }: {commit: Commit}, id: string): Promise<void> {
    commit('setStaticLocationAction', await this.$api.configurations.staticLocationActionApi.findById(id))
  },
  async loadDynamicLocationAction ({ commit }: {commit: Commit}, id: string): Promise<void> {
    commit('setDynamicLocationAction', await this.$api.configurations.dynamicLocationActionApi.findById(id))
  },
  async loadConfigurationStaticLocationActions ({ commit }: {commit: Commit}, id: string): Promise<void> {
    commit('setConfigurationStaticLocationActions', await this.$api.configurations.findRelatedStaticLocationActions(id))
  },
  async loadConfigurationDynamicLocationActions ({ commit }: {commit: Commit}, id: string): Promise<void> {
    commit('setConfigurationDynamicLocationActions', await this.$api.configurations.findRelatedDynamicLocationActions(id))
  },
  async loadDeviceMountActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    commit('setConfigurationDeviceMountActions', await this.$api.configurations.findRelatedDeviceMountActions(id))
  },
  async downloadAttachment (_, attachmentUrl: string): Promise<Blob> {
    return await this.$api.configurationAttachments.getFile(attachmentUrl)
  },
  getSensorMLUrl (_, id: string): string {
    return this.$api.configurations.getSensorMLUrl(id)
  },
  async exportAsSensorML (_, id: string): Promise<Blob> {
    return await this.$api.configurations.getSensorML(id)
  },
  async loadDeviceMountActionsForDynamicLocation ({ commit }: { commit: Commit }, id: string): Promise<void> {
    commit('setDeviceMountActionsForDynamicLocation', await this.$api.configurations.findRelatedDeviceMountActionsIncludingDeviceInformation(id))
  },
  async loadPlatformMountActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    commit('setConfigurationPlatformMountActions', await this.$api.configurations.findRelatedPlatformMountActions(id))
  },
  async loadMountingActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    commit('setConfigurationMountingActions', await this.$api.configurations.findRelatedMountingActions(id))
  },
  async loadMountingConfigurationForDate ({
    commit,
    dispatch
  }: { commit: Commit, dispatch: Dispatch }, {
    id,
    timepoint
  }: {
    id: string;
    timepoint: DateTime;
  }): Promise<void> {
    if (!timepoint) { return }

    await dispatch('contacts/loadAllContacts', null, { root: true })
    const contacts = this.getters['contacts/searchContacts']
    const mountingActionsByDate = await this.$api.configurations.findRelatedMountingActionsByDate(id, timepoint, contacts)

    commit('setConfigurationMountingActionsForDate', mountingActionsByDate)
  },
  async loadLocationActions ({ dispatch }: { dispatch: Dispatch }, id: string) {
    await dispatch('loadConfigurationStaticLocationBeginActions', id)
    await dispatch('loadConfigurationStaticLocationEndActions', id)
    await dispatch('loadConfigurationDynamicLocationBeginActions', id)
    await dispatch('loadConfigurationDynamicLocationEndActions', id)
  },
  async loadLocationActionTimepoints ({ commit }: {commit: Commit}, id: string) {
    commit('setConfigurationLocationActionTimepoints', await this.$api.configurations.findRelatedLocationActions(id))
  },
  async loadAllConfigurationActions ({ dispatch }: { dispatch: Dispatch }, id: string) {
    await Promise.all([
      dispatch('loadDeviceMountActions', id),
      dispatch('loadPlatformMountActions', id),
      dispatch('loadConfigurationDynamicLocationActions', id),
      dispatch('loadConfigurationStaticLocationActions', id),
      dispatch('loadConfigurationGenericActions', id)
    ])
  },
  async deleteConfiguration (_context, id: string) {
    await this.$api.configurations.deleteById(id)
  },
  async archiveConfiguration (_, id: string): Promise<void> {
    await this.$api.configurations.archiveById(id)
  },
  async restoreConfiguration (_, id: string): Promise<void> {
    await this.$api.configurations.restoreById(id)
  },
  saveConfiguration (_context, configuration: Configuration): Promise<Configuration> {
    return this.$api.configurations.save(configuration)
  },
  createPid (_, id: string | null): Promise<string> {
    return this.$api.pids.create(id, 'configuration')
  },
  addConfigurationContactRole (_context, {
    configurationId,
    contactRole
  }: { configurationId: string, contactRole: ContactRole }): Promise<string> {
    return this.$api.configurations.addContact(configurationId, contactRole)
  },
  removeConfigurationContactRole (_context, {
    configurationContactRoleId
  }: { configurationContactRoleId: string }): Promise<void> {
    return this.$api.configurations.removeContact(configurationContactRoleId)
  },
  async loadDeviceMountAction ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const action = await this.$api.configurations.deviceMountActionApi.findById(id)
    commit('setDeviceMountAction', action)
  },
  setDeviceMountAction ({ commit }: { commit: Commit }, action: DeviceMountAction): void {
    commit('setDeviceMountAction', action)
  },
  addDeviceMountAction (
    _context,
    {
      configurationId,
      deviceMountAction
    }: { configurationId: string, deviceMountAction: DeviceMountAction }
  ): Promise<string> {
    return this.$api.configurations.deviceMountActionApi.add(configurationId, deviceMountAction)
  },
  addPlatformMountAction (_context,
    {
      configurationId,
      platformMountAction
    }: { configurationId: string, platformMountAction: PlatformMountAction }
  ): Promise<string> {
    return this.$api.configurations.platformMountActionApi.add(configurationId, platformMountAction)
  },
  deleteDeviceMountAction (_, actionId: string): Promise<void> {
    return this.$api.configurations.deviceMountActionApi.deleteById(actionId)
  },
  deletePlatformMountAction (_, actionId: string): Promise<void> {
    return this.$api.configurations.platformMountActionApi.deleteById(actionId)
  },
  addConfigurationGenericAction (_, {
    configurationId,
    genericAction
  }: { configurationId: string, genericAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericConfigurationActions.add(configurationId, genericAction)
  },
  updateConfigurationGenericAction (_, {
    configurationId,
    genericAction
  }: { configurationId: string, genericAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericConfigurationActions.update(configurationId, genericAction)
  },
  deleteConfigurationGenericAction (_, genericActionId: string): Promise<void> {
    return this.$api.genericConfigurationActions.deleteById(genericActionId)
  },
  updateDeviceMountAction (
    _context,
    {
      configurationId,
      deviceMountAction
    }: { configurationId: string, deviceMountAction: DeviceMountAction }
  ): Promise<string> {
    return this.$api.configurations.deviceMountActionApi.update(configurationId, deviceMountAction)
  },
  async loadPlatformMountAction ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const action = await this.$api.configurations.platformMountActionApi.findById(id)
    commit('setPlatformMountAction', action)
  },
  setPlatformMountAction ({ commit }: { commit: Commit }, action: PlatformMountAction): void {
    commit('setPlatformMountAction', action)
  },
  updatePlatformMountAction (_context,
    {
      configurationId,
      platformMountAction
    }: { configurationId: string, platformMountAction: PlatformMountAction }
  ): Promise<string> {
    return this.$api.configurations.platformMountActionApi.update(configurationId, platformMountAction)
  },
  addStaticLocationBeginAction (_context, {
    configurationId,
    staticLocationAction
  }: { configurationId: string, staticLocationAction: StaticLocationAction }) {
    return this.$api.configurations.staticLocationActionApi.add(configurationId, staticLocationAction)
  },
  addStaticLocationEndAction (_context, {
    configurationId,
    staticLocationAction
  }: { configurationId: string, staticLocationAction: StaticLocationAction }) {
    return _context.dispatch('updateStaticLocationAction', {
      configurationId,
      staticLocationAction
    })
  },
  updateStaticLocationAction (_context, {
    configurationId,
    staticLocationAction
  }: { configurationId: string, staticLocationAction: StaticLocationAction }) {
    return this.$api.configurations.staticLocationActionApi.update(configurationId, staticLocationAction)
  },
  deleteStaticLocationAction (_context, id: string) {
    return this.$api.configurations.staticLocationActionApi.deleteById(id)
  },
  addDynamicLocationBeginAction (_context, {
    configurationId,
    dynamicLocationAction
  }: { configurationId: string, dynamicLocationAction: DynamicLocationAction }) {
    return this.$api.configurations.dynamicLocationActionApi.add(configurationId, dynamicLocationAction)
  },
  addDynamicLocationEndAction (_context, {
    configurationId,
    dynamicLocationAction
  }: { configurationId: string, dynamicLocationAction: DynamicLocationAction }) {
    return _context.dispatch('updateDynamicLocationAction', { configurationId, dynamicLocationAction })
  },
  updateDynamicLocationAction (_context, {
    configurationId,
    dynamicLocationAction
  }: { configurationId: string, dynamicLocationAction: DynamicLocationAction }) {
    return this.$api.configurations.dynamicLocationActionApi.update(configurationId, dynamicLocationAction)
  },
  deleteDynamicLocationAction (_context, id: string) {
    return this.$api.configurations.dynamicLocationActionApi.deleteById(id)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  setSelectedTimepointItem ({ commit }: { commit: Commit }, newval: ILocationTimepoint|null) {
    commit('setSelectedTimepointItem', newval)
  },
  setSelectedLocationDate ({ commit }: { commit: Commit }, newval: DateTime|null) {
    commit('setSelectedLocationDate', newval)
  },
  replaceConfigurationInConfigurations ({ commit, state }: {commit: Commit, state: ConfigurationsState}, newConfiguration: Configuration) {
    const result = []
    for (const oldConfiguration of state.configurations) {
      if (oldConfiguration.id !== newConfiguration.id) {
        result.push(oldConfiguration)
      } else {
        result.push(newConfiguration)
      }
    }
    commit('setConfigurations', result)
  },
  setChosenKindOfConfigurationAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfConfigurationAction', newval)
  },
  async loadConfigurationCustomFields ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const configurationCustomFields = await this.$api.configurations.findRelatedConfigurationCustomFields(id)
    commit('setConfigurationCustomFields', configurationCustomFields)
  },
  async loadConfigurationCustomField ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const configurationCustomField = await this.$api.configurationCustomfields.findById(id)
    commit('setConfigurationCustomField', configurationCustomField)
  },
  deleteConfigurationCustomField (_, customFieldId: string): Promise<void> {
    return this.$api.configurationCustomfields.deleteById(customFieldId)
  },
  addConfigurationCustomField (_, {
    configurationId,
    configurationCustomField
  }: { configurationId: string, configurationCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.configurationCustomfields.add(configurationId, configurationCustomField)
  },
  updateConfigurationCustomField (_, {
    configurationId,
    configurationCustomField
  }: { configurationId: string, configurationCustomField: CustomTextField }): Promise<CustomTextField> {
    return this.$api.configurationCustomfields.update(configurationId, configurationCustomField)
  }
}

const mutations = {
  setSelectedDate (state: ConfigurationsState, selectedDate: DateTime | null) {
    state.selectedDate = selectedDate
  },
  setConfigurations (state: ConfigurationsState, configurations: Configuration[]) {
    state.configurations = configurations
  },
  setConfiguration (state: ConfigurationsState, configuration: Configuration) {
    state.configuration = configuration
  },
  setConfigurationContactRoles (state: ConfigurationsState, configurationContactRoles: ContactRole[]) {
    state.configurationContactRoles = configurationContactRoles
  },
  setConfigurationAttachments (state: ConfigurationsState, attachments: Attachment[]) {
    state.configurationAttachments = attachments
  },
  setConfigurationAttachment (state: ConfigurationsState, attachment: Attachment) {
    state.configurationAttachment = attachment
  },
  setConfigurationStates (state: ConfigurationsState, configurationStates: string[]) {
    state.configurationStates = configurationStates
  },
  setProjects (state: ConfigurationsState, projects: string[]) {
    state.projects = projects
  },
  setPageNumber (state: ConfigurationsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setPageSize (state: ConfigurationsState, newPageSize: number) {
    state.pageSize = newPageSize
  },
  setTotalPages (state: ConfigurationsState, count: number) {
    state.totalPages = count
  },
  setConfigurationMountingActions (state: ConfigurationsState, configurationMountingActions: []) {
    state.configurationMountingActions = configurationMountingActions
  },
  setConfigurationLocationActionTimepoints (state: ConfigurationsState, configurationLocationActionTimepoints: []) {
    state.configurationLocationActionTimepoints = configurationLocationActionTimepoints
  },
  setSelectedTimepointItem (state: ConfigurationsState, newVal: ILocationTimepoint|null) {
    state.selectedTimepointItem = newVal
  },
  setStaticLocationAction (state: ConfigurationsState, newVal: StaticLocationAction|null) {
    state.staticLocationAction = newVal
  },
  setDynamicLocationAction (state: ConfigurationsState, newVal: DynamicLocationAction|null) {
    state.dynamicLocationAction = newVal
  },
  setConfigurationStaticLocationActions (state: ConfigurationsState, newVal: StaticLocationAction[]) {
    state.configurationStaticLocationActions = newVal
  },
  setConfigurationDynamicLocationActions (state: ConfigurationsState, newVal: DynamicLocationAction[]) {
    state.configurationDynamicLocationActions = newVal
  },
  setConfigurationMountingActionsForDate (state: ConfigurationsState, configurationMountingActionsForDate: ConfigurationsTree) {
    state.configurationMountingActionsForDate = configurationMountingActionsForDate
  },
  setConfigurationDeviceMountActions (state: ConfigurationsState, configurationDeviceMountActions: []) {
    state.configurationDeviceMountActions = configurationDeviceMountActions
  },
  setConfigurationPlatformMountActions (state: ConfigurationsState, configurationPlatformMountActions: []) {
    state.configurationPlatformMountActions = configurationPlatformMountActions
  },
  setDeviceMountAction (state: ConfigurationsState, deviceMountAction: DeviceMountAction | null) {
    state.deviceMountAction = deviceMountAction
  },
  setPlatformMountAction (state: ConfigurationsState, platformMountAction: PlatformMountAction | null) {
    state.platformMountAction = platformMountAction
  },
  setConfigurationGenericActions (state: ConfigurationsState, configurationGenericActions: []) {
    state.configurationGenericActions = configurationGenericActions
  },
  setConfigurationGenericAction (state: ConfigurationsState, configurationGenericAction: GenericAction) {
    state.configurationGenericAction = configurationGenericAction
  },
  setDeviceMountActionsForDynamicLocation (state: ConfigurationsState, deviceMountActionsForDynamicLocation: []) {
    state.deviceMountActionsForDynamicLocation = deviceMountActionsForDynamicLocation
  },
  setSelectedLocationDate (state: ConfigurationsState, newVal: DateTime|null) {
    state.selectedLocationDate = newVal
  },
  setChosenKindOfConfigurationAction (state: ConfigurationsState, newVal: IOptionsForActionType | null) {
    state.chosenKindOfConfigurationAction = newVal
  },
  setConfigurationCustomFields (state: ConfigurationsState, configurationCustomFields: CustomTextField[]) {
    state.configurationCustomFields = configurationCustomFields
  },
  setConfigurationCustomField (state: ConfigurationsState, configurationCustomField: CustomTextField) {
    state.configurationCustomField = configurationCustomField
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
