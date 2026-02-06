/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { ActionTree, Commit, GetterTree } from 'vuex'
import { DateTime } from 'luxon'
import { RootState } from '@/store/index'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmEndpoint } from '@/models/TsmEndpoint'
import { Device } from '@/models/Device'
import { filterLinkings } from '@/utils/dataLinkingHelper'

export enum TSMLinkingDateFilterOperation {
  GTE = 'gte',
  LTE = 'lte'
}

export type TsmLinkingDateFilterOption = {
  text: string
  id: TSMLinkingDateFilterOperation
}

export type TSMLinkingDateFilter = {
  date: DateTime
  operation: TsmLinkingDateFilterOption
}

export type TsmdlThingTree = {
  thing: TsmdlThing
  datastreams: TsmdlDatastream[]
}

export type TsmdlDatasourceTree = {
  datasource: TsmdlDatasource
  thingTrees: TsmdlThingTree[]
}

export type TsmEndpointTree = {
  tsmEndpoint: TsmEndpoint
  datasourceTrees: TsmdlDatasourceTree[]
}

export interface ITsmLinkingState {
  tsmEndpointTrees: TsmEndpointTree[]
  tsmEndpoint: TsmEndpoint | null
  linking: TsmLinking | null
  linkings: TsmLinking[]
  filterSelectedDevices: Device[]
  filterSelectedMeasuredQuantities: DeviceProperty[],
  filterSelectedStartDate: DateTime | null
  filterSelectedStartDateOperation: TsmLinkingDateFilterOption | null
  filterSelectedEndDate: DateTime | null
  filterSelectedEndDateOperation: TsmLinkingDateFilterOption | null
}

const state = (): ITsmLinkingState => ({
  tsmEndpointTrees: [],
  tsmEndpoint: null,
  linkings: [],
  linking: null,
  filterSelectedDevices: [],
  filterSelectedMeasuredQuantities: [],
  filterSelectedStartDate: null,
  filterSelectedStartDateOperation: null,
  filterSelectedEndDate: null,
  filterSelectedEndDateOperation: null
})

export type DevicesPropertiesWithoutLinkingGetter = (action: DeviceMountAction) => DeviceProperty[]
export type DevicesPropertiesWithLinkingGetter = (action: DeviceMountAction) => DeviceProperty[]
export type ThingsGetter = TsmdlThing[]
export type DatastreamsGetter = TsmdlDatastream[]
export type DatasourcesGetter = TsmdlDatasource[]
export type TsmEndpointsGetter = TsmEndpoint[]
export type DatasourcesForEndpointGetter = (arg: TsmEndpoint | null) => TsmdlDatasource[]
export type ThingsForDatasourceGetter = (arg: TsmdlDatasource | null) => TsmdlThing[]
export type DatastreamsForThingGetter = (arg: TsmdlDatastream | null) => TsmdlDatastream[]
export type SuggestedDatasourceIdGetter = (arg: DeviceMountAction, newLinkings: TsmLinking[]) => string | null
export type SuggestedTsmEndpointIdGetter = (arg: DeviceMountAction, newLinkings: TsmLinking[]) => string | null
export type SuggestedThingIdGetter = (arg: DeviceMountAction, newLinkings: TsmLinking[]) => string | null
export type SuggestedLicenseNameGetter = (arg: DeviceMountAction, newLinkings: TsmLinking[]) => string | null
export type DevicesInLinkingsGetter = Device[]
export type MeasuredQuantitiesInLinkingsGetter = DeviceProperty[]
export type DateFilterGetter = TSMLinkingDateFilter | null
export type FilteredLinkingsGetter = TsmLinking[]
export type UsedDatastreamIdsGetter = Set<string>

