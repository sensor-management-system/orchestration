/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
import { Commit, Dispatch } from 'vuex/types'

import { DateTime } from 'luxon'
import { Configuration } from '@/models/Configuration'
import { Project } from '@/models/Project'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { ContactRole } from '@/models/ContactRole'
import {
  DeviceMountTimelineAction,
  DeviceUnmountTimelineAction,
  DynamicLocationBeginTimelineAction,
  DynamicLocationEndTimelineAction,
  IActionDateWithTextItem,
  ITimelineAction,
  PlatformMountTimelineAction,
  PlatformUnmountTimelineAction,
  StaticLocationBeginTimelineAction,
  StaticLocationEndTimelineAction
} from '@/utils/configurationInterfaces'

import { byDateOldestLast } from '@/modelUtils/mountHelpers'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { Api } from '@/services/Api'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { mockCurrentConfiguration, mockMountingActions } from '@/utils/mockHelper'

export enum LocationTypes {
  staticStart = 'staticStart',
  staticEnd = 'staticEnd',
  dynamicStart = 'dynamicStart',
  dynamicEnd = 'dynamicEnd',
}

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface ConfigurationsState {
  configurations: Configuration[]
  configuration: Configuration | null,
  configurationContactRoles: ContactRole[]
  configurationStates: string[]
  projects: Project[],
  configurationStaticLocationBeginActions: StaticLocationBeginAction[],
  configurationStaticLocationEndActions: StaticLocationEndAction[],
  configurationDynamicLocationBeginActions: DynamicLocationBeginAction[],
  configurationDynamicLocationEndActions: DynamicLocationEndAction[],
  configurationMountingActions: []
  totalPages: number
  pageNumber: number
  pageSize: number
}

const state = () => ({
  configurations: [],
  configuration: null,
  configurationContactRoles: [],
  configurationStates: [],
  projects: [],
  configurationStaticLocationBeginActions: [],
  configurationStaticLocationEndActions: [],
  configurationDynamicLocationBeginActions: [],
  configurationDynamicLocationEndActions: [],
  configurationMountingActions: [],
  totalPages: 1,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0]
})

