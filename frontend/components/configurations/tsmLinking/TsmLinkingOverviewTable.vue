<!--
SPDX-FileCopyrightText: 2020 - 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="dataTableLinkings"
      sort-by="device"
      class="elevation-1"
      show-expand
      :footer-props="{
        itemsPerPageOptions:[50,100,-1]
      }"
      @click:row="toggleExpansion"
    >
      <template #[`item.deviceName`]="{ item }">
        <DeviceShortNameSerialNumber
          style="display:inline"
          :value="item.device"
        />
        <v-btn
          small
          text
          @click.stop.prevent="openDeviceLink(item.device)"
        >
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </v-btn>
      </template>
      <template #[`item.measuredQuantity`]="{ item }">
        <div v-if="item.deviceProperty">
          <span v-if="item.deviceProperty.propertyName">
            {{ item.deviceProperty.propertyName }}
          </span>
          <span
            v-if="item.deviceProperty.label"
            class="text--disabled"
          >
            - {{ item.deviceProperty.label }}
          </span>
          <span
            v-if="item.deviceProperty.unitName"
            class="text--secondary text-decoration-underline"
          >
            ({{ item.deviceProperty.unitName }})
          </span>
          <v-btn
            small
            text
            @click.stop.prevent="openDevicePropertyLink(item.deviceProperty)"
          >
            <v-icon
              small
            >
              mdi-open-in-new
            </v-icon>
          </v-btn>
        </div>
      </template>
      <template #[`item.tsmdlEntityNames`]="{ item }">
        <div>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <span
                v-bind="attrs"
                v-on="on"
              >
                {{ item.tsmEndpoint?.name ?? '-' }}
              </span>
            </template>
            <span>TSM</span>
          </v-tooltip>
        </div>
        <div>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <span
                v-bind="attrs"
                v-on="on"
              >
                {{ getDataSourceName(item) }}
              </span>
            </template>
            <span>Datasource: {{ item.datasource?.name ?? '-' }}</span>
          </v-tooltip>
        </div>
        <div>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <span
                v-bind="attrs"
                v-on="on"
              >
                {{ getThingName(item) }}
              </span>
            </template>
            <span>Thing: {{ item.thing?.name ?? '-' }}</span>
          </v-tooltip>
        </div>
        <div>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <span
                v-bind="attrs"
                v-on="on"
              >
                {{ getDatastreamName(item) }}
              </span>
            </template>
            <span>Datastream: {{ item.datastream?.name ?? '-' }}</span>
          </v-tooltip>
        </div>
      </template>
      <template #[`item.actions`]="{ item }">
        <DotMenu>
          <template #actions>
            <DotMenuActionEdit
              :readonly="!$auth.loggedIn || !canModifyEntity(configuration)"
              @click="editItem(item)"
            />
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn || !canModifyEntity(configuration)"
              @click="initDeleteDialog(item)"
            />
          </template>
        </DotMenu>
      </template>
      <template #expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <div class="ml-4">
            <v-row class="mt-2">
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                License
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ item.licenseName }}
                <a v-if="item.licenseUri" target="_blank" :href="item.licenseUri">
                  <v-icon small>
                    mdi-open-in-new
                  </v-icon>
                </a>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Involved Devices
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ item.involvedDevices | sparseJoin }}
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Aggregation
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ item.aggregationText }}
              </v-col>
            </v-row>
          </div>
          <tsm-linking-basic-data-table
            :linking="item"
          />
        </td>
      </template>
    </v-data-table>
    <DeleteDialog
      v-model="showDeleteDialog"
      title="Delete Data Linking"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the linking?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import TsmLinkingBasicDataTable from '@/components/configurations/tsmLinking/TsmLinkingBasicDataTable.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { TsmLinking } from '@/models/TsmLinking'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Device } from '@/models/Device'
import {
  DeleteConfigurationTsmLinkingAction, FilteredLinkingsGetter,
  LoadConfigurationTsmLinkingsAction
} from '@/store/tsmLinking'
import { ConfigurationsState } from '@/store/configurations'
import { CanModifyEntityGetter } from '@/store/permissions'
import { SetLoadingAction } from '@/store/progressindicator'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionEdit from '@/components/DotMenuActionEdit.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { shortenMiddle } from '@/utils/stringHelpers'
import { dateToDateString } from '@/utils/dateHelper'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmEndpoint } from '@/models/TsmEndpoint'
import DeviceShortNameSerialNumber from '@/components/devices/DeviceShortNameSerialNumber.vue'

type DataTableLinkingsItem = {
  id: string
  tsmdlEntityNames: string
  offsets: string
  startDate: string
  endDate: string
  measuredQuantity: string
  device: Device | null
  deviceName: string
  deviceProperty: DeviceProperty | null
  datasource: TsmdlDatasource | null
  datastream: TsmdlDatastream | null
  thing: TsmdlThing | null
  tsmEndpoint: TsmEndpoint | null
  licenseName: string
  licenseUri: string
  aggregationText: string
  involvedDevices: Device[]
}

