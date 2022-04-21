import { Device } from '@/models/Device'
import { Commit } from 'vuex'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'

interface devicesState {
  devices: Device[],
  device: Device | null,
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  devices: [],
  device: null,
  pageNumber: 1,
  pageSize: 20,
  totalPages: 1,
}

const getters = {}

const actions = {
  async searchDevicesPaginated ({ commit, state }: { commit: Commit, state: devicesState }, searchParams: IDeviceSearchParams) {

    let email = null;
    if (searchParams.onlyOwnDevices) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }

    // @ts-ignore
    const { elements, totalCount } = await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchPaginated(state.pageNumber, state.pageSize)
    commit('setDevices', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async deleteDevice({ commit }: { commit: Commit }, id: number){
    await this.$api.devices.deleteById(id)
  },
  async exportAsCsv({ commit}: { commit: Commit}, searchParams: IDeviceSearchParams):Promise<Blob>{
    let email = null;
    if (searchParams.onlyOwnDevices) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }
    //@ts-ignore
    return await this.$api.devices
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedDeviceTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchMatchingAsCsvBlob()
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  }
}

const mutations = {
  setDevices (state: devicesState, devices: Device[]) {
    state.devices = devices
  },
  setDevice (state: devicesState, device: Device) {
    state.device = device
  },
  setPageNumber (state: devicesState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: devicesState, count: number) {
    state.totalPages = count
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
