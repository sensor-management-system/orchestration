import { Commit } from 'vuex/types'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import { DeviceType } from '@/models/DeviceType'
import { Platform } from '@/models/Platform'
import { ActionType } from '@/models/ActionType'
import { ACTION_TYPE_API_FILTER_DEVICE, ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'

interface vocabularyState {
  manufacturers: Manufacturer[]
  equipmentstatus: Status[]
  devicetypes: DeviceType[]
  platformtypes: PlatformType[],
  platformGenericActionTypes: ActionType[],
  deviceGenericActionTypes:ActionType[]
}

const state = {
  manufacturers: [],
  equipmentstatus: [],
  devicetypes: [],
  platformtypes: [],
  platformGenericActionTypes: [],
  deviceGenericActionTypes:[]
}
// if (this.statusLookup.has(platform.statusUri)) {
//   const platformStatus: Status = this.statusLookup.get(platform.statusUri) as Status
//   return platformStatus.name
// }
const getters = {
  getPlatformTypeByUri: (state: vocabularyState) => (uri: string): PlatformType | undefined => {
    return state.platformtypes.find((platformType: PlatformType) => {
      return platformType.uri === uri
    })
  },
  getDeviceTypeByUri: (state: vocabularyState) => (uri: string): DeviceType | undefined => {
    return state.devicetypes.find((deviceType: DeviceType) => {
      return deviceType.uri === uri
    })
  },
  getEquipmentstatusByUri: (state: vocabularyState) => (uri: string): Status | undefined => {
    return state.equipmentstatus.find((equipmentstatus: Status) => {
      return equipmentstatus.uri === uri
    })
  },
  getManufacturerByUri: (state: vocabularyState) => (uri: string): Manufacturer | undefined => {
    return state.manufacturers.find((manufacturer: Manufacturer) => {
      return manufacturer.uri === uri
    })
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
  async loadDevicetypes ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setDevicetypes', await this.$api.deviceTypes.findAll())
  },
  async loadPlatformtypes ({ commit }: { commit: Commit }) {
    //@ts-ignore
    commit('setPlatformtypes', await this.$api.platformTypes.findAll())
  },
  async loadPlatformGenericActionTypes ({ commit }: { commit: Commit }) { //TODO check api and maybe refactor
    commit('setPlatformGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_PLATFORM).build().findMatchingAsList()
    )
  },
  async loadDeviceGenericActionTypes({ commit }: { commit: Commit }){
    commit('setDeviceGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_DEVICE).build().findMatchingAsList())
  }
}

const mutations = {
  setManufacturers (state: vocabularyState, manufacturers: Manufacturer[]) {
    state.manufacturers = manufacturers
  },
  setEquipmentstatus (state: vocabularyState, equipmentstatus: Status[]) {
    state.equipmentstatus = equipmentstatus
  },
  setDevicetypes (state: vocabularyState, devicetypes: DeviceType[]) {
    state.devicetypes = devicetypes
  },
  setPlatformtypes (state: vocabularyState, platformtypes: PlatformType[]) {
    state.platformtypes = platformtypes
  },
  setPlatformGenericActionTypes (state: vocabularyState, platformGenericActionTypes: ActionType[]) {
    state.platformGenericActionTypes = platformGenericActionTypes
  },
  setDeviceGenericActionTypes(state:vocabularyState,deviceGenericACtionTypes:ActionType[]){
    state.deviceGenericActionTypes=deviceGenericACtionTypes
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
