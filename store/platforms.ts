/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { Commit, Dispatch } from 'vuex'
import { Platform } from '@/models/Platform'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { IActionType } from '@/models/ActionType'
import { PlatformMountActionWrapper } from '@/viewmodels/PlatformMountActionWrapper'
import { PlatformUnmountActionWrapper } from '@/viewmodels/PlatformUnmountActionWrapper'
import { IDateCompareable } from '@/modelUtils/Compareables'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType = typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE | typeof KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION | typeof KIND_OF_ACTION_TYPE_UNKNOWN

export type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

interface platformsState {
  platforms: Platform[],
  platform: Platform | null,
  platformContacts: Contact[],
  platformAttachments: Attachment[],
  platformAttachment: Attachment|null,
  platformGenericActions: GenericAction[],
  platformGenericAction: GenericAction|null,
  platformSoftwareUpdateActions: SoftwareUpdateAction[],
  platformSoftwareUpdateAction: SoftwareUpdateAction|null,
  platformMountActions: PlatformMountAction[],
  platformUnmountActions: PlatformUnmountAction[],
  chosenKindOfPlatformAction: IOptionsForActionType | null,
  pageNumber: number,
  pageSize: number,
  totalPages: number
}

const state = {
  platforms: [],
  platform: null,
  platformContacts: [],
  platformAttachments: [],
  platformAttachment: null,
  platformGenericActions: [],
  platformSoftwareUpdateActions: [],
  platformMountActions: [],
  platformUnmountActions: [],
  chosenKindOfPlatformAction: null,
  platformGenericAction: null,
  platformSoftwareUpdateAction: null,
  totalPages: 1,
  pageNumber: 1,
  pageSize: 20
}

const getters = {
  actions: (state: platformsState) => {
    let actions = [
      ...state.platformGenericActions,
      ...state.platformSoftwareUpdateActions,
      ...state.platformMountActions,
      ...state.platformUnmountActions
    ]
    // sort the actions
    actions = actions.sort((a: IDateCompareable, b: IDateCompareable): number => {
      return a.date < b.date ? 1 : a.date > b.date ? -1 : 0
    })
    return actions
  }
}

