/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Commit } from 'vuex'

export interface IDefaultlayoutStore {
  fullWidth: boolean
}

const state = (): IDefaultlayoutStore => {
  return {
    fullWidth: false
  }
}

export type SetFullWidthAction = (fullWidth: boolean) => Promise<void>
export type SetDefaultsAction = () => Promise<void>

const mutations = {
  setFullWidth (state: IDefaultlayoutStore, fullWidth: boolean): void {
    state.fullWidth = fullWidth
  }
}

const actions = {
  setFullWidth ({ commit }: {commit: Commit }, fullWidth: boolean) {
    commit('setFullWidth', fullWidth)
  },
  setDefaults ({ commit }: {commit: Commit }) {
    commit('setFullWidth', false)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
