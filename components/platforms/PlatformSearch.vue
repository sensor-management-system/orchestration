<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-container>
      <v-tabs-items
        v-model="activeTab"
      >
        <v-tab-item :eager="true">
          <v-row>
            <v-col cols="12" md="5">
              <v-text-field
                v-model="searchedText"
                label="Search term"
                hint="Please enter at least 3 characters"
                @keydown.enter="basicSearch"
              />
            </v-col>
            <v-col
              cols="5"
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
            <v-col
              align-self="center"
              class="text-right"
            >
              <slot name="actions" />
            </v-col>
          </v-row>
        </v-tab-item>
        <v-tab-item :eager="true">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="searchedText"
                label="Search term"
                hint="Please enter at least 3 characters"
                @keydown.enter="extendedSearch"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="3">
              <ManufacturerSelect v-model="selectedManufacturers" label="Select a manufacturer" />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="3">
              <StatusSelect v-model="selectedStates" label="Select a status" />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="3">
              <PlatformTypeSelect v-model="selectedPlatformTypes" label="Select a platform type" />
            </v-col>
          </v-row>
          <v-row v-if="$auth.loggedIn">
            <v-col cols="12" md="3">
              <v-checkbox v-model="selectOnlyOwnPlatforms" label="Only own platforms" />
            </v-col>
          </v-row>
          <v-row>
            <v-col
              cols="5"
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
            <v-col
              align-self="center"
              class="text-right"
            >
              <slot name="actions" />
            </v-col>
          </v-row>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import {
  VocabularyState,
  LoadManufacturersAction,
  LoadPlatformtypesAction,
  LoadEquipmentstatusAction
} from '@/store/vocabulary'

import {
  PlatformsState,
  SearchParamsGetter,
  SearchPlatformsPaginatedAction,
  SetPageNumberAction,
  SetPageSizeAction,
  SetSelectedSearchManufacturersAction,
  SetSelectedSearchStatesAction,
  SetSelectedSearchPlatformTypesAction,
  SetOnlyOwnPlatformsAction,
  SetSearchTextAction
} from '@/store/platforms'

import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, PlatformTypeSelect, StatusSelect, ManufacturerSelect },
  computed: {
    ...mapState('vocabulary', ['platformtypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('platforms', ['selectedSearchManufacturers', 'selectedSearchStates', 'selectedSearchPlatformTypes', 'onlyOwnPlatforms', 'searchText']),
    ...mapGetters('platforms', ['searchParams'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadEquipmentstatus', 'loadPlatformtypes', 'loadManufacturers']),
    ...mapActions('platforms', [
      'searchPlatformsPaginated',
      'setPageNumber',
      'setPageSize',
      'setSelectedSearchManufacturers',
      'setSelectedSearchStates',
      'setSelectedSearchPlatformTypes',
      'setOnlyOwnPlatforms',
      'setSearchText'
    ]),
    ...mapActions('appbar', ['initPlatformsIndexAppBar', 'setDefaults'])
  }
})
export default class PlatformSearch extends Vue {
  private activeTab = 0
  private isLoading = false

  // vuex definition for typescript check
  selectedSearchManufacturers!: PlatformsState['selectedSearchManufacturers']
  selectedSearchStates!: PlatformsState['selectedSearchStates']
  selectedSearchPlatformTypes!: PlatformsState['selectedSearchPlatformTypes']
  onlyOwnPlatforms!: PlatformsState['onlyOwnPlatforms']
  searchText!: PlatformsState['searchText']
  setSelectedSearchManufacturers!: SetSelectedSearchManufacturersAction
  setSelectedSearchStates!: SetSelectedSearchStatesAction
  setSelectedSearchPlatformTypes!: SetSelectedSearchPlatformTypesAction
  setOnlyOwnPlatforms!: SetOnlyOwnPlatformsAction
  setSearchText!: SetSearchTextAction
  loadEquipmentstatus!: LoadEquipmentstatusAction
  loadPlatformtypes!: LoadPlatformtypesAction
  loadManufacturers!: LoadManufacturersAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  searchParams!: SearchParamsGetter
  equipmentstatus!: VocabularyState['equipmentstatus']
  platformtypes!: VocabularyState['platformtypes']
  manufacturers!: VocabularyState['manufacturers']

  get selectedManufacturers () {
    return this.selectedSearchManufacturers
  }

  set selectedManufacturers (newVal) {
    this.setSelectedSearchManufacturers(newVal)
  }

  get selectedStates () {
    return this.selectedSearchStates
  }

  set selectedStates (newVal) {
    this.setSelectedSearchStates(newVal)
  }

  get selectedPlatformTypes () {
    return this.selectedSearchPlatformTypes
  }

  set selectedPlatformTypes (newVal) {
    this.setSelectedSearchPlatformTypes(newVal)
  }

  get selectOnlyOwnPlatforms () {
    return this.onlyOwnPlatforms
  }

  set selectOnlyOwnPlatforms (newVal) {
    this.setOnlyOwnPlatforms(newVal)
  }

  get searchedText () {
    return this.searchText
  }

  set searchedText (newVal) {
    this.setSearchText(newVal)
  }

  async created () {
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await Promise.all([
        this.loadEquipmentstatus(),
        this.loadPlatformtypes(),
        this.loadManufacturers()
      ])
      this.initSearchQueryParams()
      // await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
    }
  }

  // get searchParams () {
  //   return {
  //     searchText: this.searchedText,
  //     manufacturer: this.selectedManufacturers,
  //     states: this.selectedStates,
  //     types: this.selectedPlatformTypes,
  //     onlyOwnPlatforms: this.selectOnlyOwnPlatforms && this.$auth.loggedIn
  //   }
  // }

  basicSearch () {
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectOnlyOwnPlatforms = false
    this.$emit('basic-search')
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchedText = null
    this.$emit('clear-basic-search')
  }

  extendedSearch () {
    this.$emit('extended-search')
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectOnlyOwnPlatforms = false
    this.$emit('clear-extended-search')
  }

  async runSearch () {
    try {
      this.isLoading = true
      this.setPageNumber(1) // important for query
      this.initUrlQueryParams()
      // await this.searchPlatformsPaginated(this.searchParams(this.$auth.loggedIn))
      await this.searchPlatformsPaginated()
      // this.setPageInUrl() // todo muss das eigentlich rein?
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
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
      this.searchedText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnPlatforms) {
      this.selectOnlyOwnPlatforms = searchParamsObject.onlyOwnPlatforms
    }
    if (searchParamsObject.manufacturer) {
      this.selectedManufacturers = searchParamsObject.manufacturer
    }
    if (searchParamsObject.types) {
      this.selectedPlatformTypes = searchParamsObject.types
    }
    if (searchParamsObject.states) {
      this.selectedStates = searchParamsObject.states
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new PlatformSearchParamsSerializer()).toQueryParams(this.searchParams(this.$auth.loggedIn)),
      hash: this.$route.hash
    })
  }
}
</script>

<style scoped>

</style>
