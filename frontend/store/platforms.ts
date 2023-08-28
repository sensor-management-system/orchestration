/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
import { Commit, Dispatch, GetterTree, ActionTree } from 'vuex'

import { DateTime } from 'luxon'
import { RootState } from '@/store'
import { IncludedRelationships } from '@/services/sms/PlatformApi'

import { Attachment } from '@/models/Attachment'
import { Availability } from '@/models/Availability'
import { ContactRole } from '@/models/ContactRole'
import { GenericAction } from '@/models/GenericAction'
import { IActionType } from '@/models/ActionType'
import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Parameter } from '@/models/Parameter'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'
import { PlatformType } from '@/models/PlatformType'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { Status } from '@/models/Status'

import { PlatformMountActionWrapper } from '@/viewmodels/PlatformMountActionWrapper'
import { PlatformUnmountActionWrapper } from '@/viewmodels/PlatformUnmountActionWrapper'

import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'

import { getLastPathElement } from '@/utils/urlHelpers'
import { KindOfPlatformAction } from '@/models/ActionKind'
import {
  filterActions,
  getDistinctContactsOfActions,
  getDistinctYearsOfActions,
  sortActions
} from '@/utils/actionHelper'

export type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfPlatformAction
}

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface PlatformsState {
  chosenKindOfPlatformAction: IOptionsForActionType | null
  includeArchivedPlatforms: boolean
  onlyOwnPlatforms: boolean
  pageNumber: number
  pageSize: number
  platform: Platform | null
  platformAttachment: Attachment | null
  platformAttachments: Attachment[]
  platformAvailabilities: Availability[]
  platformContactRoles: ContactRole[]
  platformGenericAction: GenericAction | null
  platformGenericActions: GenericAction[]
  platformMountActions: PlatformMountAction[]
  platformParameter: Parameter | null
  platformParameterChangeAction: ParameterChangeAction | null
  platformParameterChangeActions: ParameterChangeAction[]
  platformParameters: Parameter[]
  platformSoftwareUpdateAction: SoftwareUpdateAction | null
  platformSoftwareUpdateActions: SoftwareUpdateAction[]
  platforms: Platform[]
  searchText: string | null
  selectedSearchManufacturers: Manufacturer[]
  selectedSearchPermissionGroups: PermissionGroup[]
  selectedSearchPlatformTypes: PlatformType[]
  selectedSearchStates: Status[]
  totalCount: number
  totalPages: number
}

const state = (): PlatformsState => ({
  chosenKindOfPlatformAction: null,
  includeArchivedPlatforms: false,
  onlyOwnPlatforms: false,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  platform: null,
  platformAttachment: null,
  platformAttachments: [],
  platformAvailabilities: [],
  platformContactRoles: [],
  platformGenericAction: null,
  platformGenericActions: [],
  platformMountActions: [],
  platformParameter: null,
  platformParameterChangeAction: null,
  platformParameterChangeActions: [],
  platformParameters: [],
  platformSoftwareUpdateAction: null,
  platformSoftwareUpdateActions: [],
  platforms: [],
  searchText: null,
  selectedSearchManufacturers: [],
  selectedSearchPermissionGroups: [],
  selectedSearchPlatformTypes: [],
  selectedSearchStates: [],
  totalCount: 0,
  totalPages: 1
})

export type SearchParamsGetter = (isLoggedIn: boolean) => IPlatformSearchParams
export type PossiblePlatformActions =
  GenericAction
  | SoftwareUpdateAction
  | PlatformMountActionWrapper
  | PlatformUnmountActionWrapper
  | ParameterChangeAction
export type PlatformActions = (PossiblePlatformActions)[]
export type PlatformFilter = {
  selectedActionTypes: IOptionsForActionType[],
  selectedYears: number[],
  selectedContacts: string[]
}
export type FilteredActionsGetter = (filter: PlatformFilter) => PlatformActions
export type PageSizesGetter = number[]
export type AvailableContactsOfActionsGetter = string[]
export type AvailableYearsOfActionsGetter = number[]

