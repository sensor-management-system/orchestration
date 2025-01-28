/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { ActionTree, Commit, GetterTree } from 'vuex'
import { RootState } from '@/store/index'
import { StaThing } from '@/models/sta/StaThing'
import { StaDatastream } from '@/models/sta/StaDatastream'
import { StaDatastreamQueryParams, StaThingQueryParams } from '@/utils/staQueryHelper'

export interface IStaState {
  things: StaThing[]
  thing: StaThing | null,
  datastreams: StaDatastream[],
  datastream: StaDatastream | null
}

const state = (): IStaState => ({
  things: [],
  thing: null,
  datastreams: [],
  datastream: null
})

const getters: GetterTree<IStaState, RootState> = {
}

export type LoadOneStaThingAction = ({ baseUrl, id, params }: {
  baseUrl: string,
  id: string,
  params: string|StaThingQueryParams
}) => Promise<StaThing|undefined>

export type LoadStaThingsAction = ({ baseUrl, params }: {
  baseUrl: string,
  params: string|StaThingQueryParams
}) => Promise<StaThing[]>

export type LoadOneStaDatastreamAction = ({ baseUrl, id, params }: {
  baseUrl: string,
  id: string,
  params: string|StaDatastreamQueryParams
}) => Promise<StaDatastream|undefined>

export type LoadStaDatastreamsAction = ({ baseUrl, params }: {
  baseUrl: string,
  params: string|StaDatastreamQueryParams
}) => Promise<StaDatastream[]>

const actions: ActionTree<IStaState, RootState> = {
  async loadOneStaThing ({ commit }: { commit: Commit }, { baseUrl, id, params }: {baseUrl: string, id: string, params: string|StaThingQueryParams}): Promise<StaThing|null> {
    const thing: StaThing|null = await this.$api.staThings.findOneById(baseUrl, id, params)
    commit('setStaThing', thing ?? null)
    return thing
  },

  async loadStaThings ({ commit }: { commit: Commit }, { baseUrl, params }: { baseUrl: string, params: string|StaThingQueryParams }): Promise<StaThing[]> {
    const things: StaThing[] = await this.$api.staThings.findAll(baseUrl, params)
    commit('setStaThings', things)
    return things
  },

  async loadOneStaDatastream ({ commit }: { commit: Commit }, { baseUrl, id, params }: {baseUrl: string, id: string, params: string|StaDatastreamQueryParams}): Promise<StaDatastream|null> {
    const datastream: StaDatastream|null = await this.$api.staDatastreams.findOneById(baseUrl, id, params)
    commit('setStaDatastream', datastream ?? null)
    return datastream
  },

  async loadStaDatastreams ({ commit }: { commit: Commit }, { baseUrl, params }: { baseUrl: string, params: string|StaDatastreamQueryParams }): Promise<StaDatastream[]> {
    const datastreams: StaDatastream[] = await this.$api.staDatastreams.findAll(baseUrl, params)
    commit('setStaDatastreams', datastreams)
    return datastreams
  }
}

const mutations = {
  setStaThings (state: IStaState, things: StaThing[]) {
    state.things = things
  },
  setStaThing (state: IStaState, thing: StaThing) {
    state.thing = thing
  },

  setStaDatastreams (state: IStaState, datastreams: StaDatastream[]) {
    state.datastreams = datastreams
  },
  setStaDatastream (state: IStaState, datastream: StaDatastream) {
    state.datastream = datastream
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
