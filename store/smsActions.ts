export interface ActionsState{
  actionIdToDelete:string|null
}

export const state = ():ActionsState => {
  return {
    actionIdToDelete: null
  }
}

export const mutations = {
  setActionIdToDelete (state:ActionsState, id:string|null) {
    state.actionIdToDelete = id
  },
  removeActionId (state:ActionsState) {
    this.setActionIdToDelete(state, null)
  }
}
