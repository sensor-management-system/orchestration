/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Commit, GetterTree, ActionTree } from 'vuex'

import { Organization } from '@/models/Organization'
import { RootState } from '@/store'
import { IOrganizationSearchParams } from '@/modelUtils/OrganizationSearchParams'

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface OrganizationsState {
  organizations: Organization[]
  organization: Organization | null
  pageNumber: number
  pageSize: number
  totalCount: number
  totalPages: number
}

const state = (): OrganizationsState => ({
  organizations: [],
  organization: null,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalCount: 0,
  totalPages: 1
})

export type PageSizesGetter = number[]

const getters: GetterTree<OrganizationsState, RootState> = {
  pageSizes: (): number[] => {
    return PAGE_SIZES
  }
}

export type SearchOrganizationsPaginatedAction = (params: IOrganizationSearchParams) => Promise<void>
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type LoadOrganizationAction = ({ organizationId }: { organizationId: string }) => Promise<void>
export type LoadOrganizationByNameAction = ({ name }: { name: string }) => Promise<void>
export type SaveOrganizationAction = (organization: Organization) => Promise<Organization>
export type DeleteOrganizationAction = (organization: Organization) => Promise<void>
const actions: ActionTree<OrganizationsState, RootState> = {
  async searchOrganizationsPaginated (
    {
      commit,
      state
    }: { commit: Commit, state: OrganizationsState },
    searchParams: IOrganizationSearchParams
  ): Promise<void> {
    const { elements, totalCount } = await this.$api.organizations.searchPaginated(
      searchParams,
      state.pageNumber,
      state.pageSize
    )
    commit('setOrganizations', elements)
    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
    commit('setTotalCount', totalCount)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  async loadOrganization ({ commit }: { commit: Commit }, { organizationId }: { organizationId: string }): Promise<void> {
    const organization = await this.$api.organizations.findById(organizationId)
    commit('setOrganization', organization)
  },
  async loadOrganizationByName ({ commit }: { commit: Commit }, { name }: { name: string }): Promise<void> {
    const organization = await this.$api.organizations.findByName(name)
    commit('setOrganization', organization)
  },
  async saveOrganization (_context, organization: Organization): Promise<Organization> {
    return await this.$api.organizations.save(organization)
  },
  async deleteOrganization (_context, organization: Organization): Promise<void> {
    return await this.$api.organizations.deleteById(organization.id!)
  }
}

const mutations = {
  setOrganizations (state: OrganizationsState, organizations: Organization[]) {
    state.organizations = organizations
  },
  setTotalPages (state: OrganizationsState, totalPages: number) {
    state.totalPages = totalPages
  },
  setTotalCount (state: OrganizationsState, totalCount: number) {
    state.totalCount = totalCount
  },
  setPageSize (state: OrganizationsState, pageSize: number) {
    state.pageSize = pageSize
  },
  setPageNumber (state: OrganizationsState, pageNumber: number) {
    state.pageNumber = pageNumber
  },
  setOrganization (state: OrganizationsState, organization: Organization) {
    state.organization = organization
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
