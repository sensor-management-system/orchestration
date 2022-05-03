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
import { Commit } from 'vuex/types'

import { Configuration } from '@/models/Configuration'
import { Project } from '@/models/Project'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { Contact } from '@/models/Contact'
import {
  DeviceMountTimelineAction, DeviceUnmountTimelineAction,
  DynamicLocationBeginTimelineAction,
  DynamicLocationEndTimelineAction, IActionDateWithTextItem,
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

export enum LocationTypes {
  staticStart='staticStart',
  staticEnd='staticEnd',
  dynamicStart='dynamicStart',
  dynamicEnd='dynamicEnd',
}

export interface configurationsState {
  configurations: Configuration[]
  configuration: Configuration | null,
  configurationContacts: Contact[]
  configurationStates: string[]
  projects: Project[]
  totalPages: number
  pageNumber: number
  pageSize: number
}

const state = {
  configurations: [],
  configuration: null,
  configurationContacts: [],
  configurationStates: [],
  projects: [],
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}

const getters = {
  projectNames: (state: configurationsState) => {
    return state.projects.map((p: Project) => p.name)
  },
  timelineActions: (state: configurationsState) => { // Todo überlegen, ob das man das eventuell anders macht
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
  mountingActionsDates: (state: configurationsState) => {
    let result: IActionDateWithTextItem[] = []

    if (state.configuration) {
      const datesWithTexts: IActionDateWithTextItem[] = []
      for (const platformMountAction of state.configuration.platformMountActions) {
        datesWithTexts.push({
          date: platformMountAction.date,
          text: dateToDateTimeStringHHMM(platformMountAction.date) + ' - ' + 'Mount ' + platformMountAction.platform.shortName
        })
      }
      for (const platformUnmountAction of state.configuration.platformUnmountActions) {
        datesWithTexts.push({
          date: platformUnmountAction.date,
          text: dateToDateTimeStringHHMM(platformUnmountAction.date) + ' - ' + 'Unmount ' + platformUnmountAction.platform.shortName
        })
      }
      for (const deviceMountAction of state.configuration.deviceMountActions) {
        datesWithTexts.push({
          date: deviceMountAction.date,
          text: dateToDateTimeStringHHMM(deviceMountAction.date) + ' - ' + 'Mount ' + deviceMountAction.device.shortName
        })
      }
      for (const deviceUnmountAction of state.configuration.deviceUnmountActions) {
        datesWithTexts.push({
          date: deviceUnmountAction.date,
          text: dateToDateTimeStringHHMM(deviceUnmountAction.date) + ' - ' + 'Unmount ' + deviceUnmountAction.device.shortName
        })
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
  locationActionsDates: (state: configurationsState) => {
    let result:{type:string,value:}[] = []

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
  }
}

const actions = {
  async searchConfigurationsPaginated ({
    commit,
    state
  }: { commit: Commit, state: configurationsState }, searchParams: IConfigurationSearchParams) {
    // @ts-ignore
    const {
      elements,
      totalCount
    } = await this.$api.configurations
      .setSearchText(searchParams.searchText)
      .setSearchedProjects(searchParams.projects)
      .setSearchedStates(searchParams.states)
      .searchPaginated(state.pageNumber, state.pageSize)
    commit('setConfigurations', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadConfiguration ({ commit }: { commit: Commit }, id: string) {
    const configuration = await this.$api.configurations.findById(id)
    commit('setConfiguration', configuration)
  },
  async loadConfigurationContacts ({ commit }: { commit: Commit }, id: string) {
    const configurationContacts = await this.$api.configurations.findRelatedContacts(id)
    commit('setConfigurationContacts', configurationContacts)
  },
  async loadConfigurationsStates ({ commit }: { commit: Commit }) {
    // @ts-ignore
    const configurationStates = await this.$api.configurationStates.findAll()
    commit('setConfigurationStates', configurationStates)
  },
  async loadProjects ({ commit }: { commit: Commit }) {
    // @ts-ignore
    const projects = await this.$api.projects.findAll()
    commit('setProjects', projects)
  },
  async deleteConfiguration ({ _commit }: { _commit: Commit }, id: string) {
    await this.$api.configurations.deleteById(id)
  },
  saveConfiguration ({ _commit }: { _commit: Commit }, configuration: Configuration): Promise<Configuration> {
    return this.$api.configurations.save(configuration)
  },
  addConfigurationContact ({ _commit }: { _commit: Commit }, {
    configurationId,
    contactId
  }: { configurationId: string, contactId: string }): Promise<void> {
    return this.$api.configurations.addContact(configurationId, contactId)
  },
  removeConfigurationContact ({ _commit }: { _commit: Commit }, {
    configurationId,
    contactId
  }: { configurationId: string, contactId: string }): Promise<void> {
    return this.$api.configurations.removeContact(configurationId, contactId)
  },
  addDeviceMountAction (
    { _commit }: { _commit: Commit },
    {
      configurationId,
      deviceMountAction
    }: { configurationId: string, deviceMountAction: DeviceMountAction }
  ): Promise<void> {
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
  ): Promise<void> {
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
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  }
}

const mutations = {
  setConfigurations (state: configurationsState, configurations: Configuration[]) {
    state.configurations = configurations
  },
  setConfiguration (state: configurationsState, configuration: Configuration) {
    state.configuration = configuration
  },
  setConfigurationContacts (state: configurationsState, configurationContacts: Contact[]) {
    state.configurationContacts = configurationContacts
  },
  setConfigurationStates (state: configurationsState, configurationStates: string[]) {
    state.configurationStates = configurationStates
  },
  setPageNumber (state: configurationsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: configurationsState, count: number) {
    state.totalPages = count
  },
  setProjects (state: configurationsState, projects: Project[]) {
    state.projects = projects
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
