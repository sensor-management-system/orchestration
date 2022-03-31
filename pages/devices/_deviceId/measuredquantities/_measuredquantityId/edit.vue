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
    <DevicePropertyForm
      ref="propertyForm"
      v-model="valueCopy"
      :readonly="false"
      :compartments="compartments"
      :sampling-medias="samplingMedias"
      :properties="properties"
      :units="units"
      :measured-quantity-units="measuredQuantityUnits"
    />
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
export default class DevicePropertyEditPage extends Vue {
  private valueCopy: DeviceProperty = new DeviceProperty()
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: DeviceProperty

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

  created () {
    this.valueCopy = DeviceProperty.createFromObject(this.value)
  }

  save () {
    this.$emit('showsave', true)
    this.$api.deviceProperties.update(this.deviceId, this.valueCopy).then((newProperty: DeviceProperty) => {
      this.$emit('showsave', false)
      this.$emit('input', newProperty)
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    })
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }
}
</script>
