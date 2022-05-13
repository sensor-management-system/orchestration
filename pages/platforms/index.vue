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
    <div>
      <PlatformSearch>
        <template #actions>
          <v-btn
            v-if="$auth.loggedIn"
            color="accent"
            small
            nuxt
            to="/platforms/new"
          >
            New Platform
          </v-btn>
        </template>
      </PlatformSearch>
    </div>
<!--    <v-tabs-items-->
<!--      v-model="activeTab"-->
<!--    >-->
<!--      <PlatformsBasicSearch-->
<!--        v-model="searchText"-->
<!--        @search="basicSearch"-->
<!--        @clear="clearBasicSearch"-->
<!--      />-->
<!--      <v-tab-item :eager="true">-->
<!--        <v-row>-->
<!--          <v-col cols="12" md="6">-->
<!--            <PlatformsBasicSearchField-->
<!--              v-model="searchText"-->
<!--              @start-search="extendedSearch"-->
<!--            />-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row>-->
<!--          <v-col cols="12" md="3">-->
<!--            <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row>-->
<!--          <v-col cols="12" md="3">-->
<!--            <StatusSelect v-model="selectedSearchStates" label="Select a status" />-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row>-->
<!--          <v-col cols="12" md="3">-->
<!--            <PlatformTypeSelect v-model="selectedSearchPlatformTypes" label="Select a platform type" />-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row v-if="$auth.loggedIn">-->
<!--          <v-col cols="12" md="3">-->
<!--            <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row>-->
<!--          <v-col-->
<!--            cols="12"-->
<!--            align-self="center"-->
<!--          >-->
<!--            <v-btn-->
<!--              color="primary"-->
<!--              small-->
<!--              @click="extendedSearch"-->
<!--            >-->
<!--              Search-->
<!--            </v-btn>-->
<!--            <v-btn-->
<!--              text-->
<!--              small-->
<!--              @click="clearExtendedSearch"-->
<!--            >-->
<!--              Clear-->
<!--            </v-btn>-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--      </v-tab-item>-->
<!--    </v-tabs-items>-->

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
      <v-row
        no-gutters
      >
        <v-col
          cols="12"
          md="10"
          offset-md="1"
        >
          <v-pagination
            v-model="page"
            :disabled="loading"
            :length="totalPages"
            :total-visible="7"
            @input="searchPlatformsPaginated"
          />
        </v-col>
        <v-col
          cols="1"
          offset="11"
          offset-md="0"
        >
          <page-size-select
            v-model="size"
            :items="pageSizeItems"
          />
        </v-col>
      </v-row>
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
        @input="searchPlatformsPaginated"
      />
    </div>
    <PlatformDeleteDialog
      v-model="showDeleteDialog"
      :platform-to-delete="platformToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import { mapActions, mapState, mapGetters } from 'vuex'

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
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IPlatformSearchParams, PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
import PlatformSearch from '@/components/platforms/PlatformSearch.vue'

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
    StatusSelect,
    PageSizeSelect
  },
  middleware: ['permission'],
  computed: {
    ...mapState('platforms', ['platforms', 'pageNumber', 'pageSize', 'totalPages']),
    ...mapGetters('platforms', ['pageSizes'])
  },
  methods: {
    ...mapActions('platforms', ['searchPlatformsPaginated', 'setPageNumber', 'setPageSize', 'exportAsCsv', 'deletePlatform']),
    ...mapActions('appbar', ['initPlatformsIndexAppBar', 'setDefaults'])
  }
})
export default class SearchPlatformsPage extends Vue {
  private loading: boolean = true
  private processing: boolean = false

  private showDeleteDialog: boolean = false

  private platformToDelete: Platform | null = null

  // vuex definition for typescript check
  initPlatformsIndexAppBar!: () => void
  setDefaults!: () => void
  pageNumber!: number
  setPageNumber!: (newPageNumber: number) => void
  pageSize!: number
  setPageSize!: (newPageSize: number) => void
  pageSizes!: number[]
  searchPlatformsPaginated!: (searchParams: IPlatformSearchParams) => void
  platforms!: Platform[]
  exportAsCsv!: (searchParams: IPlatformSearchParams) => Promise<Blob>
  deletePlatform!: (id: string) => void
  platformtypes!: PlatformType[]
  manufacturers!: Manufacturer[]
  equipmentstatus!: Status[]

  async created () {
    try {
      this.loading = true
      await this.initPlatformsIndexAppBar()
      this.page = this.getPageFromUrl()
      this.size = this.getSizeFromUrl()
      await this.searchPlatformsPaginated()
    } catch (e) {
      console.log('e',e);
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

  get size (): number {
    return this.pageSize
  }

  set size (newVal: number) {
    this.setPageSize(newVal)
    this.setSizeInUrl(false)
    this.searchPlatformsPaginated()
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
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
