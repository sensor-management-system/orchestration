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
    <v-card class="mt-4">
      <v-card-title>
        <v-row>
          <v-col>
            Create a new measured quantity
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              text
              small
              @click.prevent.stop="cancel"
            >
              Cancel
            </v-btn>
            <v-btn
              color="green"
              small
              @click.prevent.stop="save"
            >
              Save
            </v-btn>
          </v-col>
        </v-row>
        <v-card-actions />
      </v-card-title>
      <v-card-text>
        <DevicePropertyForm
          ref="propertyForm"
          v-model="value"
          :readonly="false"
          :compartments="compartments"
          :sampling-medias="samplingMedias"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
        />
      </v-card-text>
    </v-card>
  </div>
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

@Component({
  components: { DevicePropertyForm },
  middleware: ['auth']
})
export default class DevicePropertyNewPage extends Vue {
  private value: DeviceProperty = new DeviceProperty()

  /**
   * a list of Compartments
   */
  @Prop({
    default: () => [] as Compartment[],
    required: true,
    type: Array
  })
  readonly compartments!: Compartment[]

  /**
   * a list of SamplingMedias
   */
  @Prop({
    default: () => [] as SamplingMedia[],
    required: true,
    type: Array
  })
  readonly samplingMedias!: SamplingMedia[]

  /**
   * a list of Properties
   */
  @Prop({
    default: () => [] as Property[],
    required: true,
    type: Array
  })
  readonly properties!: Property[]

  /**
   * a list of Units
   */
  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  readonly units!: Unit[]

  /**
   * a list of MeasuredQuantityUnits
   */
  @Prop({
    default: () => [] as MeasuredQuantityUnit[],
    required: true,
    type: Array
  })
  readonly measuredQuantityUnits!: MeasuredQuantityUnit[]

  save () {
    this.$emit('showsave', true)
    this.$api.deviceProperties.add(this.deviceId, this.value).then((newDeviceProperty: DeviceProperty) => {
      this.$emit('showsave', false)
      this.$emit('input', newDeviceProperty)
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    })
  }

  cancel () {
    this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }
}
</script>
