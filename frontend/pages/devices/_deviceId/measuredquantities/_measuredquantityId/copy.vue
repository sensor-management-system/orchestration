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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="Copy"
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
          :aggregation-types="aggregationtypes"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="Copy"
          :to="'/devices/' + deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <v-subheader>Existing measured quantities</v-subheader>
    <BaseList
      v-if="deviceMeasuredQuantity !== null"
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
        />
      </template>
    </BaseList>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  DevicesState,
  LoadDeviceMeasuredQuantityAction,
  LoadDeviceMeasuredQuantitiesAction,
  AddDeviceMeasuredQuantityAction
} from '@/store/devices'

import { VocabularyState } from '@/store/vocabulary'

import { DeviceProperty } from '@/models/DeviceProperty'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import BaseList from '@/components/shared/BaseList.vue'

@Component({
  components: { BaseList, DotMenuActionDelete, DevicesMeasuredQuantitiesListItem, SaveAndCancelButtons, DevicePropertyForm },
  middleware: ['auth'],
  computed: {
    ...mapState('vocabulary', ['compartments', 'samplingMedia', 'properties', 'units', 'measuredQuantityUnits', 'aggregationtypes']),
    ...mapState('devices', ['deviceMeasuredQuantity', 'deviceMeasuredQuantities'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceMeasuredQuantity', 'loadDeviceMeasuredQuantities', 'addDeviceMeasuredQuantity']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class DevicePropertyCopyPage extends mixins(CheckEditAccess) {
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
  addDeviceMeasuredQuantity!: AddDeviceMeasuredQuantityAction
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/measuredquantities'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
  }

  async created () {
    try {
      this.setLoading(true)
      await this.loadDeviceMeasuredQuantity(this.measuredquantityId)
      if (this.deviceMeasuredQuantity) {
        this.valueCopy = DeviceProperty.createFromObject(this.deviceMeasuredQuantity)
        // as we want to save a new instance of the measured quantity, we set
        // the id to null
        this.valueCopy.id = null
        this.valueCopy.label = 'Copy of ' + this.valueCopy.label
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load measured quantity')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get measuredquantityId (): string {
    return this.$route.params.measuredquantityId
  }

  async save () {
    try {
      this.setLoading(true)
      await this.addDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      })
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity copied')
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
