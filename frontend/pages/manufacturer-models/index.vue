<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <v-tabs-items
      :value="activeTab"
      @input="setActiveTab"
    >
      <v-tab-item :eager="true">
        <v-row dense>
          <v-col
            cols="12"
            md="5"
          >
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search manufacturer models"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col align-self="center">
            <v-btn
              color="primary"
              small
              @click="basicSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearBasicSearch"
            >
              Clear
            </v-btn>
          </v-col>
          <v-col align-self="center" class="text-right">
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              :to="newDeviceLink"
            >
              New Device
            </v-btn>
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              :to="newPlatformLink"
            >
              New Platform
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item :eager="true">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search manufacturer models"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="12">
            <manufacturer-select v-model="selectedSearchManufacturers" label="Select a manufacturer" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="12">
            <v-select v-model="selectedDualUseSearchOption" :items="dualUseSearchOptions" label="Dual use" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="5" align-self="center">
            <v-btn
              color="primary"
              small
              @click="extendedSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearExtendedSearch"
            >
              Clear
            </v-btn>
          </v-col>
          <v-col align-self="center" class="text-right">
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              :to="newDeviceLink"
            >
              New Device
            </v-btn>
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              :to="newPlatformLink"
            >
              New Platform
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>

    <div v-if="manufacturerModels.length <= 0 && !isLoading">
      <p class="text-center">
        There are no manufacturer models that match your search criteria.
      </p>
    </div>

    <div v-if="manufacturerModels.length > 0">
      <v-row no-gutters class="mt-10">
        <v-col cols="12" md="3">
          <v-subheader>
            <found-entries v-model="totalCount" entity-name="manufacturer model" />
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

      <base-list :list-items="manufacturerModels">
        <template #list-item="{item}">
          <manufacturer-models-list-item :manufacturer-model="item" from="searchResult" />
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'

import { mapActions, mapGetters, mapState } from 'vuex'

import {
  SetTitleAction,
  SetTabsAction,
  IAppbarState,
  SetActiveTabAction,
  SetBackToAction,
  SetShowBackButtonAction
} from '@/store/appbar'

import { VocabularyState, LoadManufacturersAction } from '@/store/vocabulary'

import {
  ManufacturermodelsState,
  SearchManufacturerModelsPaginatedAction,
  SetPageNumberAction,
  SetPageSizeAction,
  PageSizesGetter
} from '@/store/manufacturermodels'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

import { Manufacturer } from '@/models/Manufacturer'

import { QueryParams } from '@/modelUtils/QueryParams'
import { DualUseSearchOption, ManufacturerModelSearchParamsSerializer } from '@/modelUtils/ManufacturerModelSearchParams'

import ManufacturerModelsListItem from '@/components/manufacturerModels/ManufacturerModelsListItem.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import BaseList from '@/components/shared/BaseList.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import FoundEntries from '@/components/shared/FoundEntries.vue'

@Component({
  components: {
    FoundEntries,
    BaseList,
    ManufacturerSelect,
    PageSizeSelect,
    ManufacturerModelsListItem
  },
  computed: {
    ...mapState('progressindicator', ['isLoading']),
    ...mapState('appbar', ['activeTab']),
    ...mapState('vocabulary', ['manufacturers']),
    ...mapState('manufacturermodels', ['manufacturerModels', 'pageNumber', 'pageSize', 'totalPages', 'totalCount']),
    ...mapGetters('manufacturermodels', ['pageSizes'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadManufacturers']),
    ...mapActions('manufacturermodels', ['searchManufacturerModelsPaginated', 'setPageNumber', 'setPageSize']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setActiveTab', 'setBackTo', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SearchManufacturerModelsPage extends Vue {
  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedDualUseSearchOption: DualUseSearchOption = 'all'
  private searchText: string | null = null

  // vuex definition for typescript check
  manufacturerModels!: ManufacturermodelsState['manufacturerModels']
  pageSize!: ManufacturermodelsState['pageSize']
  pageNumber!: ManufacturermodelsState['pageNumber']
  totalPages!: ManufacturermodelsState['totalPages']
  totalCount!: ManufacturermodelsState['totalCount']
  pageSizes!: PageSizesGetter
  loadManufacturers!: LoadManufacturersAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchManufacturerModelsPaginated!: SearchManufacturerModelsPaginatedAction
  manufacturers!: VocabularyState['manufacturers']
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  activeTab!: IAppbarState['activeTab']
  setActiveTab!: SetActiveTabAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setBackTo!: SetBackToAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    this.initializeAppBar()
    try {
      this.setLoading(true)
      await this.loadManufacturers()
      this.initSearchQueryParams(this.$route.query)
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of manufacturer models failed')
    } finally {
      this.setLoading(false)
    }
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
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
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  get searchParams () {
    return {
      searchText: this.searchText,
      manufacturers: this.selectedSearchManufacturers,
      dualUseSearchOption: this.selectedDualUseSearchOption
    }
  }

  get dualUseSearchOptions (): DualUseSearchOption[] {
    return ['all', 'yes', 'no', 'unspecified']
  }

  isExtendedSearch (): boolean {
    return !!this.selectedSearchManufacturers.length || this.selectedDualUseSearchOption !== 'all'
  }

  async runInitialSearch (): Promise<void> {
    this.setActiveTab(this.isExtendedSearch() ? 1 : 0)

    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  basicSearch () {
    this.selectedSearchManufacturers = []
    this.page = 1
    this.selectedDualUseSearchOption = 'all'
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch () {
    this.page = 1
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedSearchManufacturers = []
    this.selectedDualUseSearchOption = 'all'
    this.initUrlQueryParams()
  }

  async runSearch (): Promise<void> {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchManufacturerModelsPaginated(this.searchParams)
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of manufacturer models failed')
    } finally {
      this.setLoading(false)
    }
  }

  initSearchQueryParams (queryParams: QueryParams): void {
    const searchParamsObject = (new ManufacturerModelSearchParamsSerializer({
      manufacturer: this.manufacturers
    })).toSearchParams(queryParams)

    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.manufacturers) {
      this.selectedSearchManufacturers = searchParamsObject.manufacturers
    }
    if (searchParamsObject.dualUseSearchOption) {
      this.selectedDualUseSearchOption = searchParamsObject.dualUseSearchOption
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new ManufacturerModelSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
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
    this.setTabs([
      'Search',
      'Extended Search'
    ])
    this.setTitle('Manufacturer models')
    this.setShowBackButton(false)
  }

  get newDeviceLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/devices/new${params}`
  }

  get newPlatformLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/platforms/new${params}`
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
