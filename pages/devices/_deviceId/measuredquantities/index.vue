<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
      v-model="isSaving"
      dark
    />
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceMeasuredQuantities.length === 0">
      There are no measured qauntities for this device.
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
        >
          <template #dot-menu-items>
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
        v-if="$auth.loggedIn"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <DevicesMeasuredQuantitiesDeleteDialog
      v-model="showDeleteDialog"
      :measured-quantity="measuredQuantityToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { mapActions, mapState } from 'vuex'
import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'
import DevicesMeasuredQuantitiesDeleteDialog from '@/components/devices/DevicesMeasuredQuantitiesDeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'
import BaseList from '@/components/shared/BaseList.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { DeviceProperty } from '@/models/DeviceProperty'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

@Component({
  components: {
    DotMenuActionDelete,
    ProgressIndicator,
    BaseList,
    HintCard,
    DevicesMeasuredQuantitiesDeleteDialog,
    DevicesMeasuredQuantitiesListItem
  },
  computed: {
    ...mapState('vocabulary', ['compartments', 'samplingMedia', 'properties', 'units', 'measuredQuantityUnits']),
    ...mapState('devices', ['deviceMeasuredQuantities'])
  },
  methods: {
    ...mapActions('devices', ['deleteDeviceMeasuredQuantity', 'loadDeviceMeasuredQuantities'])
  }
})
export default class DevicePropertyShowPage extends Vue {
  private isSaving = false

  private showDeleteDialog = false
  private measuredQuantityToDelete: DeviceProperty | null = null

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
      this.isSaving = true

      await this.deleteDeviceMeasuredQuantity(this.measuredQuantityToDelete.id)
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete measured quantity')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>
