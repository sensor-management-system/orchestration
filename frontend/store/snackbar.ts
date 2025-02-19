/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ISnackbarStore {
  error: string,
  success: string,
  warning: string,
  info: string
}

const state = () => {
  return {
    error: '',
    success: '',
    warning: '',
    info: ''
  }
}

const mutations = {
  setError (state: ISnackbarStore, error: string) {
    state.error = error
  },
  setSuccess (state: ISnackbarStore, success: string) {
    state.success = success
  },
  setInfo (state: ISnackbarStore, info: string) {
    state.info = info
  },
  setWarning (state: ISnackbarStore, warning: string) {
    state.warning = warning
  },
  clearError (state: ISnackbarStore) {
    state.error = ''
  },
  clearSuccess (state: ISnackbarStore) {
    state.success = ''
  },
  clearInfo (state: ISnackbarStore) {
    state.info = ''
  },
  clearWarning (state: ISnackbarStore) {
    state.warning = ''
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
