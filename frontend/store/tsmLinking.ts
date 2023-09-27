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
import { ActionTree, Commit, GetterTree } from 'vuex'
import { RootState } from '@/store/index'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmDeviceMountPropertyCombination } from '@/utils/configurationInterfaces'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export interface ITsmLinkingState {
  tsmEndpoints: TsmEndpoint[]
  tsmEndpoint: TsmEndpoint | null
  datasources: TsmdlDatasource[]
  things: TsmdlThing[]
  datastreams: TsmdlDatastream[]
  linkings: TsmLinking[]
  newLinkings: TsmLinking[]
  linking: TsmLinking | null
}

const state = (): ITsmLinkingState => ({
  tsmEndpoints: [],
  tsmEndpoint: null,
  datasources: [],
  things: [],
  datastreams: [],
  linkings: [],
  newLinkings: [],
  linking: null
})

export type DevicesPropertiesWithoutLinkingGetter = (action: DeviceMountAction) => DeviceProperty[]
export type DevicesPropertiesWithLinkingGetter = (action: DeviceMountAction) => DeviceProperty[]
export type FindThingByIdGetter = (id: String) => TsmdlThing | undefined
export type FindDatastreamByIdGetter = (id: String) => TsmdlDatastream | undefined
export type FindDatasourceByIdGetter = (id: String) => TsmdlDatasource | undefined
export type SuggestedDatasourceIdGetter = (arg: TsmDeviceMountPropertyCombination) => string | null
export type SuggestedTsmEndpointIdGetter = (arg: TsmDeviceMountPropertyCombination) => string | null
export type SuggestedThingIdGetter = (arg: TsmDeviceMountPropertyCombination) => string | null

const getMatchingLinking = (state: ITsmLinkingState, selectedDeviceActionPropertyCombination: TsmDeviceMountPropertyCombination): TsmLinking | null => {
  let matchingLinking = null

  const { action } = selectedDeviceActionPropertyCombination
  matchingLinking = state.linkings.find(linking => linking.device?.id === action.device.id)

  if (!matchingLinking) {
    matchingLinking = state.newLinkings.find(linking => linking.device?.id === action.device.id)
  }

  if (!matchingLinking) {
    return null
  }

  return matchingLinking
}

const getSuggestedIdIfOnlyOneOfAKindIsSelected = (linkings: TsmLinking[], type: string) => {
  if (linkings.length === 0) {
    return null
  }

  const listOfSelectedEntity = linkings.map((linking: { [key: string]: any }) => linking[type])
    .filter(value => value !== null)

  if (listOfSelectedEntity.length > 0) {
    const idOfFirst = listOfSelectedEntity[0]!.id
    const otherEntity = listOfSelectedEntity.filter(value => value!.id !== idOfFirst)

    if (otherEntity.length === 0) {
      return idOfFirst
    }
  }

  return null
}