const getters: GetterTree<PlatformsState, RootState> = {
  searchParams: (state: PlatformsState): SearchParamsGetter => (isLoggedIn: boolean): IPlatformSearchParams => {
    return {
      searchText: state.searchText,
      manufacturer: state.selectedSearchManufacturers,
      states: state.selectedSearchStates,
      types: state.selectedSearchPlatformTypes,
      permissionGroups: state.selectedSearchPermissionGroups,
      onlyOwnPlatforms: state.onlyOwnPlatforms && isLoggedIn,
      includeArchivedPlatforms: state.includeArchivedPlatforms
    }
  },
  availableContactsOfActions: (_state: PlatformsState, getters): string[] => {
    return getDistinctContactsOfActions(getters.actions)
  },
  availableYearsOfActions: (_state: PlatformsState, getters): number[] => {
    return getDistinctYearsOfActions(getters.actions)
  },
  filteredActions: (_state: PlatformsState, getters) => (filter: PlatformFilter): PlatformActions => {
    const filteredActions = filterActions(getters.actions, filter)

    const sortedFilteredActions = sortActions(filteredActions) as PlatformActions

    return sortedFilteredActions
  },
  actions: (state: PlatformsState): PlatformActions => {
    const actions: PlatformActions = [
      ...state.platformGenericActions,
      ...state.platformSoftwareUpdateActions,
      ...state.platformParameterChangeActions
    ]
    for (const platformMountAction of state.platformMountActions) {
      actions.push(new PlatformMountActionWrapper(platformMountAction))
      if (platformMountAction.basicData.endDate) {
        actions.push(new PlatformUnmountActionWrapper(platformMountAction))
      }
    }
    return actions
  },
  pageSizes: (): number[] => {
    return PAGE_SIZES
  }
}

export type AddPlatformAttachmentAction = (params: {
  platformId: string,
  attachment: Attachment
}) => Promise<Attachment>
export type AddPlatformContactRoleAction = (params: { platformId: string, contactRole: ContactRole }) => Promise<void>
export type AddPlatformGenericActionAction = (params: {
  platformId: string,
  genericPlatformAction: GenericAction
}) => Promise<GenericAction>
export type AddPlatformParameterAction = (params: { platformId: string, parameter: Parameter }) => Promise<Parameter>
export type AddPlatformParameterChangeActionAction = (params: {
  parameterId: string,
  action: ParameterChangeAction
}) => Promise<ParameterChangeAction>
export type AddPlatformSoftwareUpdateActionAction = (params: {
  platformId: string,
  softwareUpdateAction: SoftwareUpdateAction
}) => Promise<SoftwareUpdateAction>
export type ArchivePlatformAction = (id: string) => Promise<void>
export type ClearPlatformAvailabilitiesAction = () => void
export type CopyPlatformAction = (params: {
  platform: Platform,
  copyContacts: boolean,
  copyAttachments: boolean,
  copyParameters: boolean,
  originalPlatformId: string
}) => Promise<string>
export type CreatePidAction = (id: string | null) => Promise<string>
export type DeletePlatformAction = (id: string) => Promise<void>
export type DeletePlatformAttachmentAction = (attachmentId: string) => Promise<void>
export type DeletePlatformGenericActionAction = (genericPlatformActionId: string) => Promise<void>
export type DeletePlatformParameterAction = (parameterId: string) => Promise<void>
export type DeletePlatformParameterChangeActionAction = (actionId: string) => Promise<void>
export type DeletePlatformSoftwareUpdateActionAction = (softwareUpdateActionId: string) => Promise<void>
export type DownloadAttachmentAction = (attachmentUrl: string) => Promise<Blob>
export type ExportAsCsvAction = () => Promise<Blob>
export type ExportAsSensorMLAction = (id: string) => Promise<Blob>
export type GetSensorMLUrlAction = (id: string) => string
export type LoadAllPlatformActionsAction = (id: string) => Promise<void>
export type LoadPlatformAction = (params: { platformId: string } & IncludedRelationships) => Promise<void>
export type LoadPlatformAttachmentAction = (id: string) => Promise<void>
export type LoadPlatformAttachmentsAction = (id: string) => Promise<void>
export type LoadPlatformAvailabilitiesAction = (params: {
  ids: (string | null)[],
  from: DateTime,
  until: DateTime | null
}) => Promise<void>
export type LoadPlatformContactRolesAction = (id: string) => Promise<void>
export type LoadPlatformGenericActionAction = (actionId: string) => Promise<void>
export type LoadPlatformGenericActionsAction = (id: string) => Promise<void>
export type LoadPlatformMountActionsAction = (id: string) => Promise<void>
export type LoadPlatformParameterAction = (id: string) => Promise<void>
export type LoadPlatformParameterChangeActionAction = (actionId: string) => Promise<void>
export type LoadPlatformParameterChangeActionsAction = (id: string) => Promise<void>
export type LoadPlatformParametersAction = (id: string) => Promise<void>
export type LoadPlatformSoftwareUpdateActionAction = (actionId: string) => Promise<void>
export type LoadPlatformSoftwareUpdateActionsAction = (id: string) => Promise<void>
export type RemovePlatformContactRoleAction = (params: { platformContactRoleId: string }) => Promise<void>
export type ReplacePlatformInPlatformsAction = (newPlatform: Platform) => void
export type RestorePlatformAction = (id: string) => Promise<void>
export type SavePlatformAction = (platform: Platform) => Promise<Platform>
export type SearchPlatformsPaginatedAction = () => Promise<void>
export type SetChosenKindOfPlatformActionAction = (newval: IOptionsForActionType | null) => void
export type SetIncludeArchivedPlatformsAction = (includeArchivedPlatforms: boolean) => void
export type SetOnlyOwnPlatformsAction = (onlyOwnPlatforms: boolean) => void
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type SetSearchTextAction = (searchText: string | null) => void
export type SetSelectedSearchManufacturersAction = (selectedSearchManufacturers: Manufacturer[]) => void
export type SetSelectedSearchPermissionGroupsAction = (selectedSearchPermissionGroups: PermissionGroup[]) => void
export type SetSelectedSearchPlatformTypesAction = (selectedSearchPlatformTypes: PlatformType[]) => void
export type SetSelectedSearchStatesAction = (selectedSearchStates: Status[]) => void
export type UpdatePlatformAction = (platform: Platform) => void
export type UpdatePlatformAttachmentAction = (params: {
  platformId: string,
  attachment: Attachment
}) => Promise<Attachment>
export type UpdatePlatformGenericActionAction = (params: {
  platformId: string,
  genericPlatformAction: GenericAction
}) => Promise<GenericAction>
export type UpdatePlatformParameterAction = (params: { platformId: string, parameter: Parameter }) => Promise<Parameter>
export type UpdatePlatformParameterChangeActionAction = (params: {
  parameterId: string,
  action: ParameterChangeAction
}) => Promise<ParameterChangeAction>
export type UpdatePlatformSoftwareUpdateActionAction = (params: {
  platformId: string,
  softwareUpdateAction: SoftwareUpdateAction
}) => Promise<SoftwareUpdateAction>