@Component({
  components: {
    DeviceShortNameSerialNumber,
    DotMenuActionDelete,
    DotMenuActionEdit,
    DotMenu,
    DeleteDialog,
    ExtendedItemName,
    TsmLinkingBasicDataTable
  },
  computed: {
    ...mapGetters('tsmLinking', ['filteredLinkings']),
    ...mapState('configurations', ['configuration']),
    ...mapGetters('permissions', ['canModifyEntity'])
  },
  methods: {
    ...mapActions('tsmLinking', ['deleteConfigurationTsmLinking', 'loadConfigurationTsmLinkings']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class TsmLinkingOverviewTable extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  private headers = [
    {
      text: 'Device',
      value: 'deviceName'
    },
    {
      text: 'Measured Quantity',
      value: 'measuredQuantity'
    }, {
      text: 'Offsets (X | Y | Z)',
      value: 'offsets'
    }, {
      text: 'Start date',
      value: 'startDate'
    }, {
      text: 'End date',
      value: 'endDate'
    },
    {
      text: 'TSM/Datasource/Thing/Datastream',
      value: 'tsmdlEntityNames'
    },
    {
      text: 'Actions',
      value: 'actions',
      sortable: false
    }
  ]

  private itemToDelete: TsmLinking | null = null
  private showDeleteDialog: boolean = false
  // vuex definition for typescript check
  configuration!: ConfigurationsState['configuration']
  filteredLinkings!: FilteredLinkingsGetter
  deleteConfigurationTsmLinking!: DeleteConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  canModifyEntity!: CanModifyEntityGetter
  setLoading!: SetLoadingAction

  toggleExpansion (_item: TsmLinking, _row: { expand: (value: boolean) => void, isExpanded: boolean }) {
    const { expand, isExpanded } = _row
    expand(!isExpanded)
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get dataTableLinkings (): Array<DataTableLinkingsItem> {
    return this.filteredLinkings.map((linking: TsmLinking) => {
      return {
        id: linking.id,
        tsmdlEntityNames: this.generateTsmdlEntityNames(linking),
        offsets: `(${linking?.deviceMountAction?.offsetX} | ${linking?.deviceMountAction?.offsetY} | ${linking?.deviceMountAction?.offsetZ})`,
        startDate: dateToDateString(linking.startDate),
        endDate: dateToDateString(linking.endDate),
        measuredQuantity: this.generatePropertyTitle(linking.deviceProperty),
        device: linking.device,
        deviceName: this.getDeviceName(linking.device),
        deviceProperty: linking.deviceProperty,
        datasource: linking.datasource,
        datastream: linking.datastream,
        thing: linking.thing,
        tsmEndpoint: linking.tsmEndpoint,
        licenseName: linking.licenseName,
        licenseUri: linking.licenseUri,
        aggregationText: linking.aggregationText,
        involvedDevices: linking.filterInvolvedDevices(this.devices)
      }
    })
  }

  get shortMiddleNumberBasedOnBreakpoint () {
    switch (this.$vuetify.breakpoint.name) {
      case 'xs': return 5
      case 'sm': return 10
      case 'md': return 15
      case 'lg': return 25
      case 'xl': return 40
    }
  }

  editItem (item: TsmLinking) {
    this.$router.push(`/configurations/${this.configurationId}/tsm-linking/${item.id}/edit`)
  }

  initDeleteDialog (item: TsmLinking) {
    this.showDeleteDialog = true
    this.itemToDelete = item
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.itemToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.itemToDelete === null) {
      this.closeDialog()
      return
    }
    this.setLoading(true)
    try {
      this.showDeleteDialog = false
      await this.deleteConfigurationTsmLinking(this.itemToDelete)
      this.itemToDelete = null
      this.$store.commit('snackbar/setSuccess', 'Linking deleted')
      this.loadConfigurationTsmLinkings(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Linking could not be deleted')
    } finally {
      this.setLoading(false)
    }
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

  generateTsmdlEntityNames (linking: TsmLinking) {
    return `${linking.tsmEndpoint?.name ?? '-'}::${linking.datasource?.name ?? '-'}::${linking.thing?.name ?? '-'}::${linking.datastream?.name ?? '-'}`
  }

  getDeviceName (value: Device | null) {
    if (!value) {
      return ''
    }

    let nameString = value.shortName

    if (value.serialNumber) {
      nameString += ` (${value.serialNumber})`
    }

    return nameString
  }

  getDataSourceName (item: DataTableLinkingsItem) {
    if (item.datasource?.name) {
      return this.shortenbyAmount(item.datasource.name)
    } else {
      return '-'
    }
  }

  getThingName (item: DataTableLinkingsItem) {
    if (item.thing?.name) {
      return this.shortenbyAmount(item.thing.name)
    } else {
      return '-'
    }
  }

  getDatastreamName (item: DataTableLinkingsItem) {
    if (item.datastream?.name) {
      return this.shortenbyAmount(item.datastream.name)
    } else {
      return '-'
    }
  }

  private shortenbyAmount (phrase: string): string {
    return shortenMiddle(phrase, this.shortMiddleNumberBasedOnBreakpoint)
  }

  private openDeviceLink (device: Device) {
    window.open(this.$router.resolve(`/devices/${device.id}`).href, '_blank')
  }

  private openDevicePropertyLink (deviceProperty: DeviceProperty) {
    window.open(this.$router.resolve(`/measuredquantities/${deviceProperty.id}`).href, '_blank')
  }
}
</script>

<style scoped>

</style>