const getMatchingLinking = (state: ITsmLinkingState, action: DeviceMountAction, newLinkings: TsmLinking[]): TsmLinking | null => {
  let matchingLinking = null

  matchingLinking = state.linkings.find(linking => linking.device?.id === action.device.id)

  if (!matchingLinking) {
    matchingLinking = newLinkings.find(linking => linking.device?.id === action.device.id)
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
  tsmEndpoints: (state: ITsmLinkingState): TsmEndpoint[] => {
    return state.tsmEndpointTrees.map((endpointTree: TsmEndpointTree) => endpointTree.tsmEndpoint)
  },
  datasourceTrees: (state: ITsmLinkingState): TsmdlDatasourceTree[] => {
    return state.tsmEndpointTrees.flatMap((endpointTree: TsmEndpointTree) => endpointTree.datasourceTrees)
  },
  datasources: (_state: ITsmLinkingState, getters): TsmdlDatasourceTree[] => {
    return getters.datasourceTrees.map((tree: TsmdlDatasourceTree) => tree.datasource)
  },
  datasourcesForEndpoint: (state: ITsmLinkingState) => (tsmEndpoint: TsmEndpoint): TsmdlDatasource[] => {
    return findDatasourcesForEndpointInEndpointTrees(state.tsmEndpointTrees, tsmEndpoint)
  },
  thingTrees: (_state: ITsmLinkingState, getters): TsmdlThingTree[] => {
    return getters.datasourceTrees.flatMap((datasourceTree: TsmdlDatasourceTree) => datasourceTree.thingTrees)
  },
  things: (_state: ITsmLinkingState, getters): TsmdlDatasourceTree[] => {
    return getters.thingTrees.map((tree: TsmdlThingTree) => tree.thing)
  },
  thingsForDatasource: (state: ITsmLinkingState) => (datasource: TsmdlDatasource): TsmdlThing[] => {
    return findThingsForDatasourceInEndpointTrees(state.tsmEndpointTrees, datasource)
  },
  datastreams: (_state: ITsmLinkingState, getters): TsmdlDatastream[] => {
    return getters.thingTrees.flatMap((thingTree: TsmdlThingTree) => thingTree.datastreams)
  },
  datastreamsForThing: (state: ITsmLinkingState) => (thing: TsmdlThing): TsmdlDatastream[] => {
    return findDatastreamsForThingInEndpointTrees(state.tsmEndpointTrees, thing)
  },
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
  suggestedThingId: (state: ITsmLinkingState) => (action: DeviceMountAction, newLinkings: TsmLinking[]): string | null => {
    const matchingLinking = getMatchingLinking(state, action, newLinkings)

    if (!matchingLinking || !matchingLinking.thing) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(newLinkings, 'thing')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'thing')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.thing.id
  },
  suggestedDatasourceId: (state: ITsmLinkingState) => (action: DeviceMountAction, newLinkings: TsmLinking[]): string | null => {
    const matchingLinking = getMatchingLinking(state, action, newLinkings)

    if (!matchingLinking || !matchingLinking.datasource) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(newLinkings, 'datasource')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'datasource')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.datasource.id
  },
  suggestedTsmEndpointId: (state: ITsmLinkingState) => (action: DeviceMountAction, newLinkings: TsmLinking[]): string | null => {
    const matchingLinking = getMatchingLinking(state, action, newLinkings)

    if (!matchingLinking || !matchingLinking.tsmEndpoint) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(newLinkings, 'tsmEndpoint')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'tsmEndpoint')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.tsmEndpoint.id
  },
  suggestedLicenseName: (state: ITsmLinkingState) => (action: DeviceMountAction, newLinkings: TsmLinking[]): string | null => {
    const matchingLinking = getMatchingLinking(state, action, newLinkings)

    if (!matchingLinking || !matchingLinking.licenseName) {
      let suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(newLinkings, 'licenseName')
      if (!suggestedIdByNewLinkings) {
        suggestedIdByNewLinkings = getSuggestedIdIfOnlyOneOfAKindIsSelected(state.linkings, 'licenseName')
      }
      return suggestedIdByNewLinkings
    }

    return matchingLinking.licenseName
  },
  devicesInLinkings: (state: ITsmLinkingState): Device[] => {
    if (!state.linkings.length) {
      return []
    }

    const devices = state.linkings.filter((linking) => {
      return !(linking.device === null)
    }).map(linking => linking.device) as Device[]

    // one device can be in multiple linkings
    // so we remove the duplicate occurences
    return devices.filter((value, index, currentArray: Device[]) => {
      return index === currentArray.findIndex(t => t.id === value.id)
    })
  },
  measuredQuantitiesInLinkings: (state: ITsmLinkingState): DeviceProperty[] => {
    if (!state.linkings.length) {
      return []
    }

    const measuredQuantities = state.linkings.filter((linking) => {
      return !(linking.deviceProperty === null)
    }).map(linking => linking.deviceProperty) as DeviceProperty[]

    // we don't use the measured quantities associated with one device (and therefore linking), but the distinct property names of the corresponding measured quantities
    return measuredQuantities.filter((value, index, currentArray: DeviceProperty[]) => {
      return index === currentArray.findIndex(t => t.propertyName === value.propertyName)
    })
  },
  startDateFilter: (state: ITsmLinkingState): TSMLinkingDateFilter | null => {
    if (state.filterSelectedStartDate && state.filterSelectedStartDateOperation) {
      return {
        date: state.filterSelectedStartDate,
        operation: state.filterSelectedStartDateOperation
      }
    }
    return null
  },
  endDateFilter: (state: ITsmLinkingState): TSMLinkingDateFilter | null => {
    if (state.filterSelectedEndDate && state.filterSelectedEndDateOperation) {
      return {
        date: state.filterSelectedEndDate,
        operation: state.filterSelectedEndDateOperation
      }
    }
    return null
  },

  filteredLinkings: (state, getters): TsmLinking[] => {
    if (!state.linkings.length) {
      return []
    }

    return filterLinkings(state.linkings, state.filterSelectedDevices, state.filterSelectedMeasuredQuantities, getters.startDateFilter, getters.endDateFilter)
  }
}

