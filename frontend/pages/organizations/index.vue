<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <div>
      <v-row dense>
        <v-col cols="12" md="5">
          <v-text-field
            v-model="searchText"
            label="Search term"
            placeholder="Search organizations"
            @keydown.enter="basicSearch"
          />
        </v-col>
        <v-col align-self="center">
          <v-btn color="primary" small @click="basicSearch">
            Search
          </v-btn>
          <v-btn text small @click="clearBasicSearch">
            Clear
          </v-btn>
        </v-col>
        <v-col align-self="center" class="text-right">
          <v-btn
            v-if="canCreateOrganization"
            color="accent"
            small
            nuxt
            :to="newOrganizationLink"
          >
            New Organization
          </v-btn>
        </v-col>
      </v-row>
    </div>
    <div v-if="organizations.length <= 0 && !isLoading">
      <p class="text-center">
        There are no organizations that match your search criteria.
      </p>
    </div>

    <div v-if="organizations.length > 0">
      <v-row no-gutters class="mt-10">
        <v-col cols="12" md="3">
          <v-subheader>
            <found-entries v-model="totalCount" entity-name="organization" />
          </v-subheader>
        </v-col>

        <v-col cols="12" md="6">
          <v-pagination
            v-model="page"
            :disabled="isLoading"
            :length="totalPages"
            :total-visible="7"
            @input="runSearch"
          />
        </v-col>
        <v-col cols="12" md="3" class="flex-grow-1 flex-shrink-0">
          <v-subheader>
            <page-size-select
              v-model="size"
              :items="pageSizeItems"
              label="Items per page"
            />
          </v-subheader>
        </v-col>
      </v-row>

      <base-list :list-items="organizations">
        <template #list-item="{item}">
          <organizations-list-item :organization="item" from="searchResult">
            <template
              v-if="$auth.loggedIn && canDeleteOrganization(item)"
              #dot-menu-items
            >
              <dot-menu-action-delete @click="initDeleteDialog(item)" />
            </template>
          </organizations-list-item>
        </template>
      </base-list>

      <v-pagination
        v-model="page"
        :disabled="isLoading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <DeleteDialog
      v-if="organizationToDelete"
      v-model="showDeleteDialog"
      title="Delete Contact"
      :disabled="isLoading"
      @cancel="closeDeleteDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the organization <em>{{ organizationToDelete.name }}</em>?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'

import { mapActions, mapGetters, mapState } from 'vuex'

import {
  SetTitleAction,
  SetTabsAction,
  SetBackToAction,
  SetShowBackButtonAction
} from '@/store/appbar'
import { DeleteOrganizationAction, OrganizationsState, PageSizesGetter, SearchOrganizationsPaginatedAction, SetPageNumberAction } from '@/store/organizations'
import { SetPageSizeAction } from '@/store/platforms'
import { LoadingSpinnerState, SetLoadingAction } from '@/store/progressindicator'
import { OrganizationSearchParamsSerializer } from '@/modelUtils/OrganizationSearchParams'
import { QueryParams } from '@/modelUtils/QueryParams'
import FoundEntries from '@/components/shared/FoundEntries.vue'
import BaseList from '@/components/shared/BaseList.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import OrganizationsListItem from '@/components/organizations/OrganizationsListItem.vue'
import { Organization } from '@/models/Organization'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

