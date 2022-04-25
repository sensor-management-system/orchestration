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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="save"
        >
          Update
        </v-btn>
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
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="save"
        >
          Update
        </v-btn>
      </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'

import { Compartment } from '@/models/Compartment'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { mapActions, mapState } from 'vuex'

@Component({
  components: { DevicePropertyForm },
  middleware: ['auth'],
  computed:{
    ...mapState('vocabulary',['compartments','samplingMedia','properties','units','measuredQuantityUnits']),
    ...mapState('devices',['deviceMeasuredQuantity'])
  },
  methods:mapActions('devices',['loadDeviceMeasuredQuantity','loadDeviceMeasuredQuantities','updateDeviceMeasuredQuantity'])
})
export default class DevicePropertyEditPage extends Vue {
  private valueCopy: DeviceProperty = new DeviceProperty()

  async created () {
    try {
      await this.loadDeviceMeasuredQuantity(this.measuredquantityId)
      this.valueCopy = DeviceProperty.createFromObject(this.deviceMeasuredQuantity)
    } catch (e) {
      console.log('error',e);
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get measuredquantityId():string{
    return this.$route.params.measuredquantityId
  }

  async save () {
    try {
      await this.updateDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      });
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    }
  }
}
</script>
