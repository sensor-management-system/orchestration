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
    <v-row>
      <v-col cols="12" md="5">
        <v-text-field
          v-model="searchText"
          label="Name"
          placeholder="Search devices"
          hint="Please enter at least 3 characters"
          @keydown.enter="search"
        />
      </v-col>
      <v-col
        cols="12"
        md="5"
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
import { SetLoadingAction } from '@/store/progressindicator'
import { SearchDevicesPaginatedAction } from '@/store/devices'

@Component({
  methods: {
    ...mapActions('devices', ['searchDevicesPaginated']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceBasicSearch extends Vue {
  private searchText: string = ''

  setLoading!: SetLoadingAction
  searchDevicesPaginated!: SearchDevicesPaginatedAction

  public async search () {
    try {
      this.setLoading(true)
      await this.searchDevicesPaginated({
        searchText: this.searchText,
        manufacturer: [],
        states: [],
        types: [],
        permissionGroups: [],
        onlyOwnDevices: false,
        includeArchivedDevices: false,
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
    this.searchText = ''
  }
}
</script>

<style scoped>

</style>
