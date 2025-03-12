<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="50vw"
    @click:outside="$emit('cancel')"
  >
    <ProgressIndicator
      :value="isLoading"
    />
    <v-card>
      <v-card-title>
        Select entity for exchange
      </v-card-title>
      <v-card-text>
        <v-card flat>
          <v-tabs v-model="tab">
            <v-tab>Basic Search</v-tab>
            <v-tab>Extended Search</v-tab>
            <v-tabs-items v-model="tab">
              <v-tab-item>
                <DeviceBasicSearch
                  ref="deviceBasicSearch"
                  @search-finished="checkDeviceAvailabilities"
                />
              </v-tab-item>
              <v-tab-item>
                <DeviceExtendedSearch
                  ref="deviceExtendedSearch"
                  @search-finished="checkDeviceAvailabilities"
                />
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>

          <v-row
            no-gutters
            class="mt-10"
          >
            <v-col
              cols="12"
              md="3"
            >
              <DeviceFoundEntries />
            </v-col>
            <v-spacer />
            <v-col
              cols="12"
              md="6"
            >
              <DevicePagination
                ref="devicePagination"
                @input="updateSearch"
              />
            </v-col>
            <v-col
              cols="12"
              md="3"
              class="flex-grow-1 flex-shrink-0"
            >
              <v-subheader>
                <DevicePageSizeSelect
                  @input="setPageAndUpdateSearch"
                />
              </v-subheader>
            </v-col>
          </v-row>
          <ReuseDeviceExchangeList
            v-show="availabilitiesChecked"
            :devices-used-in-tree="devicesUsedInTree"
            @selected="emitSelectedDevice"
          />
        </v-card>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          @click="showDialog=false"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { DateTime } from 'luxon'
import DevicePagination from '@/components/devices/DevicePagination.vue'
import DevicePageSizeSelect from '@/components/devices/DevicePageSizeSelect.vue'
import DeviceBasicSearch from '@/components/devices/DeviceBasicSearch.vue'
import ReuseDeviceExchangeList from '@/components/configurations/reuseMounts/ReuseDeviceExchangeList.vue'
import { Device } from '@/models/Device'
import { DevicesState, LoadDeviceAvailabilitiesAction } from '@/store/devices'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DeviceFoundEntries from '@/components/devices/DeviceFoundEntries.vue'
import DeviceExtendedSearch from '@/components/devices/DeviceExtendedSearch.vue'

@Component({
  components: {
    DeviceExtendedSearch,
    DeviceFoundEntries,
    ProgressIndicator,
    ReuseDeviceExchangeList,
    DeviceBasicSearch,
    DevicePageSizeSelect,
    DevicePagination
  },
  computed: {
    ...mapState('devices', ['devices', 'deviceAvailabilities']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceAvailabilities'])
  }
})
export default class ReuseDeviceExchangeDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: true,
    type: Object
  })
  readonly beginDate!: DateTime

  @Prop({
    required: true
  })
  readonly devicesUsedInTree!: Device[]

  @Prop({
    required: false,
    type: Object,
    default: null
  })
  readonly endDate!: DateTime | null

  private tab = 0
  private availabilitiesChecked = false

  devices!: DevicesState['devices']
  loadDeviceAvailabilities!: LoadDeviceAvailabilitiesAction

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async checkDeviceAvailabilities () {
    try {
      const ids = this.devices.filter((device) => {
        const found = this.devicesUsedInTree.find(el => el.id === device.id)
        return !found
      }).map((entity: Device) => entity.id)

      await this.loadDeviceAvailabilities({ ids, from: this.beginDate, until: this.endDate })
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of availabilities failed')
    } finally {
      this.availabilitiesChecked = true
    }
  }

  updateSearch () {
    if (this.tab === 0) {
      (this.$refs.deviceBasicSearch as Vue & { search: () => void }).search()
    } else if (this.tab === 1) {
      (this.$refs.deviceExtendedSearch as Vue & { search: () => void }).search()
    }
  }

  setPageAndUpdateSearch () {
    (this.$refs.devicePagination as Vue & { setPage: (val: number) => void }).setPage(1)
    this.updateSearch()
  }

  emitSelectedDevice (device: Device) {
    this.$emit('selected', device)
  }

  @Watch('showDialog')
  async onShowDialogChanged () {
    if (this.showDialog) {
      this.availabilitiesChecked = false
      await this.$nextTick()
      this.updateSearch()
    }
  }
}
</script>

<style scoped>

</style>
