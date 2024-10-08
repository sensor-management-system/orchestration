<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-tabs-items
      v-model="activeTab"
    >
      <v-tab-item :eager="true">
        <v-row
          dense
        >
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchedText"
              label="Search term"
              placeholder="Search platforms"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
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
        <v-row
          dense
        >
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchedText"
              label="Search term"
              placeholder="Search platforms"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <ManufacturerSelect v-model="selectedManufacturers" label="Select a manufacturer" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <StatusSelect v-model="selectedStates" label="Select a status" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <PlatformTypeSelect v-model="selectedPlatformTypes" label="Select a platform type" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <permission-group-search-select v-model="selectedPermissionGroups" label="Select a permission group" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col v-if="$auth.loggedIn" cols="12" md="3">
            <v-checkbox v-model="selectOnlyOwnPlatforms" label="Only own platforms" />
          </v-col>
          <v-col cols="12" md="3">
            <v-checkbox v-model="selectIncludeArchivedPlatforms" label="Include archived platforms" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
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
  SetSelectedSearchPermissionGroupsAction,
  SetOnlyOwnPlatformsAction,
  SetSearchTextAction,
  SetIncludeArchivedPlatformsAction
} from '@/store/platforms'

import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { PermissionsState, LoadPermissionGroupsAction } from '@/store/permissions'
import { SetActiveTabAction, SetBackToAction } from '@/store/appbar'

@Component({
  components: { PlatformTypeSelect, StatusSelect, ManufacturerSelect, PermissionGroupSearchSelect },
  computed: {
    ...mapState('vocabulary', ['platformtypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('platforms', [
      'selectedSearchManufacturers',
      'selectedSearchStates',
      'selectedSearchPlatformTypes',
      'selectedSearchPermissionGroups',
      'onlyOwnPlatforms',
      'includeArchivedPlatforms',
      'searchText'
    ]),
    ...mapGetters('platforms', ['searchParams']),
    ...mapGetters('permissions', ['permissionGroups'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('vocabulary', ['loadEquipmentstatus', 'loadPlatformtypes', 'loadManufacturers']),
    ...mapActions('platforms', [
      'searchPlatformsPaginated',
      'setPageNumber',
      'setPageSize',
      'setSelectedSearchManufacturers',
      'setSelectedSearchStates',
      'setSelectedSearchPlatformTypes',
      'setSelectedSearchPermissionGroups',
      'setOnlyOwnPlatforms',
      'setIncludeArchivedPlatforms',
      'setSearchText'
    ]),
    ...mapActions('permissions', ['loadPermissionGroups']),
    ...mapActions('appbar', ['setActiveTab', 'setBackTo'])
  }
})
export default class PlatformSearch extends Vue {
  // vuex definition for typescript check
  selectedSearchManufacturers!: PlatformsState['selectedSearchManufacturers']
  selectedSearchStates!: PlatformsState['selectedSearchStates']
  selectedSearchPlatformTypes!: PlatformsState['selectedSearchPlatformTypes']
  selectedSearchPermissionGroups!: PlatformsState['selectedSearchPermissionGroups']
  onlyOwnPlatforms!: PlatformsState['onlyOwnPlatforms']
  searchText!: PlatformsState['searchText']
  includeArchivedPlatforms!: PlatformsState['includeArchivedPlatforms']
  setSelectedSearchManufacturers!: SetSelectedSearchManufacturersAction
  setSelectedSearchStates!: SetSelectedSearchStatesAction
  setSelectedSearchPlatformTypes!: SetSelectedSearchPlatformTypesAction
  setSelectedSearchPermissionGroups!: SetSelectedSearchPermissionGroupsAction
  setOnlyOwnPlatforms!: SetOnlyOwnPlatformsAction
  setIncludeArchivedPlatforms!: SetIncludeArchivedPlatformsAction
  setSearchText!: SetSearchTextAction
  loadEquipmentstatus!: LoadEquipmentstatusAction
  loadPlatformtypes!: LoadPlatformtypesAction
  loadManufacturers!: LoadManufacturersAction
  loadPermissionGroups!: LoadPermissionGroupsAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  searchParams!: SearchParamsGetter
  equipmentstatus!: VocabularyState['equipmentstatus']
  platformtypes!: VocabularyState['platformtypes']
  manufacturers!: VocabularyState['manufacturers']
  permissionGroups!: PermissionsState['permissionGroups']
  setActiveTab!: SetActiveTabAction
  setLoading!: SetLoadingAction
  setBackTo!: SetBackToAction

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

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

  get selectedPermissionGroups () {
    return this.selectedSearchPermissionGroups
  }

  set selectedPermissionGroups (newVal) {
    this.setSelectedSearchPermissionGroups(newVal)
  }

  get selectOnlyOwnPlatforms () {
    return this.onlyOwnPlatforms
  }

  set selectOnlyOwnPlatforms (newVal) {
    this.setOnlyOwnPlatforms(newVal)
  }

  get selectIncludeArchivedPlatforms () {
    return this.includeArchivedPlatforms
  }

  set selectIncludeArchivedPlatforms (newValue: boolean) {
    this.setIncludeArchivedPlatforms(newValue)
  }

  get searchedText () {
    return this.searchText
  }

  set searchedText (newVal) {
    this.setSearchText(newVal)
  }

  created () {
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectedPermissionGroups = []
    this.selectOnlyOwnPlatforms = false
    this.selectIncludeArchivedPlatforms = false
    this.searchedText = ''
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadEquipmentstatus(),
        this.loadPlatformtypes(),
        this.loadManufacturers(),
        this.loadPermissionGroups()
      ])
      this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnPlatforms === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchPlatformTypes.length ||
      !!this.selectedSearchManufacturers.length ||
      !!this.selectedSearchPermissionGroups.length ||
      this.includeArchivedPlatforms === true
  }

  async runInitialSearch (): Promise<void> {
    this.setActiveTab(this.isExtendedSearch() ? 1 : 0)
    await this.searchPlatformsPaginated()
    this.setBackTo({ path: this.$route.path, query: this.$route.query })
  }

  basicSearch () {
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectOnlyOwnPlatforms = false
    this.selectIncludeArchivedPlatforms = false
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
    this.selectedPermissionGroups = []
    this.selectOnlyOwnPlatforms = false
    this.selectIncludeArchivedPlatforms = false
    this.$emit('clear-extended-search')
  }

  async runSearch () {
    try {
      this.setLoading(true)
      this.setPageNumber(1) // important for query
      this.initUrlQueryParams()
      await this.searchPlatformsPaginated()
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new PlatformSearchParamsSerializer({
      states: this.equipmentstatus,
      platformTypes: this.platformtypes,
      manufacturer: this.manufacturers,
      permissionGroups: this.permissionGroups
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchedText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnPlatforms) {
      this.selectOnlyOwnPlatforms = searchParamsObject.onlyOwnPlatforms
    }
    if (searchParamsObject.includeArchivedPlatforms) {
      this.selectIncludeArchivedPlatforms = searchParamsObject.includeArchivedPlatforms
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
    if (searchParamsObject.permissionGroups) {
      this.selectedPermissionGroups = searchParamsObject.permissionGroups
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
