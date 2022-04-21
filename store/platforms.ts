import { Platform } from '@/models/Platform'
import { Commit, Dispatch } from 'vuex'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { IActionType } from '@/models/ActionType'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType = typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE | typeof KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION | typeof KIND_OF_ACTION_TYPE_UNKNOWN

type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

interface platformsState {
  platforms: Platform[],
  platform: Platform | null,
  platformContacts:Contact[],
  platformAttachments:Attachment[],
  platformAttachment:Attachment|null,
  platformGenericActions:GenericAction[],
  platformSoftwareUpdateActions:SoftwareUpdateAction[],
  platformMountActions:PlatformMountAction[],
  platformUnmountActions:PlatformUnmountAction[],
  chosenKindOfPlatformAction: IOptionsForActionType | null,
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  platforms: [],
  platform: null,
  platformContacts:[],
  platformAttachments:[],
  platformAttachment:null,
  platformGenericActions:[],
  platformSoftwareUpdateActions:[],
  platformMountActions:[],
  platformUnmountActions:[],
  chosenKindOfPlatformAction:null,
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}

const getters = {
  actions:(state:platformsState)=>{ //Todo actions sortieren, wobei ehrlich gesagt, eine extra route im Backend mit allen Actions (sortiert) besser wäre
    return [
      ...state.platformGenericActions,
      ...state.platformSoftwareUpdateActions,
      ...state.platformMountActions,
      ...state.platformUnmountActions
    ]
  }
}

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
  async loadPlatformContacts({ commit }: { commit: Commit },id:number){
    const platformContacts = await this.$api.platforms.findRelatedContacts(id)
    commit('setPlatformContacts',platformContacts)
  },
  async loadPlatformAttachments({ commit }: { commit: Commit },id:number){
    const platformAttachments = await this.$api.platforms.findRelatedPlatformAttachments(id)
    commit('setPlatformAttachments',platformAttachments)
  },
  async loadPlatformAttachment({ commit }: { commit: Commit },id:number){
    const platformAttachment = await this.$api.platformAttachments.findById(id)
    commit('setPlatformAttachment',platformAttachment)
  },
  async loadAllPlatformActions({dispatch}:{dispatch:Dispatch},id:number){
    await dispatch('loadPlatformGenericActions',id)
    await dispatch('loadPlatformSoftwareUpdateActions',id)
    await dispatch('loadPlatformMountActions',id)
    await dispatch('loadPlatformUnmountActions',id)
  },
  async loadPlatformGenericActions({ commit }: { commit: Commit },id:number){
    const platformGenericActions = await this.$api.platforms.findRelatedGenericActions(id)
    commit('setPlatformGenericActions',platformGenericActions)
  },
  async loadPlatformSoftwareUpdateActions({ commit }: { commit: Commit },id:number){
    const platformSoftwareUpdateActions = await this.$api.platforms.findRelatedSoftwareUpdateActions(id)
    commit('setPlatformSoftwareUpdateActions',platformSoftwareUpdateActions)
  },
  async loadPlatformMountActions({ commit }: { commit: Commit },id:number){
    const platformMountActions = await this.$api.platforms.findRelatedMountActions(id)
    commit('setPlatformMountActions',platformMountActions)
  },
  async loadPlatformUnmountActions({ commit }: { commit: Commit },id:number){
    const platformUnmountActions = await this.$api.platforms.findRelatedUnmountActions(id)
    commit('setPlatformUnmountActions',platformUnmountActions)
  },
  async addPlatformContact({ commit }: { commit: Commit },{platformId,contactId}:{platformId:number,contactId:number}):Promise<void>{
    return this.$api.platforms.addContact(platformId, contactId)
  },
  async removePlatformContact({ commit }: { commit: Commit },{platformId,contactId}:{platformId:number,contactId:number}):Promise<void>{
    return this.$api.platforms.removeContact(platformId, contactId);
  },
  async addPlatformAttachment({ commit }: { commit: Commit },{platformId,attachment}:{platformId:number,attachment:Attachment}):Promise<void>{
    return this.$api.platformAttachments.add(platformId, attachment);
  },
  async updatePlatformAttachment({ commit }: { commit: Commit },{platformId,attachment}:{platformId:number,attachment:Attachment}):Promise<void>{
    return this.$api.platformAttachments.update(platformId, attachment);
  },
  async deletePlatformAttachment({ commit }: { commit: Commit },attachmentId:number): Promise<void>{
    return this.$api.platformAttachments.deleteById(attachmentId);
  },
  async addPlatformGenericAction({ commit }: { commit: Commit },{platformId,genericPlatformAction}:{platformId:number,genericPlatformAction:GenericAction}): Promise<GenericAction>{
    return  this.$api.genericPlatformActions.add(platformId, genericPlatformAction)
  },
  addPlatformSoftwareUpdateAction({ commit }: { commit: Commit },{platformId,softwareUpdateAction}:{platformId:number,softwareUpdateAction:SoftwareUpdateAction}):Promise<SoftwareUpdateAction>{
    return this.$api.platformSoftwareUpdateActions.add(platformId,softwareUpdateAction)
  },
  async updatePlatform({ commit }: { commit: Commit }, platform:Platform){
    commit('setPlatform',platform);
  },
  async savePlatform({ commit }: { commit: Commit }, platform:Platform):Promise<Platform>{
    return this.$api.platforms.save(platform);
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
  setChosenKindOfPlatformAction({ commit }: { commit: Commit }, newval:IOptionsForActionType | null) {
    commit('setChosenKindOfPlatformAction',newval)
  }
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
  },
  setPlatformContacts(state:platformsState,platformContacts:Contact[]){
    state.platformContacts=platformContacts
  },
  setPlatformAttachments(state:platformsState,platformAttachments:Attachment[]){
    state.platformAttachments=platformAttachments;
  },
  setPlatformAttachment(state:platformsState,platformAttachment:Attachment){
    state.platformAttachment=platformAttachment
  },
  setPlatformGenericActions(state:platformsState,platformGenericActions:GenericAction[]){
    state.platformGenericActions=platformGenericActions
  },
  setPlatformSoftwareUpdateActions(state:platformsState,platformSoftwareUpdateActions:SoftwareUpdateAction[]){
    state.platformSoftwareUpdateActions=platformSoftwareUpdateActions
  },
  setPlatformMountActions(state:platformsState,platformMountActions:PlatformMountAction[]){
    state.platformMountActions=platformMountActions
  },
  setPlatformUnmountActions(state:platformsState,platformUnmountActions:PlatformUnmountAction[]){
    state.platformUnmountActions=platformUnmountActions
  },
  setChosenKindOfPlatformAction(state:platformsState,newVal:IOptionsForActionType | null){
    state.chosenKindOfPlatformAction=newVal
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
