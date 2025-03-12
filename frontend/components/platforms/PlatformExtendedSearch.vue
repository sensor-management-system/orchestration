<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-container>
    <v-row
      dense
    >
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchText"
          label="Search term"
          placeholder="Search platforms"
          hint="Please enter at least 3 characters"
          @keydown.enter="search"
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
        <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />
      </v-col>
      <v-col cols="12" md="3">
        <v-checkbox v-model="includeArchivedPlatforms" label="Include archived platforms" />
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
          @click="search"
        >
          Search
        </v-btn>
        <v-btn
          text
          small
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import StatusSelect from '@/components/StatusSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import { PermissionGroup } from '@/models/PermissionGroup'
import { SearchPlatformsPaginatedAction } from '@/store/platforms'
import { SetLoadingAction } from '@/store/progressindicator'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import { Manufacturer } from '@/models/Manufacturer'

@Component({
  components: { PlatformTypeSelect, ManufacturerSelect, PermissionGroupSearchSelect, StatusSelect },
  methods: {
    ...mapActions('platforms', ['searchPlatformsPaginated']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformExtendedSearch extends Vue {
  private searchText: string | null = null
  private selectedManufacturers: Manufacturer[] = []
  private selectedStates: Status[] = []
  private selectedPlatformTypes: PlatformType[] = []
  private selectedPermissionGroups: PermissionGroup[] = []
  private onlyOwnPlatforms: boolean = false
  private includeArchivedPlatforms: boolean = false

  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  setLoading!: SetLoadingAction

  public async search () {
    try {
      this.setLoading(true)
      await this.searchPlatformsPaginated({
        searchText: this.searchText,
        manufacturer: this.selectedManufacturers,
        states: this.selectedStates,
        types: this.selectedPlatformTypes,
        permissionGroups: this.selectedPermissionGroups,
        onlyOwnPlatforms: this.onlyOwnPlatforms,
        includeArchivedPlatforms: this.includeArchivedPlatforms,
        manufacturerName: null,
        model: null
      })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
      this.$emit('search-finished')
    }
  }

  clearSearch () {
    this.searchText = null
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectedPermissionGroups = []
    this.onlyOwnPlatforms = false
    this.includeArchivedPlatforms = false
  }
}
</script>

<style scoped>

</style>