const actions = {
  async searchPlatformsPaginated ({
    commit,
    state
  }: { commit: Commit, state: platformsState }, searchParams: IPlatformSearchParams) {
    let email = null
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
      .searchPaginated(state.pageNumber, state.pageSize)
    commit('setPlatforms', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
  },
  async searchPlatforms ({
    commit
  }: { commit: Commit }, searchtext: string = '') {
    // @ts-ignore
    const platforms = await this.$api.platforms
      .setSearchText(searchtext)
      .searchAll()
    commit('setPlatforms', platforms)
  },
  async loadPlatform ({ commit }: { commit: Commit }, { platformId, includeContacts, includePlatformAttachments }: {platformId: string, includeContacts: boolean, includePlatformAttachments: boolean}) {
    const platform = await this.$api.platforms.findById(platformId, { // TODO Überprüfen, ob man diese Parameter wirklich braucht/ notfalls die payload als Object übergeben lassen
      includeContacts,
      includePlatformAttachments
    })
    commit('setPlatform', platform)
  },
  async loadPlatformContacts ({ commit }: { commit: Commit }, id: string) {
    const platformContacts = await this.$api.platforms.findRelatedContacts(id)
    commit('setPlatformContacts', platformContacts)
  },
  async loadPlatformAttachments ({ commit }: { commit: Commit }, id: string) {
    const platformAttachments = await this.$api.platforms.findRelatedPlatformAttachments(id)
    commit('setPlatformAttachments', platformAttachments)
  },
  async loadPlatformAttachment ({ commit }: { commit: Commit }, id: string) {
    const platformAttachment = await this.$api.platformAttachments.findById(id)
    commit('setPlatformAttachment', platformAttachment)
  },
  async loadAllPlatformActions ({ dispatch }: {dispatch: Dispatch}, id: string) {
    await dispatch('loadPlatformGenericActions', id)
    await dispatch('loadPlatformSoftwareUpdateActions', id)
    await dispatch('loadPlatformMountActions', id)
    await dispatch('loadPlatformUnmountActions', id)
  },
  async loadPlatformGenericActions ({ commit }: { commit: Commit }, id: number) {
    const platformGenericActions = await this.$api.platforms.findRelatedGenericActions(id)
    commit('setPlatformGenericActions', platformGenericActions)
  },
  async loadPlatformSoftwareUpdateActions ({ commit }: { commit: Commit }, id: number) {
    const platformSoftwareUpdateActions = await this.$api.platforms.findRelatedSoftwareUpdateActions(id)
    commit('setPlatformSoftwareUpdateActions', platformSoftwareUpdateActions)
  },
  async loadPlatformMountActions ({ commit }: { commit: Commit }, id: number) {
    const platformMountActions = await this.$api.platforms.findRelatedMountActions(id)

    const wrappedPlatformMountActions = platformMountActions.map((action: PlatformMountAction) => {
      return new PlatformMountActionWrapper(action)
    })

    commit('setPlatformMountActions', wrappedPlatformMountActions)
  },
  async loadPlatformUnmountActions ({ commit }: { commit: Commit }, id: number) {
    const platformUnmountActions = await this.$api.platforms.findRelatedUnmountActions(id)

    const wrappedPlatformUnmountActions = platformUnmountActions.map((action: PlatformUnmountAction) => {
      return new PlatformUnmountActionWrapper(action)
    })
    commit('setPlatformUnmountActions', wrappedPlatformUnmountActions)
  },
  async loadPlatformGenericAction ({ commit }: { commit: Commit }, actionId: string) {
    const genericPlatformAction = await this.$api.genericPlatformActions.findById(actionId)
    commit('setPlatformGenericAction', genericPlatformAction)
  },
  async loadPlatformSoftwareUpdateAction ({ commit }: { commit: Commit }, actionId: string) {
    const platformSoftwareUpdateAction = await this.$api.platformSoftwareUpdateActions.findById(actionId)
    commit('setPlatformSoftwareUpdateAction', platformSoftwareUpdateAction)
  },
  addPlatformContact ({ _commit }: { _commit: Commit }, { platformId, contactId }: {platformId: string, contactId: string}): Promise<void> {
    return this.$api.platforms.addContact(platformId, contactId)
  },
  removePlatformContact ({ _commit }: { _commit: Commit }, { platformId, contactId }: {platformId: number, contactId: number}): Promise<void> {
    return this.$api.platforms.removeContact(platformId, contactId)
  },
  addPlatformAttachment ({ _commit }: { _commit: Commit }, { platformId, attachment }: {platformId: string, attachment: Attachment}): Promise<void> {
    return this.$api.platformAttachments.add(platformId, attachment)
  },
  updatePlatformAttachment ({ _commit }: { _commit: Commit }, { platformId, attachment }: {platformId: string, attachment: Attachment}): Promise<void> {
    return this.$api.platformAttachments.update(platformId, attachment)
  },
  deletePlatformAttachment ({ _commit }: { _commit: Commit }, attachmentId: string): Promise<void> {
    return this.$api.platformAttachments.deleteById(attachmentId)
  },
  addPlatformGenericAction ({ _commit }: { _commit: Commit }, { platformId, genericPlatformAction }: {platformId: string, genericPlatformAction: GenericAction}): Promise<GenericAction> {
    return this.$api.genericPlatformActions.add(platformId, genericPlatformAction)
  },
  updatePlatformGenericAction ({ _commit }: { _commit: Commit }, { platformId, genericPlatformAction }: {platformId: string, genericPlatformAction: GenericAction}): Promise<GenericAction> {
    return this.$api.genericPlatformActions.update(platformId, genericPlatformAction)
  },
  deletePlatformGenericAction ({ _commit }: { _commit: Commit }, genericPlatformActionId: string): Promise<void> {
    return this.$api.genericPlatformActions.deleteById(genericPlatformActionId)
  },
  addPlatformSoftwareUpdateAction ({ _commit }: { _commit: Commit }, { platformId, softwareUpdateAction }: {platformId: string, softwareUpdateAction: SoftwareUpdateAction}): Promise<SoftwareUpdateAction> {
    return this.$api.platformSoftwareUpdateActions.add(platformId, softwareUpdateAction)
  },
  updatePlatformSoftwareUpdateAction ({ _commit }: { _commit: Commit }, { platformId, softwareUpdateAction }: {platformId: string, softwareUpdateAction: SoftwareUpdateAction}): Promise<SoftwareUpdateAction> {
    return this.$api.platformSoftwareUpdateActions.update(platformId, softwareUpdateAction)
  },
  deletePlatformSoftwareUpdateAction ({ _commit }: { _commit: Commit }, softwareUpdateActionId: string): Promise<void> {
    return this.$api.platformSoftwareUpdateActions.deleteById(softwareUpdateActionId)
  },
  updatePlatform ({ commit }: { commit: Commit }, platform: Platform) {
    commit('setPlatform', platform)
  },
  savePlatform ({ _commit }: { _commit: Commit }, platform: Platform): Promise<Platform> {
    return this.$api.platforms.save(platform)
  },
  async copyPlatform ({ dispatch, state }: { dispatch: Dispatch, state: platformsState }, { platform, copyContacts, copyAttachments }: {platform: Platform, copyContacts: boolean, copyAttachments: boolean}) {
    // Todo, prüfen ob man eventuell etwas vereinfachen kann
    const savedPlatform = await dispatch('savePlatform', platform)
    const savedPlatformId = savedPlatform.id!
    const related: Promise<any>[] = []
    if (copyContacts) {
      // hier erstmal die Umsetztung, wie es vorher in pages/platforms/copy/_platformId.vue
      const contacts = platform.contacts
      await dispatch('loadPlatformContacts', savedPlatformId)
      const contactsToSave = contacts.filter(c => state.platformContacts.findIndex((ec: Contact) => { return ec.id === c.id }) === -1)

      for (const contact of contactsToSave) {
        if (contact.id) {
          // related.push(this.$api.platforms.addContact(savedPlatformId, contact.id))
          related.push(dispatch('addPlatformContact', { platformId: savedPlatformId, contactId: contact.id }))
        }
      }
    }
    if (copyAttachments) {
      // hier erstmal die Umsetztung, wie es vorher in pages/platforms/copy/_platformId.vue
      const attachments = platform.attachments.map(Attachment.createFromObject)
      for (const attachment of attachments) {
        attachment.id = null
        related.push(dispatch('addPlatformAttachment', { platformId: savedPlatformId, attachment }))
      }
    }
    await Promise.all(related)
    return savedPlatformId
  },
  async exportAsCsv ({ _commit }: { _commit: Commit}, searchParams: IPlatformSearchParams): Promise<Blob> {
    let email = null
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
  async deletePlatform ({ _commit }: { _commit: Commit }, id: string) {
    await this.$api.platforms.deleteById(id)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setChosenKindOfPlatformAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfPlatformAction', newval)
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
  setPlatformContacts (state: platformsState, platformContacts: Contact[]) {
    state.platformContacts = platformContacts
  },
  setPlatformAttachments (state: platformsState, platformAttachments: Attachment[]) {
    state.platformAttachments = platformAttachments
  },
  setPlatformAttachment (state: platformsState, platformAttachment: Attachment) {
    state.platformAttachment = platformAttachment
  },
  setPlatformGenericActions (state: platformsState, platformGenericActions: GenericAction[]) {
    state.platformGenericActions = platformGenericActions
  },
  setPlatformSoftwareUpdateActions (state: platformsState, platformSoftwareUpdateActions: SoftwareUpdateAction[]) {
    state.platformSoftwareUpdateActions = platformSoftwareUpdateActions
  },
  setPlatformMountActions (state: platformsState, platformMountActions: PlatformMountAction[]) {
    state.platformMountActions = platformMountActions
  },
  setPlatformUnmountActions (state: platformsState, platformUnmountActions: PlatformUnmountAction[]) {
    state.platformUnmountActions = platformUnmountActions
  },
  setChosenKindOfPlatformAction (state: platformsState, newVal: IOptionsForActionType | null) {
    state.chosenKindOfPlatformAction = newVal
  },
  setPlatformGenericAction (state: platformsState, action: GenericAction) {
    state.platformGenericAction = action
  },
  setPlatformSoftwareUpdateAction (state: platformsState, action: SoftwareUpdateAction) {
    state.platformSoftwareUpdateAction = action
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