@Component({
  components: {
    FoundEntries,
    BaseList,
    PageSizeSelect,
    OrganizationsListItem,
    DotMenuActionDelete,
    DeleteDialog
  },
  computed: {
    ...mapState('progressindicator', ['isLoading']),
    ...mapState('organizations', ['organizations', 'pageNumber', 'pageSize', 'totalPages', 'totalCount']),
    ...mapGetters('organizations', ['pageSizes']),
    ...mapGetters('permissions', ['canCreateOrganization', 'canDeleteOrganization'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('organizations', ['searchOrganizationsPaginated', 'setPageNumber', 'setPageSize', 'deleteOrganization']),
    ...mapActions('appbar', ['setTabs', 'setTitle', 'setBackTo', 'setShowBackButton'])
  }
})
export default class SearchOrganizationsPage extends Vue {
  private searchText: string | null = null
  private showDeleteDialog = false
  private organizationToDelete: Organization | null = null

  organizations!: OrganizationsState['organizations']
  pageSize!: OrganizationsState['pageSize']
  pageNumber!: OrganizationsState['pageNumber']
  totalPages!: OrganizationsState['totalPages']
  totalCount!: OrganizationsState['totalCount']
  pageSizes!: PageSizesGetter
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchOrganizationsPaginated!: SearchOrganizationsPaginatedAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setBackTo!: SetBackToAction
  setShowBackButton!: SetShowBackButtonAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  deleteOrganization!: DeleteOrganizationAction

  async created () {
    this.initializeAppBar()
    try {
      this.setLoading(true)
      this.initSearchQueryParams(this.$route.query)
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of organizations failed')
    } finally {
      this.setLoading(false)
    }
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal: number) {
    this.setPageNumber(newVal)
    this.setPageInUrl(false)
  }

  get size (): number {
    return this.pageSize
  }

  set size (newVal: number) {
    const sizeChanged: boolean = this.size !== newVal

    this.setPageSize(newVal)
    this.setSizeInUrl(false)

    if (sizeChanged) {
      this.runSearch()
    }
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([...this.pageSizes, this.getSizeFromUrl()])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  async runInitialSearch (): Promise<void> {
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  basicSearch () {
    this.page = 1
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  async runSearch (): Promise<void> {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchOrganizationsPaginated(this.searchParams)
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of organizations failed')
    } finally {
      this.setLoading(false)
    }
  }

  initSearchQueryParams (queryParams: QueryParams): void {
    const searchParamsObject = new OrganizationSearchParamsSerializer().toSearchParams(queryParams)
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new OrganizationSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  get searchParams () {
    return {
      searchText: this.searchText
    }
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) ?? 1
    }
    return 1
  }

  setPageInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(this.page)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
  }

  setSizeInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.size) {
      // add size to the current url params
      query = {
        ...this.$route.query,
        size: String(this.size)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }

  setPageAndSizeInUrl (preserveHash: boolean = true): Promise<Route> {
    // In general it should be possible to just call
    // setPageInUrl()
    // and
    // setSizeInUrl()
    // However, it seems that setSizeInUrl removes the page parameter then.
    // So we do both in one run.
    let query: QueryParams = {
      ...this.$route.query
    }
    if (this.size) {
      // add size to the current url params
      query = {
        ...query,
        size: String(this.size)
      }
    }
    if (this.page) {
      // add query to the current url params
      query = {
        ...query,
        page: String(this.page)
      }
    }
    return this.$router.replace({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }

  initializeAppBar () {
    this.setTabs([])
    this.setTitle('Organizations')
    this.setShowBackButton(false)
  }

  get newOrganizationLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/organizations/new${params}`
  }

  initDeleteDialog (organization: Organization) {
    this.showDeleteDialog = true
    this.organizationToDelete = organization
  }

  closeDeleteDialog () {
    this.showDeleteDialog = false
    this.organizationToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.organizationToDelete === null || this.organizationToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteOrganization(this.organizationToDelete)
      this.runSearch()// to update the list
      this.$store.commit('snackbar/setSuccess', 'Organization deleted')
    } catch (e) {
      const msg = new ErrorMessageDispatcher()
        .forCase({
          // 409 is a conflict
          status: 409,
          predicate: sourceLowerCaseIncludes('associated contacts'),
          text: 'There are still contacts associated with the organization'
        })
        .defaultText('Organization could not be deleted')
        .dispatch(e)

      this.$store.commit('snackbar/setError', msg)
    } finally {
      this.setLoading(false)
      this.closeDeleteDialog()
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
.progress-spinner {
  position: absolute;
  top: 40vh;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 32px;
  z-index: 99;
}
.v-select__selections input {
  display: none;
}
</style>