const getters = {
  projectNames: (state: ConfigurationsState) => {
    return state.projects.map((p: Project) => p.name)
  },
  timelineActions: (state: ConfigurationsState) => { // Todo überlegen, ob das man das eventuell anders macht
    const result: ITimelineAction[] = []

    if (state.configuration !== null) {
      const devices = state.configuration.deviceMountActions.map(a => a.device)
      for (const platformMountAction of state.configuration.platformMountActions) {
        result.push(new PlatformMountTimelineAction(platformMountAction))
      }
      for (const deviceMountAction of state.configuration.deviceMountActions) {
        result.push(new DeviceMountTimelineAction(deviceMountAction))
      }
      for (const platformUnmountAction of state.configuration.platformUnmountActions) {
        result.push(new PlatformUnmountTimelineAction(platformUnmountAction))
      }
      for (const deviceUnmountAction of state.configuration.deviceUnmountActions) {
        result.push(new DeviceUnmountTimelineAction(deviceUnmountAction))
      }
      for (const action of state.configuration.staticLocationBeginActions) {
        result.push(new StaticLocationBeginTimelineAction(action))
      }
      for (const action of state.configuration.staticLocationEndActions) {
        result.push(new StaticLocationEndTimelineAction(action))
      }
      for (const action of state.configuration.dynamicLocationBeginActions) {
        result.push(new DynamicLocationBeginTimelineAction(action, devices))
      }
      for (const action of state.configuration.dynamicLocationEndActions) {
        result.push(new DynamicLocationEndTimelineAction(action))
      }
      result.sort(byDateOldestLast)
    }
    return result
  },
  // mountingActionsDates: (state: ConfigurationsState) => {
  //   let result: IActionDateWithTextItem[] = []
  //
  //   if (state.configuration) {
  //     const datesWithTexts: IActionDateWithTextItem[] = []
  //     for (const platformMountAction of state.configurationPlatformMountActions) {
  //       datesWithTexts.push({
  //         date: platformMountAction.date,
  //         text: dateToDateTimeStringHHMM(platformMountAction.date) + ' - ' + 'Mount ' + platformMountAction.platform.shortName
  //       })
  //     }
  //     for (const platformUnmountAction of state.configurationPlatformUnmountActions) {
  //       datesWithTexts.push({
  //         date: platformUnmountAction.date,
  //         text: dateToDateTimeStringHHMM(platformUnmountAction.date) + ' - ' + 'Unmount ' + platformUnmountAction.platform.shortName
  //       })
  //     }
  //     for (const deviceMountAction of state.configurationDeviceMountActions) {
  //       datesWithTexts.push({
  //         date: deviceMountAction.date,
  //         text: dateToDateTimeStringHHMM(deviceMountAction.date) + ' - ' + 'Mount ' + deviceMountAction.device.shortName
  //       })
  //     }
  //     for (const deviceUnmountAction of state.configurationDeviceUnmountActions) {
  //       datesWithTexts.push({
  //         date: deviceUnmountAction.date,
  //         text: dateToDateTimeStringHHMM(deviceUnmountAction.date) + ' - ' + 'Unmount ' + deviceUnmountAction.device.shortName
  //       })
  //     }
  //     datesWithTexts.sort((a, b) => {
  //       if (a.date < b.date) {
  //         return -1
  //       }
  //       if (a.date > b.date) {
  //         return 1
  //       }
  //       return 0
  //     })
  //     // Todo: Anmerknug: ich hab das grouping nicht eingebaut
  //     result = datesWithTexts
  //   }
  //   return result
  // },
  locationActionsDates: (state: ConfigurationsState) => {
    let result: IActionDateWithTextItem[] = []

    if (state.configuration) {
      const datesWithTexts = []
      for (const staticLocationBeginAction of state.configuration.staticLocationBeginActions) {
        if (staticLocationBeginAction.beginDate) {
          datesWithTexts.push({
            type: LocationTypes.staticStart,
            value: staticLocationBeginAction,
            date: staticLocationBeginAction.beginDate,
            text: dateToDateTimeStringHHMM(staticLocationBeginAction.beginDate) + ' - ' + 'Static location begin'
          })
        }
      }
      for (const staticLocationEndAction of state.configuration.staticLocationEndActions) {
        if (staticLocationEndAction.endDate) {
          datesWithTexts.push({
            type: LocationTypes.staticEnd,
            value: staticLocationEndAction,
            date: staticLocationEndAction.endDate,
            text: dateToDateTimeStringHHMM(staticLocationEndAction.endDate) + ' - ' + 'Static location end'
          })
        }
      }
      for (const dynamicLocationBeginAction of state.configuration.dynamicLocationBeginActions) {
        if (dynamicLocationBeginAction.beginDate) {
          datesWithTexts.push({
            type: LocationTypes.dynamicStart,
            value: dynamicLocationBeginAction,
            date: dynamicLocationBeginAction.beginDate,
            text: dateToDateTimeStringHHMM(dynamicLocationBeginAction.beginDate) + ' - ' + 'Dynamic location begin'
          })
        }
      }
      for (const dynamicLocationEndAction of state.configuration.dynamicLocationEndActions) {
        if (dynamicLocationEndAction.endDate) {
          datesWithTexts.push({
            type: LocationTypes.dynamicEnd,
            value: dynamicLocationEndAction,
            date: dynamicLocationEndAction.endDate,
            text: dateToDateTimeStringHHMM(dynamicLocationEndAction.endDate) + ' - ' + 'Dynamic location end'
          })
        }
      }
      datesWithTexts.sort((a, b) => {
        if (a.date < b.date) {
          return -1
        }
        if (a.date > b.date) {
          return 1
        }
        return 0
      })
      // Todo: Anmerknug: ich hab das grouping nicht eingebaut

      result = datesWithTexts
    }
    return result
  },
  pageSizes: () => {
    return PAGE_SIZES
  }
}

