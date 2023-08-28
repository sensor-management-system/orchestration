/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Rubankumar Moorthy (FZJ, r.moorthy@fz-juelich.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Research Centre Juelich GmbH - Institute of Bio- and Geosciences
 *   Agrosphere (IBG-3, https://www.fz-juelich.de/en/ibg/ibg-3)
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