const getters: GetterTree<ITsmLinkingState, RootState> = {
  devicesPropertiesWithoutLinking: (state: ITsmLinkingState) => (action: DeviceMountAction): DeviceProperty[] => {
    return action.device.properties.filter((prop: DeviceProperty) => {
      return state.linkings.filter((linking) => {
        return linking.deviceMountAction!.id === action.id &&
          linking.device!.id === action.device.id &&
          linking.deviceProperty!.id === prop.id
      }).length === 0
    })
  },
  devicesPropertiesWithLinking: (state: ITsmLinkingState) => (action: DeviceMountAction): DeviceProperty[] => {
    return action.device.properties.filter((prop: DeviceProperty) => {
      return state.linkings.filter((linking) => {
        return linking.deviceMountAction!.id === action.id &&
          linking.device!.id === action.device.id &&
          linking.deviceProperty!.id === prop.id
      }).length > 0
    })
  },
  suggestedThingId: (state: ITsmLinkingState) => (selectedDeviceActionPropertyCombination: TsmDeviceMountPropertyCombination): string | null => {
    if (!state.linkings || !selectedDeviceActionPropertyCombination) {
      return null
    }

    const matchingLinking = getMatchingLinking(state, selectedDeviceActionPropertyCombination)

    if (!matchingLinking || !matchingLinking.thing) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.newLinkings, 'thing')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'thing')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.thing.id
  },
  suggestedDatasourceId: (state: ITsmLinkingState) => (selectedDeviceActionPropertyCombination: TsmDeviceMountPropertyCombination): string | null => {
    if (!state.linkings || !selectedDeviceActionPropertyCombination) {
      return null
    }

    const matchingLinking = getMatchingLinking(state, selectedDeviceActionPropertyCombination)

    if (!matchingLinking || !matchingLinking.datasource) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.newLinkings, 'datasource')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'datasource')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.datasource.id
  },
  suggestedTsmEndpointId: (state: ITsmLinkingState) => (selectedDeviceActionPropertyCombination: TsmDeviceMountPropertyCombination): string | null => {
    if (!state.linkings || !selectedDeviceActionPropertyCombination) {
      return null
    }

    const matchingLinking = getMatchingLinking(state, selectedDeviceActionPropertyCombination)

    if (!matchingLinking || !matchingLinking.tsmEndpoint) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.newLinkings, 'tsmEndpoint')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'tsmEndpoint')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.tsmEndpoint.id
  }
}

export type LoadTsmEndpointsAction = () => Promise<void>
export type LoadDatasourcesAction = ({ endpoint }: { endpoint: TsmEndpoint }) => Promise<void>
export type LoadThingsForDatasourceAction = ({
  endpoint,
  datasource
}: { endpoint: TsmEndpoint, datasource: TsmdlDatasource }) => Promise<void>
export type LoadDatastreamsForDatasourceAndThingAction = ({
  endpoint,
  datasource,
  thing
}: { endpoint: TsmEndpoint, datasource: TsmdlDatasource, thing: TsmdlThing }) => Promise<void>
export type LoadConfigurationTsmLinkingsAction = (configurationId: string) => Promise<void>
export type AddConfigurationTsmLinkingAction = (tsmLinking: TsmLinking) => Promise<string>
export type UpdateConfigurationTsmLinkingAction = (tsmLinking: TsmLinking) => Promise<string>
export type DeleteConfigurationTsmLinkingAction = (tsmLinking: TsmLinking) => Promise<void>
export type LoadConfigurationTsmLinkingAction = (linkingId: string) => Promise<void>
export type LoadOneDatasourceAction = ({
  endpoint,
  datasourceId
}: { endpoint: TsmEndpoint, datasourceId: string }) => Promise<TsmdlDatasource>
export type LoadOneThingAction = ({
  endpoint,
  datasource,
  thingId
}: { endpoint: TsmEndpoint, datasource: TsmdlDatasource, thingId: string }) => Promise<TsmdlThing>
export type LoadOneDatastreamAction = ({
  endpoint,
  datasource,
  thing,
  datastreamId
}: {
  endpoint: TsmEndpoint,
  datasource: TsmdlDatasource,
  thing: TsmdlThing,
  datastreamId: string
}) => Promise<TsmdlDatastream>

