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
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchText"
              label="Name"
              placeholder="Name of platform"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
            cols="12"
            md="7"
            align-self="center"
          >
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
        </v-row>
      </v-tab-item>
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Name"
              placeholder="Name of platform"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
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

        <template v-if="lastActiveSearcher != null">
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
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
      />
      <BaseList
        :list-items="platforms"
      >
        <template v-slot:list-item="{item}">
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
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
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

import {mapState,mapActions} from 'vuex'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import PlatformDeleteDialog from '@/components/platforms/PlatformDeleteDialog.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

import { PlatformSearcher } from '@/services/sms/PlatformApi'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IPlatformSearchParams, PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'

type PaginatedResult = {
    [page: number]: Platform[]
}

@Component({
  components: {
    PlatformsListItem,
    BaseList,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenu,
    PlatformDeleteDialog,
    ManufacturerSelect,
    PlatformTypeSelect,
    StatusBadge,
    StatusSelect
  },
  computed:{
    ...mapState('vocabulary',['platformtypes','manufacturers','equipmentstatus']),
    ...mapState('platforms',['platforms'])
  },
  methods:{
    ...mapActions('vocabulary',['loadEquipmentstatus','loadPlatformtypes','loadManufacturers']),
    ...mapActions('platforms',['searchPlatformsPaginated'])
  }
})
export default class SearchPlatformsPage extends Vue {
  private pageSize: number = 20
  private loading: boolean = true
  private processing: boolean = false

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Platform> = null
  private lastActiveSearcher: PlatformSearcher | null = null
  private page: number = 0

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []
  private onlyOwnPlatforms: boolean = false

  // private manufacturer: Manufacturer[] = []
  // private states: Status[] = []
  // private platformTypes: PlatformType[] = []

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: PaginatedResult = {}
  private searchText: string | null = null

  private showDeleteDialog: boolean = false

  private searchResultItemsShown: { [id: string]: boolean } = {}

  public readonly NO_TYPE: string = 'Unknown type'

  private platformToDelete: Platform | null = null

  created () {
    this.initializeAppBar()
    this.loadEquipmentstatus();
    this.loadPlatformtypes();
    this.loadManufacturers();

  }

  async mounted () {
    // await this.fetchEntities()
    this.initSearchQueryParams(this.$route.query)
    this.runInitialSearch()
  }

  // async fetchEntities (): Promise<void> {
  //   const platformTypeLookup = new Map<string, PlatformType>()
  //   const statusLookup = new Map<string, Status>()
  //
  //   try {
  //     const [platformTypes, states, manufacturer] = await Promise.all([
  //       this.$api.platformTypes.findAll(),
  //       this.$api.states.findAll(),
  //       this.$api.manufacturer.findAll()
  //     ])
  //
  //     this.platformTypes = platformTypes
  //     this.states = states
  //     this.manufacturer = manufacturer
  //
  //     for (const platformType of platformTypes) {
  //       platformTypeLookup.set(platformType.uri, platformType)
  //     }
  //     for (const status of states) {
  //       statusLookup.set(status.uri, status)
  //     }
  //
  //     this.platformTypeLookup = platformTypeLookup
  //     this.statusLookup = statusLookup
  //   } catch (_error) {
  //     this.$store.commit('snackbar/setError', 'Loading of entities failed')
  //   }
  // }

