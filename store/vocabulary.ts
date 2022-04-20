import { Commit } from 'vuex/types'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import { DeviceType } from '@/models/DeviceType'
import { Platform } from '@/models/Platform'

interface vocabularyState {
  manufacturers: Manufacturer[]
  equipmentstatus: Status[]
  equipmenttypes: DeviceType[]
  platformtypes: PlatformType[]
}

const state = {
  manufacturers: [],
  equipmentstatus: [],
  equipmenttypes: [],
  platformtypes: []
}
// if (this.statusLookup.has(platform.statusUri)) {
//   const platformStatus: Status = this.statusLookup.get(platform.statusUri) as Status
//   return platformStatus.name
// }
const getters = {
  getPlatformTypeByUri: (state:vocabularyState)=>(uri:string):PlatformType|undefined=>{
    return state.platformtypes.find((platformType:PlatformType)=>{
      return platformType.uri===uri
    });
  },
  getEquipmentstatusByUri: (state:vocabularyState)=>(uri:string):Status|undefined=>{
    return state.equipmentstatus.find((equipmentstatus:Status)=>{
      return equipmentstatus.uri===uri
    });
  },
  getManufacturerByUri: (state:vocabularyState)=>(uri:string):Manufacturer|undefined=>{
    return state.manufacturers.find((manufacturer:Manufacturer)=>{
      return manufacturer.uri===uri
    });
  }
}

const actions = {
  async loadManufacturers ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setManufacturers', await this.$api.manufacturer.findAll())
  },
  async loadEquipmentstatus ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setEquipmentstatus', await this.$api.states.findAll())
  },
  async loadEquipmenttypes ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setEquipmenttypes', await this.$api.deviceTypes.findAll())
  },
  async loadPlatformtypes ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setPlatformtypes', await this.$api.platformTypes.findAll())
  },
}

const mutations = {
  setManufacturers (state: vocabularyState, manufacturers: Manufacturer[]) {
    state.manufacturers = manufacturers
  },
  setEquipmentstatus (state: vocabularyState, equipmentstatus: Status[]) {
    state.equipmentstatus = equipmentstatus
  },
  setEquipmenttypes (state: vocabularyState, equipmenttypes: DeviceType[]) {
    state.equipmenttypes = equipmenttypes
  },
  setPlatformtypes (state: vocabularyState, platformtypes: PlatformType[]) {
    state.platformtypes = platformtypes
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
