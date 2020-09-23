export interface ISnackbarStore {
  error: string,
  success: string
}

export const state = () => {
  return {
    error: '',
    success: ''
  }
}

export const mutations = {
  setError (state: ISnackbarStore, error: string) {
    state.error = error
  },
  setSuccess (state: ISnackbarStore, success: string) {
    state.success = success
  },
  clearError (state: ISnackbarStore) {
    state.error = ''
  },
  clearSuccess (state: ISnackbarStore) {
    state.success = ''
  }
}
