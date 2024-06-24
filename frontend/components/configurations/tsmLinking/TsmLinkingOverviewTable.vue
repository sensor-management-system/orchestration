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
      <template #[`item.actions`]="{ item }">
        <v-icon
          v-if="$auth.loggedIn && canModifyEntity(configuration)"
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          v-if="$auth.loggedIn && canModifyEntity(configuration)"
          small
          color="error"
          @click="initDeleteDialog(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template #expanded-item="{ headers, item }">
        <td :colspan="headers.length">
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
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import TsmLinkingBasicDataTable from '@/components/configurations/tsmLinking/TsmLinkingBasicDataTable.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { TsmLinking } from '@/models/TsmLinking'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Device } from '@/models/Device'
import {
  DeleteConfigurationTsmLinkingAction,
  ITsmLinkingState,
  LoadConfigurationTsmLinkingsAction
} from '@/store/tsmLinking'
import { ConfigurationsState } from '@/store/configurations'
import { CanModifyEntityGetter } from '@/store/permissions'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  components: {
    DeleteDialog,
    ExtendedItemName,
    TsmLinkingBasicDataTable
  },
  computed: {
    ...mapState('tsmLinking', ['linkings']),
    ...mapState('configurations', ['configuration']),
    ...mapGetters('permissions', ['canModifyEntity'])
  },
  methods: {
    ...mapActions('tsmLinking', ['deleteConfigurationTsmLinking', 'loadConfigurationTsmLinkings']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class TsmLinkingOverviewTable extends Vue {
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
    }, {
      text: 'Offsets (X | Y | Z)',
      value: 'offsets'
    }, {
      text: 'Start date',
      value: 'startDate'
    }, {
      text: 'End date',
      value: 'endDate'
    }, {
      text: 'License',
      value: 'licenseName'
    }, {
      text: 'Aggregation',
      value: 'aggregationText'
    }, { text: 'Actions', value: 'actions', sortable: false }
  ]

  private itemToDelete: TsmLinking | null = null
  private showDeleteDialog: boolean = false
  // vuex definition for typescript check
  configuration!: ConfigurationsState['configuration']
  linkings!: ITsmLinkingState['linkings']
  deleteConfigurationTsmLinking!: DeleteConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  canModifyEntity!: CanModifyEntityGetter
  setLoading!: SetLoadingAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get dataTableLinkings (): Array<any> {
    const dataTableLinkings: Array<any> = this.linkings
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
    return `${value.shortName} - ${value.manufacturerName} - ${value.model} - ${value.serialNumber}`
  }
}
</script>

<style scoped>

</style>
