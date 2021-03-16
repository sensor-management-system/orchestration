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
  <div class="mb-1" style="flex: 0 0 100%; align-self: flex-start;">
    <NuxtChild
      v-if="isEditModeForProperty"
      v-model="property"
      :compartments="compartments"
      :sampling-medias="samplingMedias"
      :properties="properties"
      :units="units"
      :measured-quantity-units="measuredQuantityUnits"
    />
    <DevicePropertyExpansionPanel
      v-else
      v-model="property"
    >
      <DevicePropertyInfo
        v-model="property"
        :compartments="compartments"
        :sampling-medias="samplingMedias"
        :properties="properties"
        :units="units"
        :measured-quantity-units="measuredQuantityUnits"
      />
    </DevicePropertyExpansionPanel>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DevicePropertyExpansionPanel from '@/components/DevicePropertyExpansionPanel.vue'
import DevicePropertyInfo from '@/components/DevicePropertyInfo.vue'

@Component({
  components: {
    DevicePropertyExpansionPanel,
    DevicePropertyInfo,
    ProgressIndicator
  }
})
export default class DevicePropertyIdPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: DeviceProperty

  /**
   * a list of compartments
   */
  @Prop({
    default: () => [] as Compartment[],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly compartments!: Compartment[]

  /**
   * a list of samplingMedias
   */
  @Prop({
    default: () => [] as SamplingMedia[],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly samplingMedias!: SamplingMedia[]

  /**
   * a list of properties
   */
  @Prop({
    default: () => [] as Property[],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly properties!: Property[]

  /**
   * a list of units
   */
  @Prop({
    default: () => [] as Unit[],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly units!: Unit[]

  /**
   * a list of measuredQuantityUnits
   */
  @Prop({
    default: () => [] as MeasuredQuantityUnit[],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly measuredQuantityUnits!: MeasuredQuantityUnit[]

  get property (): DeviceProperty {
    return this.value
  }

  set property (value: DeviceProperty) {
    this.$emit('input', value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isEditModeForProperty () {
    return this.$route.path === '/devices/' + this.deviceId + '/properties/' + this.value.id + '/edit'
  }
}
</script>
