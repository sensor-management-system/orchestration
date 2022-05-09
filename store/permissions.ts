import { Api } from '@/services/Api'
import { Commit } from 'vuex'

interface permissionsState {
  userInfo:{}
}
  const state = ():permissionsState => ({
  userInfo:{}
})

const getters = {

}
// @ts-ignore
const actions: {
  [key: string]: any;
  $api: Api
} = {
  loadUserInfo({commit}:{commit:Commit}){

  }
}

const mutations = {
  setUserInfo(state:permissionsState,userInfo:any){
    state.userInfo = userInfo
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