const actions: ActionTree<PlatformsState, RootState> = {
  async searchPlatformsPaginated ({
    commit,
    state,
    getters
  }: { commit: Commit, state: PlatformsState, getters: any }): Promise<void> {
    const searchParams = getters.searchParams(this.$auth.loggedIn)
    let userId = null
    if (searchParams.onlyOwnPlatforms) {
      userId = this.getters['permissions/userId']
    }

    const {
      elements,
      totalCount
    } = await this.$api.platforms
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedPlatformTypes(searchParams.types)
      .setSearchedPermissionGroups(searchParams.permissionGroups)
      .setSearchedCreatorId(userId)
      .setSearchIncludeArchivedPlatforms(searchParams.includeArchivedPlatforms)
      .searchPaginated(
        state.pageNumber,
        state.pageSize,
        {
          includeCreatedBy: true
        }
      )
    commit('setPlatforms', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
    commit('setTotalCount', totalCount)
  },
  async loadPlatform ({ commit }: { commit: Commit },
    {
      platformId,
      includeContacts,
      includePlatformAttachments,
      includePlatformParameters,
      includeCreatedBy,
      includeUpdatedBy
    }: { platformId: string } & IncludedRelationships
  ): Promise<void> {
    const platform = await this.$api.platforms.findById(platformId, { // TODO Überprüfen, ob man diese Parameter wirklich braucht/ notfalls die payload als Object übergeben lassen
      includeContacts,
      includePlatformAttachments,
      includePlatformParameters,
      includeCreatedBy,
      includeUpdatedBy
    })
    commit('setPlatform', platform)
  },
  async loadPlatformContactRoles ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformContactRoles = await this.$api.platforms.findRelatedContactRoles(id)
    commit('setPlatformContactRoles', platformContactRoles)
  },
  async loadPlatformAttachments ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformAttachments = await this.$api.platforms.findRelatedPlatformAttachments(id)
    commit('setPlatformAttachments', platformAttachments)
  },
  async loadPlatformAttachment ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformAttachment = await this.$api.platformAttachments.findById(id)
    commit('setPlatformAttachment', platformAttachment)
  },
  async loadAllPlatformActions ({ dispatch }: { dispatch: Dispatch }, id: string): Promise<void> {
    await Promise.all([
      dispatch('loadPlatformGenericActions', id),
      dispatch('loadPlatformSoftwareUpdateActions', id),
      dispatch('loadPlatformMountActions', id),
      dispatch('loadPlatformParameterChangeActions', id)
    ])
  },
  async loadPlatformGenericActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformGenericActions = await this.$api.platforms.findRelatedGenericActions(id)
    commit('setPlatformGenericActions', platformGenericActions)
  },
  async loadPlatformSoftwareUpdateActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformSoftwareUpdateActions = await this.$api.platforms.findRelatedSoftwareUpdateActions(id)
    commit('setPlatformSoftwareUpdateActions', platformSoftwareUpdateActions)
  },
  async loadPlatformMountActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformMountActions = await this.$api.platforms.findRelatedMountActions(id)
    commit('setPlatformMountActions', platformMountActions)
  },
  async loadPlatformGenericAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const genericPlatformAction = await this.$api.genericPlatformActions.findById(actionId)
    commit('setPlatformGenericAction', genericPlatformAction)
  },
  async loadPlatformSoftwareUpdateAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const platformSoftwareUpdateAction = await this.$api.platformSoftwareUpdateActions.findById(actionId)
    commit('setPlatformSoftwareUpdateAction', platformSoftwareUpdateAction)
  },
  async loadPlatformParameterChangeActions ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const actions = await this.$api.platforms.findRelatedParameterChangeActions(id)
    commit('setPlatformParameterChangeActions', actions)
  },
  async loadPlatformParameterChangeAction ({ commit }: { commit: Commit }, actionId: string): Promise<void> {
    const action = await this.$api.platformParameterChangeActions.findById(actionId)
    commit('setPlatformParameterChangeAction', action)
  },
  async loadPlatformAvailabilities ({ commit }: { commit: Commit }, {
    ids,
    from,
    until
  }: {
    ids: (string | null)[];
    from: DateTime;
    until: DateTime | null
  }): Promise<void> {
    const platformAvailabilities = await this.$api.platforms.checkAvailability(ids, from, until)
    commit('setPlatformAvailabilities', platformAvailabilities)
  },
  async loadPlatformParameters ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const platformParameters = await this.$api.platforms.findRelatedPlatformParameters(id)
    commit('setPlatformParameters', platformParameters)
  },
  async loadPlatformParameter ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const parameter = await this.$api.platformParameters.findById(id)
    commit('setPlatformParameter', parameter)
  },
  deletePlatformParameter (_, parameterId: string): Promise<void> {
    return this.$api.platformParameters.deleteById(parameterId)
  },
  addPlatformParameter (_, {
    platformId,
    parameter
  }: { platformId: string, parameter: Parameter }): Promise<Parameter> {
    return this.$api.platformParameters.add(platformId, parameter)
  },
  updatePlatformParameter (_, {
    platformId,
    parameter
  }: { platformId: string, parameter: Parameter }): Promise<Parameter> {
    return this.$api.platformParameters.update(platformId, parameter)
  },
  addPlatformContactRole (_: {}, {
    platformId,
    contactRole
  }: { platformId: string, contactRole: ContactRole }): Promise<string> {
    return this.$api.platforms.addContact(platformId, contactRole)
  },
  removePlatformContactRole (_: {}, { platformContactRoleId }: { platformContactRoleId: string }): Promise<void> {
    return this.$api.platforms.removeContact(platformContactRoleId)
  },
  addPlatformAttachment (_: {}, {
    platformId,
    attachment
  }: { platformId: string, attachment: Attachment }): Promise<Attachment> {
    return this.$api.platformAttachments.add(platformId, attachment)
  },
  updatePlatformAttachment (_: {}, {
    platformId,
    attachment
  }: { platformId: string, attachment: Attachment }): Promise<Attachment> {
    return this.$api.platformAttachments.update(platformId, attachment)
  },
  deletePlatformAttachment (_: {}, attachmentId: string): Promise<void> {
    return this.$api.platformAttachments.deleteById(attachmentId)
  },
  addPlatformGenericAction (_: {}, {
    platformId,
    genericPlatformAction
  }: { platformId: string, genericPlatformAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericPlatformActions.add(platformId, genericPlatformAction)
  },
  updatePlatformGenericAction (_: {}, {
    platformId,
    genericPlatformAction
  }: { platformId: string, genericPlatformAction: GenericAction }): Promise<GenericAction> {
    return this.$api.genericPlatformActions.update(platformId, genericPlatformAction)
  },
  deletePlatformGenericAction (_: {}, genericPlatformActionId: string): Promise<void> {
    return this.$api.genericPlatformActions.deleteById(genericPlatformActionId)
  },
  addPlatformSoftwareUpdateAction (_: {}, {
    platformId,
    softwareUpdateAction
  }: { platformId: string, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.platformSoftwareUpdateActions.add(platformId, softwareUpdateAction)
  },
  updatePlatformSoftwareUpdateAction (_: {}, {
    platformId,
    softwareUpdateAction
  }: { platformId: string, softwareUpdateAction: SoftwareUpdateAction }): Promise<SoftwareUpdateAction> {
    return this.$api.platformSoftwareUpdateActions.update(platformId, softwareUpdateAction)
  },
  deletePlatformSoftwareUpdateAction (_: {}, softwareUpdateActionId: string): Promise<void> {
    return this.$api.platformSoftwareUpdateActions.deleteById(softwareUpdateActionId)
  },
  addPlatformParameterChangeAction (_, {
    parameterId,
    action
  }: { parameterId: string, action: ParameterChangeAction }): Promise<ParameterChangeAction> {
    return this.$api.platformParameterChangeActions.add(parameterId, action)
  },
  updatePlatformParameterChangeAction (_, {
    parameterId,
    action
  }: { parameterId: string, action: ParameterChangeAction }): Promise<ParameterChangeAction> {
    return this.$api.platformParameterChangeActions.update(parameterId, action)
  },
  deletePlatformParameterChangeAction (_, actionId: string): Promise<void> {
    return this.$api.platformParameterChangeActions.deleteById(actionId)
  },
  updatePlatform ({ commit }: { commit: Commit }, platform: Platform): void {
    commit('setPlatform', platform)
  },
  savePlatform (_: {}, platform: Platform): Promise<Platform> {
    return this.$api.platforms.save(platform)
  },
  createPid (_, id: string | null): Promise<string> {
    return this.$api.pids.create(id, 'platform')
  },
  async copyPlatform ({ dispatch }: { dispatch: Dispatch }, {
    platform,
    copyContacts,
    copyAttachments,
    copyParameters,
    originalPlatformId
  }: {
    platform: Platform,
    copyContacts: boolean,
    copyAttachments: boolean,
    copyParameters: boolean,
    originalPlatformId: string
  }): Promise<string> {
    // Todo, prüfen ob man eventuell etwas vereinfachen kann
    const savedPlatform = await dispatch('savePlatform', platform)
    const savedPlatformId = savedPlatform.id!
    const related: Promise<any>[] = []
    if (copyContacts) {
      const sourceContactRoles = await this.$api.platforms.findRelatedContactRoles(originalPlatformId)
      // The system creates the owner automatically when we create the device
      const freshCreatedContactRoles = await this.$api.platforms.findRelatedContactRoles(savedPlatformId)
      const contactRolesToSave = sourceContactRoles.filter(c => freshCreatedContactRoles.findIndex((ec: ContactRole) => {
        return ec.contact!.id === c.contact!.id && ec.roleName === c.roleName
      }) === -1)

      for (const contactRole of contactRolesToSave) {
        const contactRoleToSave = ContactRole.createFromObject(contactRole)
        contactRoleToSave.id = null
        related.push(dispatch('addPlatformContactRole', {
          platformId: savedPlatformId,
          contactRole: contactRoleToSave
        }))
      }
    }
    if (copyAttachments) {
      // hier erstmal die Umsetztung, wie es vorher in pages/platforms/copy/_platformId.vue
      const attachments = platform.attachments.map(Attachment.createFromObject)
      for (const attachment of attachments) {
        attachment.id = null
        if (attachment.isUpload) {
          const blob = await dispatch('downloadAttachment', attachment.url)
          const filename = getLastPathElement(attachment.url)
          const uploadResult = await dispatch('files/uploadBlob', {
            blob,
            filename
          }, { root: true })
          const newUrl = uploadResult.url
          attachment.url = newUrl
        }
        related.push(dispatch('addPlatformAttachment', {
          platformId: savedPlatformId,
          attachment
        }))
      }
    }
    if (copyParameters) {
      const parameters = platform.parameters.map(Parameter.createFromObject)
      for (const parameter of parameters) {
        parameter.id = null
        related.push(dispatch('addPlatformParameter', {
          platformId: savedPlatformId,
          parameter
        }))
      }
    }
    await Promise.all(related)
    return savedPlatformId
  },
  async downloadAttachment (_, attachmentUrl: string): Promise<Blob> {
    return await this.$api.platformAttachments.getFile(attachmentUrl)
  },
  getSensorMLUrl (_, id: string): string {
    return this.$api.platforms.getSensorMLUrl(id)
  },
  async exportAsSensorML (_, id: string): Promise<Blob> {
    return await this.$api.platforms.getSensorML(id)
  },
  async exportAsCsv ({ getters }: { getters: any }): Promise<Blob> {
    let userId = null
    const searchParams = getters.searchParams(this.$auth.loggedIn)
    if (searchParams.onlyOwnPlatforms) {
      userId = this.getters['permissions/userId']
    }
    // @ts-ignore
    return await this.$api.platforms
      .setSearchText(searchParams.searchText)
      .setSearchedManufacturers(searchParams.manufacturer)
      .setSearchedStates(searchParams.states)
      .setSearchedPlatformTypes(searchParams.types)
      .setSearchedPermissionGroups(searchParams.permissionGroups)
      .setSearchedCreatorId(userId)
      .setSearchIncludeArchivedPlatforms(searchParams.includeArchivedPlatforms)
      .searchMatchingAsCsvBlob()
  },
  async deletePlatform (_: {}, id: string): Promise<void> {
    await this.$api.platforms.deleteById(id)
  },
  async archivePlatform (_, id: string): Promise<void> {
    await this.$api.platforms.archiveById(id)
  },
  async restorePlatform (_, id: string): Promise<void> {
    await this.$api.platforms.restoreById(id)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  setChosenKindOfPlatformAction ({ commit }: { commit: Commit }, newval: IOptionsForActionType | null) {
    commit('setChosenKindOfPlatformAction', newval)
  },
  setSelectedSearchManufacturers ({ commit }: { commit: Commit }, selectedSearchManufacturers: Manufacturer[]) {
    commit('setSelectedSearchManufacturers', selectedSearchManufacturers)
  },
  setSelectedSearchStates ({ commit }: { commit: Commit }, selectedSearchStates: Status[]) {
    commit('setSelectedSearchStates', selectedSearchStates)
  },
  setSelectedSearchPlatformTypes ({ commit }: { commit: Commit }, selectedSearchPlatformTypes: PlatformType[]) {
    commit('setSelectedSearchPlatformTypes', selectedSearchPlatformTypes)
  },
  setSelectedSearchPermissionGroups ({ commit }: {
    commit: Commit
  }, selectedSearchPermissionGroups: PermissionGroup[]) {
    commit('setSelectedSearchPermissionGroups', selectedSearchPermissionGroups)
  },
  setOnlyOwnPlatforms ({ commit }: { commit: Commit }, onlyOwnPlatforms: boolean) {
    commit('setOnlyOwnPlatforms', onlyOwnPlatforms)
  },
  setIncludeArchivedPlatforms ({ commit }: { commit: Commit }, includeArchivedPlatforms: boolean) {
    commit('setIncludeArchivedPlatforms', includeArchivedPlatforms)
  },
  setSearchText ({ commit }: { commit: Commit }, searchText: string | null) {
    commit('setSearchText', searchText)
  },
  replacePlatformInPlatforms ({
    commit,
    state
  }: { commit: Commit, state: PlatformsState }, newPlatform: Platform) {
    const result = []
    for (const oldPlatform of state.platforms) {
      if (oldPlatform.id !== newPlatform.id) {
        result.push(oldPlatform)
      } else {
        result.push(newPlatform)
      }
    }
    commit('setPlatforms', result)
  },
  clearPlatformAvailabilities ({ commit }: { commit: Commit }) {
    commit('setPlatformAvailabilities', [])
  }

}

const mutations = {
  setPlatforms (state: PlatformsState, platforms: Platform[]) {
    state.platforms = platforms
  },
  setPlatform (state: PlatformsState, platform: Platform) {
    state.platform = platform
  },
  setPageNumber (state: PlatformsState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setPageSize (state: PlatformsState, newPageSize: number) {
    state.pageSize = newPageSize
  },
  setTotalPages (state: PlatformsState, count: number) {
    state.totalPages = count
  },
  setTotalCount (state: PlatformsState, count: number) {
    state.totalCount = count
  },
  setPlatformContactRoles (state: PlatformsState, platformContactRoles: ContactRole[]) {
    state.platformContactRoles = platformContactRoles
  },
  setPlatformAttachments (state: PlatformsState, platformAttachments: Attachment[]) {
    state.platformAttachments = platformAttachments
  },
  setPlatformAttachment (state: PlatformsState, platformAttachment: Attachment) {
    state.platformAttachment = platformAttachment
  },
  setPlatformGenericActions (state: PlatformsState, platformGenericActions: GenericAction[]) {
    state.platformGenericActions = platformGenericActions
  },
  setPlatformSoftwareUpdateActions (state: PlatformsState, platformSoftwareUpdateActions: SoftwareUpdateAction[]) {
    state.platformSoftwareUpdateActions = platformSoftwareUpdateActions
  },
  setPlatformMountActions (state: PlatformsState, platformMountActions: PlatformMountAction[]) {
    state.platformMountActions = platformMountActions
  },
  setChosenKindOfPlatformAction (state: PlatformsState, newVal: IOptionsForActionType | null) {
    state.chosenKindOfPlatformAction = newVal
  },
  setPlatformGenericAction (state: PlatformsState, action: GenericAction) {
    state.platformGenericAction = action
  },
  setPlatformSoftwareUpdateAction (state: PlatformsState, action: SoftwareUpdateAction) {
    state.platformSoftwareUpdateAction = action
  },
  setSelectedSearchManufacturers (state: PlatformsState, selectedSearchManufacturers: Manufacturer[]) {
    state.selectedSearchManufacturers = selectedSearchManufacturers
  },
  setSelectedSearchStates (state: PlatformsState, selectedSearchStates: Status[]) {
    state.selectedSearchStates = selectedSearchStates
  },
  setSelectedSearchPlatformTypes (state: PlatformsState, selectedSearchPlatformTypes: PlatformType[]) {
    state.selectedSearchPlatformTypes = selectedSearchPlatformTypes
  },
  setSelectedSearchPermissionGroups (state: PlatformsState, selectedSearchPermissionGroups: PermissionGroup[]) {
    state.selectedSearchPermissionGroups = selectedSearchPermissionGroups
  },
  setOnlyOwnPlatforms (state: PlatformsState, onlyOwnPlatforms: boolean) {
    state.onlyOwnPlatforms = onlyOwnPlatforms
  },
  setIncludeArchivedPlatforms (state: PlatformsState, includeArchivedPlatforms: boolean) {
    state.includeArchivedPlatforms = includeArchivedPlatforms
  },
  setSearchText (state: PlatformsState, searchText: string | null) {
    state.searchText = searchText
  },
  setPlatformAvailabilities (state: PlatformsState, platformAvailabilities: Availability[]) {
    state.platformAvailabilities = platformAvailabilities
  },
  setPlatformParameters (state: PlatformsState, platformParameters: Parameter[]) {
    state.platformParameters = platformParameters
  },
  setPlatformParameter (state: PlatformsState, platformParameter: Parameter) {
    state.platformParameter = platformParameter
  },
  setPlatformParameterChangeActions (state: PlatformsState, platformParameterChangeActions: ParameterChangeAction[]) {
    state.platformParameterChangeActions = platformParameterChangeActions
  },
  setPlatformParameterChangeAction (state: PlatformsState, platformParameterChangeAction: ParameterChangeAction) {
    state.platformParameterChangeAction = platformParameterChangeAction
  }

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