export type LoadConfigurationContactRolesAction = (id: string) => Promise<void>
export type AddConfigurationContactRoleAction = (params: { configurationId: string, contactRole: ContactRole }) => Promise<void>
export type RemoveConfigurationContactRoleAction = (params: { configurationContactRoleId: string }) => Promise<void>

// @ts-ignore
const actions: {
  [key: string]: any;
  $api: Api
} = {
  async searchConfigurationsPaginated ({
    commit,
    state
  }: { commit: Commit, state: ConfigurationsState }, searchParams: IConfigurationSearchParams) {
    const {
      elements,
      totalCount
    } = await this.$api.configurations
      .setSearchText(searchParams.searchText)
      .setSearchedProjects(searchParams.projects)
      .setSearchedStates(searchParams.states)
      .setSearchPermissionGroups(searchParams.permissionGroups)
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
  async loadConfiguration ({ commit }: { commit: Commit }, id: string) {
    const configuration = await this.$api.configurations.findById(id, { includeCreatedBy: true, includeUpdatedBy: true })
    commit('setConfiguration', configuration)
  },
  async loadConfigurationContactRoles ({ commit }: { commit: Commit }, id: string) {
    const configurationContactRoles = await this.$api.configurations.findRelatedContactRoles(id)
    commit('setConfigurationContactRoles', configurationContactRoles)
  },
  async loadConfigurationsStates ({ commit }: { commit: Commit }) {
    const configurationStates = await this.$api.configurationStates.findAll()
    commit('setConfigurationStates', configurationStates)
  },
  async loadProjects ({ commit }: { commit: Commit }) {
    const projects = await this.$api.projects.findAll()
    commit('setProjects', projects)
  },
  async loadConfigurationStaticLocationBeginActions ({ commit }: { commit: Commit }, id: string) {
    commit('setConfigurationStaticLocationBeginActions', await this.$api.configurations.findRelatedStaticLocationBeginActions(id))
  },
  async loadConfigurationStaticLocationEndActions ({ commit }: { commit: Commit }, id: string) {
    commit('setConfigurationStaticLocationEndActions', await this.$api.configurations.findRelatedStaticLocationEndActions(id))
  },
  async loadConfigurationDynamicLocationBeginActions ({ commit }: { commit: Commit }, id: string) {
    commit('setConfigurationDynamicLocationBeginActions', await this.$api.configurations.findRelatedDynamicLocationBeginActions(id))
  },
  async loadConfigurationDynamicLocationEndActions ({ commit }: { commit: Commit }, id: string) {
    commit('setConfigurationDynamicLocationEndActions', await this.$api.configurations.findRelatedDynamicLocationEndActions(id))
  },
  async loadMountingActions ({ commit }: {commit: Commit}, id: string) {
    // Todo currently mock

    // request to controller via $api
    // /backend/api/v1/controller/configurations/<configuration-id>/mounting-action-timepoints

    // Todo import of mockHelper.ts
    commit('setConfigurationMountingActions', mockMountingActions)
  },
  async getMountingConfigurationForDate ({ commit }: {commit: Commit}, id: string, timepoint: DateTime) {
    // Todo currently mock
    // request to controller via $api
    /// backend/api/v1/controller/configurations/<configuration-id>/mounting-actions?timepoint=<time-point>

    // Todo import of mockHelper.ts
    return mockCurrentConfiguration
  },
  async loadLocationActions ({ dispatch }: {dispatch: Dispatch}, id: string) {
    await dispatch('loadConfigurationStaticLocationBeginActions', id)
    await dispatch('loadConfigurationStaticLocationEndActions', id)
    await dispatch('loadConfigurationDynamicLocationBeginActions', id)
    await dispatch('loadConfigurationDynamicLocationEndActions', id)
  },
  async deleteConfiguration ({ _commit }: { _commit: Commit }, id: string) {
    await this.$api.configurations.deleteById(id)
  },
  saveConfiguration ({ _commit }: { _commit: Commit }, configuration: Configuration): Promise<Configuration> {
    return this.$api.configurations.save(configuration)
  },
  addConfigurationContactRole ({ _commit }: { _commit: Commit }, {
    configurationId,
    contactRole
  }: { configurationId: string, contactRole: ContactRole }): Promise<string> {
    return this.$api.configurations.addContact(configurationId, contactRole)
  },
  removeConfigurationContactRole ({ _commit }: { _commit: Commit }, {
    configurationContactRoleId
  }: { configurationContactRoleId: string }): Promise<void> {
    return this.$api.configurations.removeContact(configurationContactRoleId)
  },
  addDeviceMountAction (
    { _commit }: { _commit: Commit },
    {
      configurationId,
      deviceMountAction
    }: { configurationId: string, deviceMountAction: DeviceMountAction }
  ): Promise<string> {
    return this.$api.configurations.deviceMountActionApi.add(configurationId, deviceMountAction)
  },
  addDeviceUnMountAction ({ _commit }: { _commit: Commit },
    {
      configurationId,
      deviceUnMountAction
    }: { configurationId: string, deviceUnMountAction: DeviceUnmountAction }
  ) {
    return this.$api.configurations.deviceUnmountActionApi.add(configurationId, deviceUnMountAction)
  },
  addPlatformMountAction ({ _commit }: { _commit: Commit },
    {
      configurationId,
      platformMountAction
    }: { configurationId: string, platformMountAction: PlatformMountAction }
  ): Promise<string> {
    return this.$api.configurations.platformMountActionApi.add(configurationId, platformMountAction)
  },
  addPlatformUnMountAction ({ _commit }: { _commit: Commit },
    {
      configurationId,
      platformUnMountAction
    }: { configurationId: string, platformUnMountAction: PlatformUnmountAction }
  ) {
    return this.$api.configurations.platformUnmountActionApi.add(configurationId, platformUnMountAction)
  },
  addStaticLocationBeginAction ({ _commit }: { _commit: Commit }, {
    configurationId,
    staticLocationBeginAction
  }: { configurationId: string, staticLocationBeginAction: StaticLocationBeginAction }) {
    return this.$api.configurations.staticLocationBeginActionApi.add(configurationId, staticLocationBeginAction)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  }
}

const mutations = {
  setConfigurations (state: ConfigurationsState, configurations: Configuration[]) {
    state.configurations = configurations
  },
  setConfiguration (state: ConfigurationsState, configuration: Configuration) {
    state.configuration = configuration
  },
  setConfigurationContactRoles (state: ConfigurationsState, configurationContactRoles: ContactRole[]) {
    state.configurationContactRoles = configurationContactRoles
  },
  setConfigurationStates (state: ConfigurationsState, configurationStates: string[]) {
    state.configurationStates = configurationStates
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
  setProjects (state: ConfigurationsState, projects: Project[]) {
    state.projects = projects
  },
  setConfigurationStaticLocationBeginActions (state: ConfigurationsState, staticLocationBeginActions: StaticLocationBeginAction[]) {
    state.configurationStaticLocationBeginActions = staticLocationBeginActions
  },
  setConfigurationStaticLocationEndActions (state: ConfigurationsState, staticLocationEndActions: StaticLocationEndAction[]) {
    state.configurationStaticLocationEndActions = staticLocationEndActions
  },
  setConfigurationDynamicLocationBeginActions (state: ConfigurationsState, dynamicLocationBeginActions: DynamicLocationBeginAction[]) {
    state.configurationDynamicLocationBeginActions = dynamicLocationBeginActions
  },
  setConfigurationDynamicLocationEndActions (state: ConfigurationsState, dynamicLocationEndActions: DynamicLocationEndAction[]) {
    state.configurationDynamicLocationEndActions = dynamicLocationEndActions
  },
  setConfigurationMountingActions (state: ConfigurationsState, configurationMountingActions: []) {
    state.configurationMountingActions = configurationMountingActions
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
