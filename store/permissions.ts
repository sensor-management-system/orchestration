import { Api } from '@/services/Api'
import { Commit } from 'vuex'
import { UserInfo } from '@/models/UserInfo'
import { PermissionGroup } from '@/models/PermissionGroup'

interface permissionsState {
  userInfo: UserInfo | null,
  permissionGroups: PermissionGroup[]
}

const state = (): permissionsState => ({
  userInfo: null,
  permissionGroups: []
})

const getters = {}
// @ts-ignore
const actions: {
  [key: string]: any;
  $api: Api
} = {
  async loadUserInfo ({ commit }: { commit: Commit }) {
    const userInfo = await this.$api.userInfoApi.get()
    commit('setUserInfo', userInfo)
  },
  async loadPermissionGroups ({ commit }: { commit: Commit }){
    const permissionGroups = await this.$api.permissionGroupApi.findAll()
    commit('setPermissionGroups',permissionGroups)
  }
}

const mutations = {
  setUserInfo (state: permissionsState, userInfo: UserInfo|null) {
    state.userInfo = userInfo
  },
  setPermissionGroups(state:permissionsState,permissionGroups:PermissionGroup[]){
    state.permissionGroups=permissionGroups
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
