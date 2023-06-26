<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
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
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
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
      <template #[`item.actions`]="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
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
      title="Delete TSM Linking"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the linking?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
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
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator,
    DeleteDialog,
    ExtendedItemName,
    TsmLinkingBasicDataTable
  },
  computed: {
    ...mapState('tsmLinking', ['linkings'])
  },
  methods: {
    ...mapActions('tsmLinking', ['deleteConfigurationTsmLinking', 'loadConfigurationTsmLinkings'])
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
      text: 'Start date',
      value: 'startDate'
    }, {
      text: 'End date',
      value: 'endDate'
    },
    { text: 'Actions', value: 'actions', sortable: false }
  ]

  private itemToDelete: TsmLinking | null = null
  private isLoading: boolean = false
  private showDeleteDialog: boolean = false
  // vuex definition for typescript check
  linkings!: ITsmLinkingState['linkings']
  deleteConfigurationTsmLinking!: DeleteConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get dataTableLinkings (): Array<any> {
    const dataTableLinkings: Array<any> = this.linkings
    return dataTableLinkings.map((linking: TsmLinking) => {
      return {
        id: linking.id,
        tsmdlEntityNames: this.generateTsmdlEntityNames(linking),
        startDate: this.$root.$options.filters!.toUtcDateTimeStringHHMM(linking.startDate),
        endDate: this.$root.$options.filters!.toUtcDateTimeStringHHMM(linking.endDate),
        measuredQuantity: this.generatePropertyTitle(linking.deviceProperty),
        device: linking.device,
        deviceName: this.getDeviceName(linking.device),
        datasource: linking.datasource,
        datastream: linking.datastream,
        thing: linking.thing,
        tsmEndpoint: linking.tsmEndpoint
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
    this.isLoading = true
    try {
      this.showDeleteDialog = false
      await this.deleteConfigurationTsmLinking(this.itemToDelete)
      this.itemToDelete = null
      this.$store.commit('snackbar/setSuccess', 'Linking deleted')
      this.loadConfigurationTsmLinkings(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Linking could not be deleted')
    } finally {
      this.isLoading = false
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