  beforeDestroy () {
    this.unsetResultItemsShown()
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Search',
        'Extended Search'
      ],
      title: 'Platforms',
      saveBtnHidden: true,
      cancelBtnHidden: true
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnPlatforms === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchPlatformTypes.length ||
      !!this.selectedSearchManufacturers.length
  }

  async runInitialSearch (): Promise<void> {
    this.activeTab = this.isExtendedSearch() ? 1 : 0

    const page: number | undefined = this.getPageFromUrl()

    await this.runSearch(
      {
        searchText: this.searchText,
        manufacturer: this.selectedSearchManufacturers,
        states: this.selectedSearchStates,
        types: this.selectedSearchPlatformTypes,
        onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
      },
      page
    )
  }

  basicSearch (): Promise<void> {
    return this.runSearch({
      searchText: this.searchText,
      manufacturer: [],
      states: [],
      types: [],
      onlyOwnPlatforms: false
    })
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch (): Promise<void> {
    return this.runSearch({
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchPlatformTypes,
      onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
    })
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
  }

  async runSearch (
    searchParameters: IPlatformSearchParams,
    page: number = 1
  ): Promise<void> {
    this.initUrlQueryParams(searchParameters)

    this.totalCount = 0
    this.loading = true
    this.searchResults = {}
    this.unsetResultItemsShown()
    this.loader = null
    this.page = 0
    //
    // const searchBuilder = this.$api.platforms
    //   .newSearchBuilder()
    //   .withText(searchParameters.searchText)
    //   .withOneMatchingManufacturerOf(searchParameters.manufacturer)
    //   .withOneMatchingStatusOf(searchParameters.states)
    //   .withOneMatchingPlatformTypeOf(searchParameters.types)

    // if (searchParameters.onlyOwnPlatforms) {
    //   const email = this.$auth.user!.email as string
    //   if (email) {
    //     searchBuilder.withContactEmail(email)
    //   }
    // }

    // let filterSettings = [];
    // if (searchParameters.manufacturer.length > 0) {
    //   filterSettings.push({
    //     or: [
    //       {
    //         name: 'manufacturer_name',
    //         op: 'in_',
    //         val: searchParameters.manufacturer.map((m: Manufacturer) => m.name)
    //       },
    //       {
    //         name: 'manufacturer_uri',
    //         op: 'in_',
    //         val: searchParameters.manufacturer.map((m: Manufacturer) => m.uri)
    //       }
    //     ]
    //   })
    // }
    // if (searchParameters.states.length > 0) {
    //   filterSettings.push({
    //     or: [
    //       {
    //         name: 'status_name',
    //         op: 'in_',
    //         val: searchParameters.states.map((s: Status) => s.name)
    //       },
    //       {
    //         name: 'status_uri',
    //         op: 'in_',
    //         val: searchParameters.states.map((s: Status) => s.uri)
    //       }
    //     ]
    //   })
    // }
    // if (searchParameters.types.length > 0) {
    //   filterSettings.push({
    //     or: [
    //       {
    //         name: 'platform_type_name',
    //         op: 'in_',
    //         val: searchParameters.types.map((t: PlatformType) => t.name)
    //       },
    //       {
    //         name: 'platform_type_uri',
    //         op: 'in_',
    //         val: searchParameters.types.map((t: PlatformType) => t.uri)
    //       }
    //     ]
    //   })
    // }
    // if (searchParameters.onlyOwnPlatforms) {
    //   const email = this.$auth.user!.email as string
    //   if (email) {
    //     filterSettings.push({
    //       name: 'contacts.email',
    //       op: 'eq',
    //       val: email
    //     })
    //   }
    // }
    // //todo nicht vergessen:
    // //searchParameters.searchText
    //
    // let queryParams = {};
    // queryParams={
    //   filter:JSON.stringify(filterSettings)
    // }
    // if(searchParameters.searchText){
    //   queryParams.q = searchParameters.searchText
    // }
    // queryParams.sort='short_name';
    //
    // // this.lastActiveSearcher = searchBuilder.build()
    // console.log('searchParameters',searchParameters);
    // console.log('filterSettings',filterSettings);
    try {

      // if (searchParameters.onlyOwnPlatforms) {
      //   const email = this.$auth.user!.email as string
      //   if (email) {
      //     searchBuilder.withContactEmail(email)
      //   }
      // }

      this.searchPlatformsPaginated(searchParameters);
      // const loader = await this.lastActiveSearcher.findMatchingAsPaginationLoaderOnPage(page, this.pageSize)
      // this.loader = loader
      // this.searchResults[page] = loader.elements
      // this.totalCount = loader.totalCount
      // this.page = page
      // this.setPageInUrl(page)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.loading = false
    }
  }

  // async loadPage (pageNr: number, useCache: boolean = true) {
  //   // use the results that were already loaded if available
  //   if (useCache && this.searchResults[pageNr]) {
  //     return
  //   }
  //   if (this.loader != null && this.loader.funToLoadPage != null) {
  //     try {
  //       this.loading = true
  //       const loader = await this.loader.funToLoadPage(pageNr)
  //       this.loader = loader
  //       this.searchResults[pageNr] = loader.elements
  //       this.totalCount = loader.totalCount
  //     } catch (_error) {
  //       this.$store.commit('snackbar/setError', 'Loading of platforms failed')
  //     } finally {
  //       this.loading = false
  //     }
  //   }
  // }

  get numberOfPages (): number {
    return Math.ceil(this.totalCount / this.pageSize)
  }

  async setPage (page: number) {
    await this.loadPage(page)
    this.page = page
    this.setPageInUrl(page, false)
  }

  getSearchResultForPage (pageNr: number): Platform[] | undefined {
    return this.searchResults[pageNr]
  }

  exportCsv () {
    if (this.lastActiveSearcher != null) {
      this.processing = true
      this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
        this.processing = false
        saveAs(blob, 'platforms.csv')
      }).catch((_err) => {
        this.processing = false
        this.$store.commit('snackbar/setError', 'CSV export failed')
      })
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
    this.loading = true
    try {
      await this.$api.platforms.deleteById(this.platformToDelete.id)
      // if we know that the deleted platform was the last of the page, we
      // decrement the page by one
      if (this.getSearchResultForPage(this.page)?.length === 1) {
        this.page = this.page > 1 ? this.page - 1 : 1
      }
      this.loadPage(this.page, false)
      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  getType (platform: Platform) {
    if (this.platformTypeLookup.has(platform.platformTypeUri)) {
      const platformType: PlatformType = this.platformTypeLookup.get(platform.platformTypeUri) as PlatformType
      return platformType.name
    }
    if (platform.platformTypeName) {
      return platform.platformTypeName
    }
    return this.NO_TYPE
  }

  getStatus (platform: Platform) {
    if (this.statusLookup.has(platform.statusUri)) {
      const platformStatus: Status = this.statusLookup.get(platform.statusUri) as Status
      return platformStatus.name
    }
    if (platform.statusName) {
      return platform.statusName
    }
    return ''
  }

  showResultItem (id: string) {
    const show = !!this.searchResultItemsShown[id]
    Vue.set(this.searchResultItemsShown, id, !show)
  }

  isResultItemShown (id: string): boolean {
    return this.searchResultItemsShown[id]
  }

  unsetResultItemsShown (): void {
    this.searchResultItemsShown = {}
  }

  getTextOrDefault = (text: string): string => text || '-'

  initSearchQueryParams (params: QueryParams): void {
    const searchParamsObject = (new PlatformSearchParamsSerializer({
      states: this.states,
      platformTypes: this.platformTypes,
      manufacturer: this.manufacturer
    })).toSearchParams(params)

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

  initUrlQueryParams (params: IPlatformSearchParams): void {
    this.$router.push({
      query: (new PlatformSearchParamsSerializer()).toQueryParams(params),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 0
    }
  }

  setPageInUrl (page: number, preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(page)
      }
    } else {
      // remove page from the current url params
      const {
        // eslint-disable-next-line
        page,
        ...params
      } = this.$route.query
      query = params
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