const actions: ActionTree<ITsmLinkingState, RootState> = {

  async loadTsmEndpoints ({ commit }: { commit: Commit }): Promise<void> {
    commit('setTsmEndpoints', await this.$api.tsmEndpoints.findAll())
  },

  async loadTsmEndpoint ({ commit }: { commit: Commit }, { tsmEndpointId }: { tsmEndpointId: string }): Promise<void> {
    commit('setTsmEndpoint', await this.$api.tsmEndpoints.findOneById(tsmEndpointId))
  },

  async loadDatasources ({ commit }: { commit: Commit }, { endpoint }: {
    endpoint: TsmEndpoint | null
  }): Promise<void> {
    if (endpoint === null) {
      commit('setDatasources', [])
    } else {
      commit('setDatasources', await this.$api.datasources.findAll(endpoint))
    }
  },

  async loadThingsForDatasource ({ commit }: { commit: Commit }, {
    endpoint,
    datasource
  }: { endpoint: TsmEndpoint | null, datasource: TsmdlDatasource | null }): Promise<void> {
    if (endpoint === null || datasource === null) {
      commit('setThings', [])
    } else {
      commit('setThings', await this.$api.things.findAllByDatasource(endpoint, datasource))
    }
  },

  async loadDatastreamsForDatasourceAndThing ({ commit }: { commit: Commit }, {
    endpoint,
    datasource,
    thing
  }: { endpoint: TsmEndpoint | null, datasource: TsmdlDatasource | null, thing: TsmdlThing | null }): Promise<void> {
    if (endpoint === null || datasource === null || thing === null) {
      commit('setDatastreams', [])
    } else {
      commit('setDatastreams', await this.$api.datastreams.findAllByDatasourceAndThing(endpoint, datasource, thing))
    }
  },

  async loadConfigurationTsmLinkings ({ commit }: { commit: Commit }, configurationId: string): Promise<void> {
    const linkings = await this.$api.configurations.findRelatedTsmLinkings(configurationId)
    commit('setLinkings', linkings)
  },

  async loadOneDatasource (_, {
    endpoint,
    datasourceId
  }: { endpoint: TsmEndpoint, datasourceId: string }): Promise<TsmdlDatasource | null> {
    return await this.$api.datasources.findOneById(endpoint, datasourceId)
  },

  async loadOneThing (_, {
    endpoint,
    datasource,
    thingId
  }: { endpoint: TsmEndpoint, datasource: TsmdlDatasource, thingId: string }): Promise<TsmdlThing | null> {
    return await this.$api.things.findOneByDatasourceAndId(endpoint, datasource, thingId)
  },

  async loadOneDatastream (
    _, {
      endpoint,
      datasource,
      thing,
      datastreamId
    }: { endpoint: TsmEndpoint, datasource: TsmdlDatasource, thing: TsmdlThing, datastreamId: string }
  ): Promise<TsmdlDatastream | null> {
    return await this.$api.datastreams.findOneByDatasourceAndThingAndId(endpoint, datasource, thing, datastreamId)
  },
  async loadConfigurationTsmLinking (
    {
      commit
    }: { commit: Commit }, linkingId: string
  ): Promise<void> {
    commit('setLinking', await this.$api.configurations.tsmLinkingApi.findById(linkingId))
  },

  addConfigurationTsmLinking (_: {}, tsmLinking: TsmLinking) {
    return this.$api.configurations.tsmLinkingApi.add(tsmLinking)
  },

  updateConfigurationTsmLinking (_: {}, tsmLinking: TsmLinking) {
    return this.$api.configurations.tsmLinkingApi.update(tsmLinking)
  },

  deleteConfigurationTsmLinking (_: {}, tsmLinking: TsmLinking) {
    return this.$api.configurations.tsmLinkingApi.delete(tsmLinking)
  }
}

const mutations = {
  setTsmEndpoints (state: ITsmLinkingState, tsmEndpoints: TsmEndpoint[]) {
    state.tsmEndpoints = tsmEndpoints
  },
  setTsmEndpoint (state: ITsmLinkingState, tsmEndpoint: TsmEndpoint) {
    state.tsmEndpoint = tsmEndpoint
  },
  setDatasources (state: ITsmLinkingState, datasources: TsmdlDatasource[]) {
    state.datasources = datasources
  },
  setThings (state: ITsmLinkingState, things: TsmdlThing[]) {
    state.things = things
  },
  setDatastreams (state: ITsmLinkingState, datastreams: TsmdlDatastream[]) {
    state.datastreams = datastreams
  },
  setLinkings (state: ITsmLinkingState, linkings: TsmLinking[]) {
    state.linkings = linkings
  },
  setNewLinkings (state: ITsmLinkingState, linkings: TsmLinking[]) {
    state.newLinkings = linkings
  },
  setLinking (state: ITsmLinkingState, linking: TsmLinking) {
    state.linking = linking
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
