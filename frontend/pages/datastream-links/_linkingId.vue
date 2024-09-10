<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <template v-if="tsmLinking">
      <v-card flat>
        <v-data-table
          :headers="headers"
          :items="dataTableLinkings"
          :expanded="dataTableLinkings"
          sort-by="device"
          class="elevation-1"
          show-expand
          hide-default-footer
        >
          <template #[`item.deviceName`]="{ item }">
            <ExtendedItemName :value="item.device" />
          </template>
          <template #[`item.licenseName`]="{ item }">
            {{ item.licenseName }}
            <a v-if="item.licenseUri" target="_blank" :href="item.licenseUri">
              <v-icon small>
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
          <template #expanded-item="{ headers, item }">
            <td :colspan="headers.length">
              <tsm-linking-basic-data-table
                :linking="item"
              />
            </td>
          </template>
        </v-data-table>
      </v-card>
    </template>
    <template v-else>
      <hint-card v-if="needLogin">
        Please log in to see the datastream link.
      </hint-card>
      <hint-card v-else>
        There is no such datastream link.
      </hint-card>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import HintCard from '@/components/HintCard.vue'
import TsmLinkingBasicDataTable from '@/components/configurations/tsmLinking/TsmLinkingBasicDataTable.vue'

import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TsmLinking } from '@/models/TsmLinking'
import { SetTitleAction } from '@/store/appbar'

@Component({
  components: {
    ExtendedItemName,
    HintCard,
    TsmLinkingBasicDataTable
  },
  methods: {
    ...mapActions('appbar', ['setTitle'])
  }
})
export default class DatastreamLinkIdPage extends Vue {
  private headers = [
    {
      text: 'TSM::Datasource::Thing::Datastream',
      value: 'tsmdlEntityNames'
    },
    {
      text: 'Device',
      value: 'deviceName'
    }, {
      text: 'Measured Quantity',
      value: 'measuredQuantity'
    },
    {
      text: 'Offsets (X | Y | Z)',
      value: 'offsets'
    },
    {
      text: 'Start date',
      value: 'startDate'
    },
    {
      text: 'End date',
      value: 'endDate'
    },
    {
      text: 'License',
      value: 'licenseName'
    },
    {
      text: 'Aggregation',
      value: 'aggregationText'
    }
  ]

  private tsmLinking: TsmLinking | null = null
  private needLogin = false

  setTitle!: SetTitleAction

  created () {
    this.initializeAppBar()
  }

  async fetch () {
    try {
      this.tsmLinking = await this.$api.tsmLinkings.findById(this.linkingId)
    } catch (e) {
      const errorData = JSON.parse(JSON.stringify(e))
      if (errorData.status === 401) {
        this.$store.commit('snackbar/setWarning', 'Please log in to see the datastream link.')
        this.needLogin = true
      }
    }
  }

  get linkingId (): string {
    return this.$route.params.linkingId
  }

  get dataTableLinkings (): Array<any> {
    const dataTableLinkings: Array<any> = [this.tsmLinking]
    return dataTableLinkings.map((linking: TsmLinking) => {
      return {
        id: linking.id,
        tsmdlEntityNames: this.generateTsmdlEntityNames(linking),
        offsets: `(${linking?.deviceMountAction?.offsetX} | ${linking?.deviceMountAction?.offsetY} | ${linking?.deviceMountAction?.offsetZ})`,
        startDate: this.$root.$options.filters!.toUtcDateTimeStringHHMM(linking.startDate),
        endDate: this.$root.$options.filters!.toUtcDateTimeStringHHMM(linking.endDate),
        measuredQuantity: this.generatePropertyTitle(linking.deviceProperty),
        device: linking.device,
        deviceName: this.getDeviceName(linking.device),
        datasource: linking.datasource,
        datastream: linking.datastream,
        thing: linking.thing,
        tsmEndpoint: linking.tsmEndpoint,
        licenseName: linking.licenseName,
        licenseUri: linking.licenseUri,
        aggregationText: linking.aggregationText
      }
    })
  }

  generatePropertyTitle (measuredQuantity: DeviceProperty | null) {
    if (measuredQuantity) {
      const propertyName = measuredQuantity.propertyName ?? ''
      const label = measuredQuantity.label ?? ''
      const unit = measuredQuantity.unitName ?? ''
      return `${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
    }
    return ''
  }

  getDeviceName (value: Device | null) {
    if (!value) {
      return ''
    }
    return `${value.shortName} - ${value.manufacturerName} - ${value.model} - ${value.serialNumber}`
  }

  generateTsmdlEntityNames (linking: TsmLinking) {
    return `${linking.tsmEndpoint?.name ?? '-'}::${linking.datasource?.name ?? '-'}::${linking.thing?.name ?? '-'}::${linking.datastream?.name ?? '-'}`
  }

  head () {
    return {
      titleTemplate: 'Datastream Link - %s'
    }
  }

  initializeAppBar () {
    this.setTitle('Datastream Link')
  }

  @Watch('tsmLinking')
  onTsmLinkingChange (newVal: TsmLinking | null) {
    if (newVal) {
      this.setTitle(this.generateTsmdlEntityNames(newVal))
    }
  }
}
</script>
