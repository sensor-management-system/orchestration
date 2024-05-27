<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <DevicePropertyForm
          ref="propertyForm"
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
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <v-subheader
      v-if="deviceMeasuredQuantities.length"
    >
      Existing measured quantities
    </v-subheader>
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
        />
      </template>
    </BaseList>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { AddDeviceMeasuredQuantityAction, DevicesState, LoadDeviceMeasuredQuantitiesAction } from '@/store/devices'
import {
  LoadCompartmentsAction,
  LoadSamplingMediaAction,
  LoadPropertiesAction,
  LoadUnitsAction,
  LoadMeasuredQuantityUnitsAction,
  VocabularyState
} from '@/store/vocabulary'

import { DeviceProperty } from '@/models/DeviceProperty'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'

@Component({
  middleware: ['auth'],
  components: { DevicesMeasuredQuantitiesListItem, BaseList, SaveAndCancelButtons, DevicePropertyForm },
  computed: {
    ...mapState('vocabulary', ['compartments', 'samplingMedia', 'properties', 'units', 'measuredQuantityUnits', 'aggregationtypes']),
    ...mapState('devices', ['deviceMeasuredQuantities'])
  },
  methods: {
    ...mapActions('devices', ['addDeviceMeasuredQuantity', 'loadDeviceMeasuredQuantities']),
    ...mapActions('vocabulary', ['loadCompartments', 'loadSamplingMedia', 'loadProperties', 'loadUnits', 'loadMeasuredQuantityUnits']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class DevicePropertyAddPage extends mixins(CheckEditAccess) {
  private valueCopy: DeviceProperty = new DeviceProperty()

  // vuex definition for typescript check
  compartments!: VocabularyState['compartments']
  samplingMedia!: VocabularyState['samplingMedia']
  properties!: VocabularyState['properties']
  units!: VocabularyState['units']
  aggregationtypes!: VocabularyState['aggregationtypes']
  measuredQuantityUnits!: VocabularyState['measuredQuantityUnits']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  loadCompartments!: LoadCompartmentsAction
  loadSamplingMedia!: LoadSamplingMediaAction
  loadProperties!: LoadPropertiesAction
  loadUnits!: LoadUnitsAction
  loadMeasuredQuantityUnits!: LoadMeasuredQuantityUnitsAction
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

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {
    if (!(this.$refs.propertyForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      await this.addDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      })
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New measured quantity added')
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
