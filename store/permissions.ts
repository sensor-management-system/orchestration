import { Api } from '@/services/Api'
import { Commit, GetterTree} from 'vuex'
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

const getters = {
  memberedPermissionGroups:(state:permissionsState)=>{
    if(state.userInfo!==null){
      const memberMappedIds = state.userInfo.member.map(groupId=>groupId.split('/').pop())
      // return state.permissionGroups.filter(group => state.userInfo!.isMemberOf(group))
      return state.permissionGroups.filter((group)=>{
        return memberMappedIds.find(groupId => groupId===group.id)
      })
    }
    return []
  },
  administradedPermissionGroups:(state:permissionsState)=>{
    if(state.userInfo !== null){
      const administratedMappedIds = state.userInfo.admin.map(groupId=>groupId.split('/').pop())
      return state.permissionGroups.filter((group)=>{
        return administratedMappedIds.find(groupId => groupId===group.id)
      })
    }
    return []
    // return state.permissionGroups.filter(group => state.userInfo?.isAdminOf(group))
  },
  userGroups:(state:permissionsState,getters:any)=>{
    if(state.userInfo){
      return [...new Set(
          [...getters.memberedPermissionGroups, ...getters.administradedPermissionGroups]
        )
      ]
    }
    return []
  }
}
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
