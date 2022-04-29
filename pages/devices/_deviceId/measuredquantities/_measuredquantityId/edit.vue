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
          save-btn-text="Apply"
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
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
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Apply"
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { DeviceProperty } from '@/models/DeviceProperty'
import { mapActions, mapState } from 'vuex'

@Component({
  components: { SaveAndCancelButtons, ProgressIndicator, DevicePropertyForm },
  middleware: ['auth'],
  computed:{
    ...mapState('vocabulary',['compartments','samplingMedia','properties','units','measuredQuantityUnits']),
    ...mapState('devices',['deviceMeasuredQuantity'])
  },
  methods:mapActions('devices',['loadDeviceMeasuredQuantity','loadDeviceMeasuredQuantities','updateDeviceMeasuredQuantity'])
})
export default class DevicePropertyEditPage extends Vue {
  private isSaving = false
  private isLoading = false

  private valueCopy: DeviceProperty = new DeviceProperty()

  async created () {
    try {
      this.isLoading=true
      await this.loadDeviceMeasuredQuantity(this.measuredquantityId)
      this.valueCopy = DeviceProperty.createFromObject(this.deviceMeasuredQuantity)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load measured quantity')
    }finally {
      this.isLoading=false
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get measuredquantityId():string{
    return this.$route.params.measuredquantityId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    try {
      this.isSaving=true
      await this.updateDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      });
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity updated')
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    }finally {
      this.isSaving=false
    }
  }
}
</script>
