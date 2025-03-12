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
          placeholder="Search devices"
          hint="Please enter at least 3 characters"
          @keydown.enter="search"
        />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <StatusSelect v-model="selectedSearchStates" label="Select a status" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <DeviceTypeSelect v-model="selectedSearchDeviceTypes" label="Select a device type" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <permission-group-search-select v-model="selectedSearchPermissionGroups" label="Select a permission group" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col v-if="$auth.loggedIn" cols="12" md="3">
        <v-checkbox v-model="onlyOwnDevices" label="Only own devices" />
      </v-col>
      <v-col cols="12" md="3">
        <v-checkbox v-model="includeArchivedDevices" label="Include archived devices" />
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
import DeviceTypeSelect from '@/components/DeviceTypeSelect.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { DeviceType } from '@/models/DeviceType'
import { PermissionGroup } from '@/models/PermissionGroup'
import { SearchDevicesPaginatedAction } from '@/store/devices'

@Component({
  components: { ManufacturerSelect, DeviceTypeSelect, PermissionGroupSearchSelect, StatusSelect },
  methods: {
    ...mapActions('devices', ['searchDevicesPaginated']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceExtendedSearch extends Vue {
  private searchText: string | null = null
  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []
  private selectedSearchPermissionGroups: PermissionGroup[] = []
  private onlyOwnDevices: boolean = false
  private includeArchivedDevices: boolean = false

  // vuex
  setLoading!: SetLoadingAction
  searchDevicesPaginated!: SearchDevicesPaginatedAction

  public async search () {
    try {
      this.setLoading(true)
      await this.searchDevicesPaginated({
        searchText: this.searchText,
        manufacturer: this.selectedSearchManufacturers,
        states: this.selectedSearchStates,
        types: this.selectedSearchDeviceTypes,
        permissionGroups: this.selectedSearchPermissionGroups,
        onlyOwnDevices: this.onlyOwnDevices,
        includeArchivedDevices: this.includeArchivedDevices,
        manufacturerName: null,
        model: null
      })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.setLoading(false)
      this.$emit('search-finished')
    }
  }

  clearSearch () {
    this.searchText = null
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
    this.selectedSearchPermissionGroups = []
    this.onlyOwnDevices = false
    this.includeArchivedDevices = false
  }
}
</script>

<style scoped>

</style>
