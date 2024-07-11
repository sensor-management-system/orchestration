/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Commit, ActionTree } from 'vuex/types'
import { RootState } from '@/store'

export interface LoadingSpinnerState {
  isLoading: boolean
}

const state = (): LoadingSpinnerState => ({
  isLoading: false
})

export type SetLoadingAction = (isLoading: boolean) => void

const actions: ActionTree<LoadingSpinnerState, RootState> = {
  setLoading ({ commit }: { commit: Commit }, isLoading: boolean) {
    commit('setLoading', isLoading)
  }
}

const mutations = {
  setLoading (state: LoadingSpinnerState, isLoading: boolean) {
    state.isLoading = isLoading
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
