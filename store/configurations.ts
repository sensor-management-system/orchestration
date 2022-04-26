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
import { ActionContext, Commit } from 'vuex/types'
import { DateTime } from 'luxon'

import { Configuration } from '@/models/Configuration'
import { Project } from '@/models/Project'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'

export interface configurationsState {
  configurations: Configuration[]
  configuration: Configuration|null,
  configurationStates: string[]
  totalPages: number
  pageNumber: number
  pageSize: number
  // projects: Project[],
  // configurationStates: string[]
  // configurationEditDate: DateTime
}

const state={
  configurations:[],
  configuration:null,
  configurationStates:[],
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}

const getters={}

const actions={
  async searchConfigurationsPaginated({commit,state}:{commit:Commit,state:configurationsState},searchParams:IConfigurationSearchParams){
    // @ts-ignore
    const { elements, totalCount } = await this.$api.configurations
      .setSearchText(searchParams.searchText)
      .setSearchedProjects(searchParams.projects)
      .setSearchedStates(searchParams.states)
      .searchPaginated(state.pageNumber,state.pageSize)
    commit('setConfigurations',elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadConfiguration({ commit }: { commit: Commit },id:number){

  },
  async loadConfigurationsStates ({ commit }: { commit: Commit }) {
    // @ts-ignore
    const configurationStates = await this.$api.configurationStates.findAll()
    commit('setConfigurationStates', configurationStates)
  },
  async deleteConfiguration({ commit }: { commit: Commit }, id: number){
    await this.$api.configurations.deleteById(id)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
}

const mutations={
  setConfigurations(state:configurationsState,configurations:Configuration[]){
    state.configurations=configurations
  },
  setConfiguration(state:configurationsState,configuration:Configuration){
    state.configuration=configuration
  },
  setConfigurationStates(state:configurationsState,configurationStates:string[]){
    state.configurationStates=configurationStates;
  },
  setPageNumber (state: configurationsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: configurationsState, count: number) {
    state.totalPages = count
  }
}
// export const state = (): ConfigurationsStoreState => {
//   return {
//     configuration: new Configuration(),
//     projects: [],
//     configurationStates: [],
//     configurationEditDate: DateTime.utc()
//   }
// }
//
// export const mutations = {
//   setConfiguration (state: ConfigurationsStoreState, configuration: Configuration) {
//     state.configuration = configuration
//   },
//   setProjects (state: ConfigurationsStoreState, projects: Project[]) {
//     state.projects = projects
//   },
//   setConfigurationsStates (state: ConfigurationsStoreState, configurationStates: string[]) {
//     state.configurationStates = configurationStates
//   },
//   setConfigurationEditDate (state: ConfigurationsStoreState, configurationEditDate: DateTime) {
//     state.configurationEditDate = configurationEditDate
//   }
// }
//
// export const actions = {
//   async loadProjects (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
//     // @ts-ignore
//     const projects = await this.$api.projects.findAll()
//     context.commit('setProjects', projects)
//   },
//   async loadConfigurationsStates (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
//     // @ts-ignore
//     const configurationStates = await this.$api.configurationStates.findAll()
//     context.commit('setConfigurationsStates', configurationStates)
//   },
//   async loadConfigurationById (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>, id: string) {
//     const oldConfigurationId = context.state.configuration?.id
//     // @ts-ignore
//     const configuration = await this.$api.configurations.findById(id)
//     context.commit('setConfiguration', configuration)
//
//     // for the edit date:
//     // the moment we open the very same configuration, we want to stay with the
//     // current edit date (say we switch from the platform & devices tab to the one
//     // for the locations).
//     // However, in case we load a different configuration there is no point in
//     // reusing the old date (it is very likely that it doesn't make sense for
//     // the now selected configuration).
//     if (oldConfigurationId && oldConfigurationId !== id) {
//       context.commit('setConfigurationEditDate', DateTime.utc())
//     }
//   },
//   async saveConfiguration (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
//     // @ts-ignore
//     const configuration = await this.$api.configurations.save(context.state.configuration)
//     context.commit('setConfiguration', configuration)
//   }
// }
//
// export const getters = {
//   projectNames: (state: ConfigurationsStoreState) => {
//     return state.projects.map((p: Project) => p.name)
//   },
//   configurationEditDate (state: ConfigurationsStoreState): DateTime {
//     return state.configurationEditDate || DateTime.utc()
//   }
// }

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
