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
    <PlatformSearch
      @basic-search="runSearch"
      @extended-search="runSearch"
    />
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

import {mapState,mapActions} from 'vuex'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformDeleteDialog from '@/components/platforms/PlatformDeleteDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IPlatformSearchParams, PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import PlatformsBasicSearch from '@/components/platforms/PlatformsBasicSearch.vue'
import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'
import PlatformSearch from '@/components/platforms/PlatformSearch.vue'
import { DeviceSearchParamsSerializer } from '@/modelUtils/DeviceSearchParams'

@Component({
  components: {
    PlatformSearch,
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
  computed:{
    ...mapState('vocabulary',['platformtypes','manufacturers','equipmentstatus']),
    ...mapState('platforms',['platforms','pageNumber','pageSize','totalPages'])
  },
  methods:{
    ...mapActions('vocabulary',['loadEquipmentstatus','loadPlatformtypes','loadManufacturers']),
    ...mapActions('platforms',['searchPlatformsPaginated','setPageNumber','exportAsCsv','deletePlatform'])
  }
})
export default class SearchPlatformsPage extends Vue {
  private loading: boolean = true
  private processing: boolean = false

  private showDeleteDialog: boolean = false

  private platformToDelete: Platform | null = null

  async created () {
    // await this.initializeAppBar()
    await this.loadEquipmentstatus();
    await this.loadPlatformtypes();
    await this.loadManufacturers();

    await this.initSearchQueryParams(this.$route.query)
    await this.runInitialSearch()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }


  get page(){
    return this.pageNumber;
  }

  set page(newVal){
    this.setPageNumber(newVal);
  }

  // isExtendedSearch (): boolean {
  //   return this.onlyOwnPlatforms === true ||
  //     !!this.selectedSearchStates.length ||
  //     !!this.selectedSearchPlatformTypes.length ||
  //     !!this.selectedSearchManufacturers.length
  // }

  async runInitialSearch (): Promise<void> {
    // this.activeTab = this.isExtendedSearch() ? 1 : 0

    this.page = this.getPageFromUrl()

    await this.runSearch(
      {
        searchText: '',
        manufacturer: [],
        states: [],
        types: [],
        onlyOwnPlatforms: false
      }
    )
  }

  get searchParams(){
    return {
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchPlatformTypes,
      onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
    }
  }

  async runSearch (searchParams:IPlatformSearchParams): Promise<void> {
    this.initUrlQueryParams()
    this.loading = true
    try {
      this.searchPlatformsPaginated(searchParams);
      this.setPageInUrl(this.page)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.loading = false
    }
  }

  exportCsv () {
    if(this.platforms.length>0){
      this.processing=true
      this.exportAsCsv(this.searchParams).then((blob) => {
        saveAs(blob, 'platforms.csv')
      }).catch((_err) => {
        this.$store.commit('snackbar/setError', 'CSV export failed')
      }).finally(()=>{
        this.processing = false
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

  // initSearchQueryParams (params: QueryParams): void {
  //   const searchParamsObject = (new PlatformSearchParamsSerializer({
  //     states: this.states,
  //     platformTypes: this.platformTypes,
  //     manufacturer: this.manufacturer
  //   })).toSearchParams(params)
  //
  //   // prefill the form by the serialized search params from the URL
  //   if (searchParamsObject.searchText) {
  //     this.searchText = searchParamsObject.searchText
  //   }
  //   if (searchParamsObject.onlyOwnPlatforms) {
  //     this.onlyOwnPlatforms = searchParamsObject.onlyOwnPlatforms
  //   }
  //   if (searchParamsObject.manufacturer) {
  //     this.selectedSearchManufacturers = searchParamsObject.manufacturer
  //   }
  //   if (searchParamsObject.types) {
  //     this.selectedSearchPlatformTypes = searchParamsObject.types
  //   }
  //   if (searchParamsObject.states) {
  //     this.selectedSearchStates = searchParamsObject.states
  //   }
  // }

  // initUrlQueryParams (): void { // todo scheint aktuell nicht zu funktionieren, noch keine Ahnung warum. Er pushed nicht zur route
  //   this.$router.push({
  //     query: (new PlatformSearchParamsSerializer()).toQueryParams(this.searchParams),
  //     hash: this.$route.hash
  //   })
  // }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page)
    }
    return 1
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
