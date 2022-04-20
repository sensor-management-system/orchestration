import { Platform } from '@/models/Platform'
import { Commit } from 'vuex'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'

interface platformsState {
  platforms: Platform[],
  platform: Platform | null,
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  platforms: [],
  platform: null,
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}

const getters = {}

const actions = {
  async searchPlatformsPaginated ({
    commit,
    state
  }: { commit: Commit, state: platformsState }, searchParams: IPlatformSearchParams) {

    let email = null;
    if (searchParams.onlyOwnPlatforms) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }

    // @ts-ignore
    const { elements, totalCount } = await this.$api.platforms
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedPlatformTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchPaginated(state.pageNumber, state.pageSize, searchParams)
    commit('setPlatforms', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async loadPlatform({ commit }: { commit: Commit },id:number){
    const platform = await this.$api.platforms.findById(id,{ //TODO Überprüfen, ob man diese Parameter wirklich braucht/ notfalls die payload als Object übergeben lassen
      includeContacts: false,
      includePlatformAttachments: false
    });
    commit('setPlatform',platform)
  },
  async exportAsCsv({ commit}: { commit: Commit}, searchParams: IPlatformSearchParams):Promise<Blob> {
    let email = null;
    if (searchParams.onlyOwnPlatforms) {
      // @ts-ignore
      email = this.$auth.user!.email as string
    }
    // @ts-ignore
    return await this.$api.platforms
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedPlatformTypes(searchParams.types)
      .setSearchedUserMail(email)
      .searchMatchingAsCsvBlob()
  },
  async deletePlatform({ commit }: { commit: Commit }, id: number){
    await this.$api.platforms.deleteById(id)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
}

const mutations = {
  setPlatforms (state: platformsState, platforms: Platform[]) {
    state.platforms = platforms
  },
  setPlatform (state: platformsState, platform: Platform) {
    state.platform = platform
  },
  setPageNumber (state: platformsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setTotalPages (state: platformsState, count: number) {
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
