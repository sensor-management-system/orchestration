<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :disabled="isLoading"
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceMeasuredQuantities.length === 0">
      There are no measured quantities for this device.
    </hint-card>
    <BaseList
      :list-items="deviceMeasuredQuantities"
    >
      <template #list-item="{item,index}">
        <DevicesMeasuredQuantitiesListItem
          :measured-quantity="item"
          :index="index"
          :device-id="deviceId"
          :compartments="compartments"
          :sampling-medias="samplingMedia"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
          :aggregation-types="aggregationtypes"
        >
          <template
            v-if="editable"
            #actions
          >
            <v-btn
              :to="'/devices/' + deviceId + '/measuredquantities/' + item.id + '/edit'"
              color="primary"
              text
              small
              @click.stop.prevent
            >
              Edit
            </v-btn>
          </template>
          <template
            v-if="editable"
            #dot-menu-items
          >
            <DotMenuActionCopy
              :readonly="!editable"
              :path="'/devices/' + deviceId + '/measuredquantities/' + item.id + '/copy'"
            />
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialog(item)"
            />
          </template>
        </DevicesMeasuredQuantitiesListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceMeasuredQuantities.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <DeleteDialog
      v-if="editable && measuredQuantityToDelete"
      v-model="showDeleteDialog"
      title="Delete Measured Quantity"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the measured quantity <em>{{ measuredQuantityToDelete.label }}</em>?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DeleteDeviceMeasuredQuantityAction, DevicesState, LoadDeviceMeasuredQuantitiesAction } from '@/store/devices'
import { VocabularyState } from '@/store/vocabulary'

import { DeviceProperty } from '@/models/DeviceProperty'

import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'
import BaseList from '@/components/shared/BaseList.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'

@Component({
  components: {
    DotMenuActionDelete,
    DotMenuActionCopy,
    BaseList,
    HintCard,
    DeleteDialog,
    DevicesMeasuredQuantitiesListItem
  },
  computed: {
    ...mapState('vocabulary', ['compartments', 'samplingMedia', 'properties', 'units', 'measuredQuantityUnits', 'aggregationtypes']),
    ...mapState('devices', ['deviceMeasuredQuantities']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['deleteDeviceMeasuredQuantity', 'loadDeviceMeasuredQuantities']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class DevicePropertyShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private measuredQuantityToDelete: DeviceProperty | null = null

  // vuex definition for typescript check
  compartments!: VocabularyState['compartments']
  samplingMedia!: VocabularyState['samplingMedia']
  properties!: VocabularyState['properties']
  units!: VocabularyState['units']
  measureQuantityUnits!: VocabularyState['measuredQuantityUnits']
  aggregtiontypes!: VocabularyState['aggregationtypes']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  deleteDeviceMeasuredQuantity!: DeleteDeviceMeasuredQuantityAction
  setLoading!: SetLoadingAction

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initDeleteDialog (measuredQuantity: DeviceProperty) {
    this.showDeleteDialog = true
    this.measuredQuantityToDelete = measuredQuantity
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.measuredQuantityToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.measuredQuantityToDelete === null || this.measuredQuantityToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)

      await this.deleteDeviceMeasuredQuantity(this.measuredQuantityToDelete.id)
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete measured quantity')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>
