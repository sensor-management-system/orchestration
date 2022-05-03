<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
      v-model="activeTab"
    >
      <PlatformsBasicSearch
        v-model="searchText"
        @search="basicSearch"
        @clear="clearBasicSearch"
      />
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="6">
            <PlatformsBasicSearchField
              v-model="searchText"
              @start-search="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <StatusSelect v-model="selectedSearchStates" label="Select a status" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <PlatformTypeSelect v-model="selectedSearchPlatformTypes" label="Select a platform type" />
          </v-col>
        </v-row>
        <v-row v-if="$auth.loggedIn">
          <v-col cols="12" md="3">
            <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            align-self="center"
          >
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
        </v-row>
      </v-tab-item>
    </v-tabs-items>

    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="platforms.length <=0 && !loading">
      <p class="text-center">
        There are no platforms that match your search criteria.
      </p>
    </div>

    <div v-if="platforms.length>0">
      <v-subheader>
        <template v-if="platforms.length == 1">
          1 platform found
        </template>
        <template v-else>
          {{ platforms.length }} platforms found
        </template>
        <v-spacer />

        <template v-if="platforms.length>0">
          <v-dialog v-model="processing" max-width="100">
            <v-card>
              <v-card-text>
                <div class="text-center pt-2">
                  <v-progress-circular indeterminate />
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-menu
            close-on-click
            close-on-content-click
            offset-x
            left
            z-index="999"
          >
            <template #activator="{ on }">
              <v-btn
                icon
                v-on="on"
              >
                <v-icon
                  dense
                >
                  mdi-file-download
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                dense
                @click.prevent="exportCsv"
              >
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon
                      left
                    >
                      mdi-table
                    </v-icon>
                    CSV
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-subheader>

      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
      <BaseList
        :list-items="platforms"
      >
        <template #list-item="{item}">
          <PlatformsListItem
            :key="item.id"
            :platform="item"
          >
            <template #dot-menu-items>
              <DotMenuActionCopy
                :readonly="!$auth.loggedIn"
                :path="'/platforms/copy/' + item.id"
              />
              <DotMenuActionDelete
                :readonly="!$auth.loggedIn"
                @click="initDeleteDialog(item)"
              />
            </template>
          </PlatformsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <PlatformDeleteDialog
      v-model="showDeleteDialog"
      :platform-to-delete="platformToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <v-btn
      v-if="$auth.loggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/platforms/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import { mapState, mapActions } from 'vuex'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformDeleteDialog from '@/components/platforms/PlatformDeleteDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import PlatformsBasicSearch from '@/components/platforms/PlatformsBasicSearch.vue'
import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IPlatformSearchParams, PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'

@Component({
  components: {
    PlatformsBasicSearchField,
    PlatformsBasicSearch,
    PlatformsListItem,
    BaseList,
    DotMenuActionDelete,
    DotMenuActionCopy,
    PlatformDeleteDialog,
    ManufacturerSelect,
    PlatformTypeSelect,
    StatusSelect
  },
  computed: {
    ...mapState('vocabulary', ['platformtypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('platforms', ['platforms', 'pageNumber', 'pageSize', 'totalPages'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadEquipmentstatus', 'loadPlatformtypes', 'loadManufacturers']),
    ...mapActions('platforms', ['searchPlatformsPaginated', 'setPageNumber', 'exportAsCsv', 'deletePlatform']),
    ...mapActions('appbar', ['initPlatformsIndexAppBar', 'setDefaults'])
  }
})
export default class SearchPlatformsPage extends Vue {
  private loading: boolean = true
  private processing: boolean = false

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []
  private onlyOwnPlatforms: boolean = false

  private searchText: string | null = null

  private showDeleteDialog: boolean = false

  private platformToDelete: Platform | null = null

  // vuex definition for typescript check
  loadEquipmentstatus!:()=>void
  loadPlatformtypes!:()=>void
  loadManufacturers!:()=>void
  initPlatformsIndexAppBar!:()=>void
  setDefaults!:()=>void
  pageNumber!:number
  setPageNumber!:(newPageNumber: number)=>void
  searchPlatformsPaginated!:(searchParams: IPlatformSearchParams)=>void
  platforms!:Platform[]
  exportAsCsv!:(searchParams: IPlatformSearchParams)=> Promise<Blob>
  deletePlatform!:(id:string)=>void
  platformtypes!:  PlatformType[]
  manufacturers!:  Manufacturer[]
  equipmentstatus!: Status[]


  async created () {
    try {
      this.loading = true
      await this.loadEquipmentstatus()
      await this.loadPlatformtypes()
      await this.loadManufacturers()
      await this.initPlatformsIndexAppBar()
      await this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.loading = false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
    this.setPageNumber(newVal)
    this.setPageInUrl(false)
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  get searchParams () {
    return {
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchPlatformTypes,
      onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnPlatforms === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchPlatformTypes.length ||
      !!this.selectedSearchManufacturers.length
  }

  async runInitialSearch (): Promise<void> {
    this.activeTab = this.isExtendedSearch() ? 1 : 0

    this.page = this.getPageFromUrl()

    await this.runSearch()
  }

  basicSearch (){
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch () {
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
    this.initUrlQueryParams()
  }

  async runSearch () {
    try {
      this.loading = true
      this.initUrlQueryParams()
      await this.searchPlatformsPaginated(this.searchParams)
      this.setPageInUrl()
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.loading = false
    }
  }

  async exportCsv () {
    if (this.platforms.length > 0) {
      try {
        this.processing = true
        const blob = await this.exportAsCsv(this.searchParams)
        saveAs(blob, 'platforms.csv')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'CSV export failed')
      } finally {
        this.processing = false
      }
    }
  }

  initDeleteDialog (platform: Platform) {
    this.showDeleteDialog = true
    this.platformToDelete = platform
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.platformToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.platformToDelete === null || this.platformToDelete.id === null) {
      return
    }
    try {
      this.loading = true
      await this.deletePlatform(this.platformToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new PlatformSearchParamsSerializer({
      states: this.equipmentstatus,
      platformTypes: this.platformtypes,
      manufacturer: this.manufacturers
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnPlatforms) {
      this.onlyOwnPlatforms = searchParamsObject.onlyOwnPlatforms
    }
    if (searchParamsObject.manufacturer) {
      this.selectedSearchManufacturers = searchParamsObject.manufacturer
    }
    if (searchParamsObject.types) {
      this.selectedSearchPlatformTypes = searchParamsObject.types
    }
    if (searchParamsObject.states) {
      this.selectedSearchStates = searchParamsObject.states
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new PlatformSearchParamsSerializer()).toQueryParams(this.searchParams),
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
</style>