export type LoadTsmEndpointsAction = () => Promise<void>
export type LoadDatasourcesAction = ({ endpoint }: { endpoint: TsmEndpoint | null }) => Promise<void>
export type LoadThingsForDatasourceAction = ({
  endpoint,
  datasource
}: { endpoint: TsmEndpoint, datasource: TsmdlDatasource }) => Promise<void>
export type LoadDatastreamsForDatasourceAndThingAction = ({
  endpoint,
  datasource,
  thing
}: {
  endpoint: TsmEndpoint,
  datasource: TsmdlDatasource,
  thing: TsmdlThing
}) => Promise<void>
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
}: {
  endpoint: TsmEndpoint,
  datasource: TsmdlDatasource,
  thingId: string
}) => Promise<TsmdlThing>
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

  async loadDatasources ({ commit, state }: { commit: Commit, state: ITsmLinkingState }, { endpoint }: {
    endpoint: TsmEndpoint | null
  }): Promise<void> {
    if (endpoint === null) {
      return
    }
    const tsmEndpointTree = state.tsmEndpointTrees.find(tree => tree.tsmEndpoint.id === endpoint.id)
    commit('setDatasourcesForEndpoint', { tsmEndpointTree, datasources: await this.$api.datasources.findAll(endpoint) })
  },

  async loadThingsForDatasource ({ commit }: { commit: Commit }, {
    endpoint,
    datasource
  }: { endpoint: TsmEndpoint | null, datasource: TsmdlDatasource | null }): Promise<void> {
    if (endpoint === null || datasource === null) {
      return
    }
    const tsmdlDatasourceTree: TsmdlDatasourceTree = this.getters['tsmLinking/datasourceTrees'].find((tree: TsmdlDatasourceTree) => tree.datasource.id === datasource.id)
    commit('setThingsForDatasource', {
      tsmdlDatasourceTree,
      things: await this.$api.things.findAllByDatasource(endpoint, datasource)
    })
  },

  async loadDatastreamsForDatasourceAndThing ({ commit }: { commit: Commit }, {
    endpoint,
    datasource,
    thing
  }: { endpoint: TsmEndpoint | null, datasource: TsmdlDatasource | null, thing: TsmdlThing | null }): Promise<void> {
    if (endpoint === null || datasource === null || thing === null) {
      return
    }
    const tsmdlThingTree: TsmdlThingTree = this.getters['tsmLinking/thingTrees'].find((tree: TsmdlThingTree) => tree.thing.id === thing.id)
    commit('setDatastreamsForThing', {
      tsmdlThingTree,
      datastreams: await this.$api.datastreams.findAllByDatasourceAndThing(endpoint, datasource, thing)
    })
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
    state.tsmEndpointTrees = []
    for (const endpoint of tsmEndpoints) {
      state.tsmEndpointTrees.push({
        tsmEndpoint: endpoint,
        datasourceTrees: []
      })
    }
  },
  setDatasourcesForEndpoint (_: ITsmLinkingState, { tsmEndpointTree, datasources }: {
    tsmEndpointTree: TsmEndpointTree,
    datasources: TsmdlDatasource[]
  }) {
    tsmEndpointTree.datasourceTrees = []
    for (const datasource of datasources) {
      tsmEndpointTree.datasourceTrees.push({
        datasource,
        thingTrees: []
      })
    }
  },
  setThingsForDatasource (_: ITsmLinkingState, { tsmdlDatasourceTree, things }: {
    tsmdlDatasourceTree: TsmdlDatasourceTree,
    things: TsmdlThing[]
  }) {
    tsmdlDatasourceTree.thingTrees = []
    for (const thing of things) {
      tsmdlDatasourceTree.thingTrees.push({
        thing,
        datastreams: []
      })
    }
  },
  setDatastreamsForThing (_: ITsmLinkingState, { tsmdlThingTree, datastreams }: {
    tsmdlThingTree: TsmdlThingTree,
    datastreams: TsmdlDatastream[]
  }) {
    tsmdlThingTree.datastreams = datastreams
  },
  setLinkings (state: ITsmLinkingState, linkings: TsmLinking[]) {
    state.linkings = linkings
  },
  setLinking (state: ITsmLinkingState, linking: TsmLinking) {
    state.linking = linking
  },
  setFilterSelectedDevices (state: ITsmLinkingState, selectedDevices: Device[]) {
    state.filterSelectedDevices = selectedDevices
  },
  setFilterSelectedMeasuredQuantities (state: ITsmLinkingState, selectedMeasuredQuantities: DeviceProperty[]) {
    state.filterSelectedMeasuredQuantities = selectedMeasuredQuantities
  },

  setFilterSelectedStartDate (state: ITsmLinkingState, date: DateTime | null) {
    state.filterSelectedStartDate = date
  },
  setFilterSelectedStartDateOperation (state: ITsmLinkingState, operation: TsmLinkingDateFilterOption | null) {
    state.filterSelectedStartDateOperation = operation
  },
  setFilterSelectedEndDate (state: ITsmLinkingState, date: DateTime | null) {
    state.filterSelectedEndDate = date
  },
  setFilterSelectedEndDateOperation (state: ITsmLinkingState, operation: TsmLinkingDateFilterOption | null) {
    state.filterSelectedEndDateOperation = operation
  }
}

