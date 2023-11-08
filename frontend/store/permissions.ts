/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
import { DateTime } from 'luxon'
import { Commit, GetterTree, ActionTree } from 'vuex'

import { RootState } from '@/store'

import { UserInfo } from '@/models/UserInfo'
import { PermissionGroup, IPermissionable, IArchivable, IPersistentlyIdentifiable } from '@/models/PermissionGroup'
import { IVisible } from '@/models/Visibility'
import { IMetaCreationInfo } from '@/models/MetaCreationInfo'
import { Contact } from '@/models/Contact'

export type PermissionHandable = IPermissionable & IVisible & IMetaCreationInfo & IArchivable & IPersistentlyIdentifiable

const isInternalAndHasNotPermissionGroups = (entity: PermissionHandable): boolean => {
  return entity.isInternal && (('permissionGroups' in entity && entity.permissionGroups.length === 0) || ('permissionGroup' in entity && entity.permissionGroup === null))
}
const userHasAtLeastOneGroupCommonWithEntity = (entity: PermissionHandable, groups: PermissionGroup[]): boolean => {
  if ('permissionGroups' in entity) {
    return groups.some(userGroup => entity.permissionGroups.some(permissionGroup => permissionGroup.equals(userGroup)))
  }
  if ('permissionGroup' in entity) {
    return groups.some(userGroup => entity.permissionGroup !== null && entity.permissionGroup.equals(userGroup))
  }
  return false
}

const userIsCreatorOfPrivateEntity = (entity: PermissionHandable, userInfo: UserInfo) => {
  const result = entity.isPrivate && entity.createdByUserId === userInfo.id
  return result
}

const userIsCreatorOfContact = (entity: Contact, userInfo: UserInfo) => {
  return entity.createdByUserId === userInfo.id
}

const userIsContact = (entity: Contact, userInfo: UserInfo) => {
  return entity.id && entity.id === userInfo.contactId
}

export interface PermissionsState {
  userInfo: UserInfo | null,
  permissionGroups: PermissionGroup[]
}

const state = (): PermissionsState => ({
  userInfo: null,
  permissionGroups: []
})

export type CanAccessEntityGetter = (entity: PermissionHandable) => boolean
export type CanModifyEntityGetter = (entity: PermissionHandable) => boolean
export type CanDeleteEntityGetter = (entity: PermissionHandable) => boolean
export type CanDeleteContactGetter = (entity: Contact) => boolean
export type CanModifyContactGetter = (entity: Contact) => boolean

export type CanArchiveEntityGetter = (entity: PermissionHandable) => boolean
export type CanRestoreEntityGetter = (entity: PermissionHandable) => boolean
export type MemberedPermissionGroupsGetter = PermissionGroup[]
export type AdministradedPermissionGroupsGetter = PermissionGroup[]
export type UserGroupsGetter = PermissionGroup[]
export type PermissionGroupsGetter = PermissionGroup[]
export type ContactIdGetter = string | null

