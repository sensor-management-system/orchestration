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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="Apply"
          :to="'/devices/' + deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <DevicePropertyForm
          ref="propertyEditForm"
          v-model="valueCopy"
          :readonly="false"
          :compartments="compartments"
          :sampling-medias="samplingMedia"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="Apply"
          :to="'/devices/' + deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <v-subheader>Existing measured quantities</v-subheader>
    <BaseList
      v-if="deviceMeasuredQuantity !== null"
      :list-items="quantitiesExceptCurrent"
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
        />
      </template>
    </BaseList>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import {
  DevicesState,
  LoadDeviceMeasuredQuantityAction,
  LoadDeviceMeasuredQuantitiesAction,
  UpdateDeviceMeasuredQuantityAction
} from '@/store/devices'

import { VocabularyState } from '@/store/vocabulary'

import { DeviceProperty } from '@/models/DeviceProperty'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import BaseList from '@/components/shared/BaseList.vue'

@Component({
  components: { BaseList, DotMenuActionDelete, DevicesMeasuredQuantitiesListItem, SaveAndCancelButtons, ProgressIndicator, DevicePropertyForm },
  middleware: ['auth'],
  computed: {
    ...mapState('vocabulary', ['compartments', 'samplingMedia', 'properties', 'units', 'measuredQuantityUnits']),
    ...mapState('devices', ['deviceMeasuredQuantity', 'deviceMeasuredQuantities'])
  },
  methods: mapActions('devices', ['loadDeviceMeasuredQuantity', 'loadDeviceMeasuredQuantities', 'updateDeviceMeasuredQuantity'])
})
export default class DevicePropertyEditPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private isSaving = false
  private isLoading = false

  private valueCopy: DeviceProperty = new DeviceProperty()

  // vuex definition for typescript check
  compartments!: VocabularyState['compartments']
  samplingMedia!: VocabularyState['samplingMedia']
  properties!: VocabularyState['properties']
  units!: VocabularyState['units']
  measureQuantityUnits!: VocabularyState['measuredQuantityUnits']
  deviceMeasuredQuantity!: DevicesState['deviceMeasuredQuantity']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  loadDeviceMeasuredQuantity!: LoadDeviceMeasuredQuantityAction
  updateDeviceMeasuredQuantity!: UpdateDeviceMeasuredQuantityAction
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction

  async created () {
    try {
      this.isLoading = true
      await this.loadDeviceMeasuredQuantity(this.measuredquantityId)
      if (this.deviceMeasuredQuantity) {
        this.valueCopy = DeviceProperty.createFromObject(this.deviceMeasuredQuantity)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load measured quantity')
    } finally {
      this.isLoading = false
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get measuredquantityId (): string {
    return this.$route.params.measuredquantityId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get quantitiesExceptCurrent () {
    return this.deviceMeasuredQuantities.filter((measuredQuantity) => {
      return measuredQuantity.id !== this.deviceMeasuredQuantity!.id
    })
  }

  async save () {
    try {
      this.isSaving = true
      await this.updateDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      })
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity updated')
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    } finally {
      this.isSaving = false
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/devices/' + this.deviceId + '/measuredquantities', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this device.')
      })
    }
  }
}
</script>