function findDatasourcesForEndpointInEndpointTrees (endpointTrees: TsmEndpointTree[], endpoint: TsmEndpoint): TsmdlDatasource[] {
  if (!endpoint) {
    return []
  }
  return endpointTrees.find(tree => tree.tsmEndpoint.id === endpoint.id)?.datasourceTrees.map(tree => tree.datasource) ?? []
}

function getDatasourceTreesFromEndpointTrees (endpointTrees: TsmEndpointTree[]): TsmdlDatasourceTree[] {
  return endpointTrees.flatMap((endpointTree: TsmEndpointTree) => endpointTree.datasourceTrees)
}

function getThingTreesFromEndpointTrees (endpointTrees: TsmEndpointTree[]): TsmdlThingTree[] {
  return getDatasourceTreesFromEndpointTrees(endpointTrees).flatMap((datasourceTree: TsmdlDatasourceTree) => datasourceTree.thingTrees)
}

function findThingsForDatasourceInEndpointTrees (endpointTrees: TsmEndpointTree[], datasource: TsmdlDatasource): TsmdlThing[] {
  if (!datasource) {
    return []
  }
  return getDatasourceTreesFromEndpointTrees(endpointTrees).find(tree => tree.datasource.id === datasource.id)?.thingTrees.map(tree => tree.thing) ?? []
}

function findDatastreamsForThingInEndpointTrees (endpointTrees: TsmEndpointTree[], thing: TsmdlDatasource): TsmdlDatastream[] {
  if (!thing) {
    return []
  }
  return getThingTreesFromEndpointTrees(endpointTrees).find(tree => tree.thing.id === thing.id)?.datastreams ?? []
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