const getters: GetterTree<PermissionsState, RootState> = {
  canAccessEntity: (state: PermissionsState) => (entity: PermissionHandable): boolean => {
    if (entity.isPublic) {
      return true
    }
    if (state.userInfo === null) {
      return false
    }
    // for private and internal entities, the user has to be active
    if (!state.userInfo.active) {
      return false
    }
    // allow superusers for all entities
    if (state.userInfo.isSuperUser) {
      return true
    }
    // if the entity is private, check if the user that created the entity matches the current user
    if (userIsCreatorOfPrivateEntity(entity, state.userInfo)) {
      return true
    }
    // all internal entities can be accessed by logged-in users
    if (entity.isInternal) {
      return true
    }
    // in case that we missed a check, restrict access
    return false
  },
  canModifyEntity: (state: PermissionsState, getters: any) => (entity: PermissionHandable): boolean => {
    if (entity.archived) {
      return false
    }
    if (!state.userInfo) {
      return false
    }
    if (!state.userInfo.active) {
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    // if the entity is private, check if the user that created the entity matches the current user
    if (userIsCreatorOfPrivateEntity(entity, state.userInfo)) {
      return true
    }
    // if the entity is internal, check if it has no permission groups
    if (isInternalAndHasNotPermissionGroups(entity)) {
      return true
    }
    if (!entity.isPrivate && userHasAtLeastOneGroupCommonWithEntity(entity, getters.userGroups)) {
      return true
    }
    // in case that we missed a check, restrict access
    return false
  },
  canDeleteEntity: (state: PermissionsState) => (entity: PermissionHandable): boolean => {
    if (entity.persistentIdentifier) {
      return false
    }
    if (!state.userInfo) {
      return false
    }
    if (!state.userInfo.active) {
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    // if the entity is private, check if the user that created the entity matches the current user
    if (userIsCreatorOfPrivateEntity(entity, state.userInfo)) {
      return true
    }
    // in case that we missed a check, restrict access
    return false
  },
  canDeleteContact: (state: PermissionsState) => (entity: Contact): boolean => {
    if (!state.userInfo) {
      return false
    }
    if (userIsContact(entity, state.userInfo)) {
      // it doesn't make sense if the user tries to delete the own entry
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    if (userIsCreatorOfContact(entity, state.userInfo)) {
      return true
    }
    return false
  },
  canModifyContact: (state: PermissionsState) => (entity: Contact): boolean => {
    if (!state.userInfo) {
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    if (userIsContact(entity, state.userInfo)) {
      return true
    }
    if (userIsCreatorOfContact(entity, state.userInfo)) {
      return true
    }
    return false
  },
  canArchiveEntity: (state: PermissionsState, getters: any) => (entity: PermissionHandable): boolean => {
    if (entity.archived) {
      return false
    }
    if (!state.userInfo) {
      return false
    }
    if (!state.userInfo.active) {
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    // if the entity is private, check if the user that created the entity matches the current user
    if (userIsCreatorOfPrivateEntity(entity, state.userInfo)) {
      return true
    }
    // if the entity is internal or public, check if the user is admin of at least one of the permission groups of the entity
    if (!entity.isPrivate && userHasAtLeastOneGroupCommonWithEntity(entity, getters.administradedPermissionGroups)) {
      return true
    }
    // in case that we missed a check, restrict access
    return false
  },
  canRestoreEntity: (state: PermissionsState, getters: any) => (entity: PermissionHandable): boolean => {
    if (!entity.archived) {
      return false
    }
    if (!state.userInfo) {
      return false
    }
    if (!state.userInfo.active) {
      return false
    }
    if (state.userInfo.isSuperUser) {
      return true
    }
    // if the entity is private, check if the user that created the entity matches the current user
    if (userIsCreatorOfPrivateEntity(entity, state.userInfo)) {
      return true
    }
    // if the entity is internal or public, check if the user is admin of at least one of the permission groups of the entity
    if (!entity.isPrivate && userHasAtLeastOneGroupCommonWithEntity(entity, getters.administradedPermissionGroups)) {
      return true
    }
    // in case that we missed a check, restrict access
    return false
  },
  memberedPermissionGroups: (state: PermissionsState): PermissionGroup[] => {
    if (state.userInfo !== null && state.userInfo.member !== null) {
      return state.permissionGroups.filter(group => state.userInfo!.isMemberOf(group))
    }
    return []
  },
  administradedPermissionGroups: (state: PermissionsState): PermissionGroup[] => {
    if (state.userInfo !== null) {
      return state.permissionGroups.filter(group => state.userInfo!.isAdminOf(group))
    }
    return []
  },
  userGroups: (state: PermissionsState, getters: any): PermissionGroup[] => {
    if (state.userInfo) {
      return [...new Set(
        [...getters.memberedPermissionGroups, ...getters.administradedPermissionGroups]
      )
      ].sort(
        (a: PermissionGroup, b: PermissionGroup) => a.name.localeCompare(b.name)
      )
    }
    return []
  },
  userId: (state: PermissionsState) => {
    if (state.userInfo) {
      return state.userInfo.id
    }
    return null
  },
  contactId: (state: PermissionsState) => {
    if (state.userInfo) {
      return state.userInfo.contactId
    }
    return null
  },
  permissionGroups: (state: PermissionsState): PermissionGroup[] => {
    return state.permissionGroups
  },
  apikey: (state: PermissionsState): string | null => {
    if (state.userInfo) {
      return state.userInfo.apikey
    }
    return null
  },
  isSuperUser: (state: PermissionsState): boolean => {
    if (state.userInfo) {
      return state.userInfo.isSuperUser
    }
    return false
  },
  termsOfUseAgreementDate: (state: PermissionsState): DateTime | null => {
    if (state.userInfo) {
      return state.userInfo.termsOfUseAgreementDate
    }
    return null
  },
  needToAcceptTermsOfUse: (state: PermissionsState): boolean => {
    // Can be set for every new release.
    // const latestUpdateToTermsOfUse = DateTime.fromISO('2023-03-05T00:00:00')
    if (state.userInfo) {
      if (state.userInfo.termsOfUseAgreementDate === null) {
        return true
      }
      // if (state.userInfo.termsOfUseAgreementDate < latestUpdateToTermsOfUse) {
      //   return true
      // }
    }
    return false
  }
}

export type LoadUserInfoAction = () => void
export type ClearUserInfoAction = () => void
export type LoadPermissionGroupsAction = () => Promise<void>
export type AcceptTermsOfUseAction = () => Promise<void>

const actions: ActionTree<PermissionsState, RootState> = {
  async loadUserInfo ({ commit }: { commit: Commit }, params?: { skipBackendCache?: boolean }) {
    const userInfo = await this.$api.userInfoApi.get(params?.skipBackendCache || false)
    commit('setUserInfo', userInfo)
  },
  clearUserInfo ({ commit }: { commit: Commit }) {
    commit('setUserInfo', null)
  },
  async loadPermissionGroups ({ commit }: { commit: Commit }, params?: { skipBackendCache?: boolean}): Promise<void> {
    const useFrontendCache = false
    const permissionGroups = await this.$api.permissionGroupApi.findAll(useFrontendCache, params?.skipBackendCache || false)
    commit('setPermissionGroups', permissionGroups)
  },
  async acceptTermsOfUse ({ commit }: { commit: Commit }): Promise<void> {
    await this.$api.userModificationApi.acceptTermsOfUse()
    const userInfo = await this.$api.userInfoApi.get()
    commit('setUserInfo', userInfo)
  }
}

const mutations = {
  setUserInfo (state: PermissionsState, userInfo: UserInfo | null) {
    state.userInfo = userInfo
  },
  setPermissionGroups (state: PermissionsState, permissionGroups: PermissionGroup[]) {
    state.permissionGroups = permissionGroups
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
