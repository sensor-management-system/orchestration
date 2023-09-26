<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <slot name="actions" />
    </template>
    <template #default>
      {{ computedTitle }}
    </template>
    <template #expandable>
      <DevicePropertyInfo
        v-model="measuredQuantity"
        :compartments="compartments"
        :sampling-medias="samplingMedias"
        :properties="properties"
        :units="units"
        :measured-quantity-units="measuredQuantityUnits"
        :aggregation-types="aggregationTypes"
      />
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Property } from '@/models/Property'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import DotMenu from '@/components/DotMenu.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import DevicePropertyInfo from '@/components/DevicePropertyInfo.vue'
import { AggregationType } from '@/models/AggregationType'

@Component({
  components: {
    DevicePropertyInfo,
    DotMenu,
    BaseExpandableListItem
  }
})
export default class DevicesMeasuredQuantitiesListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private measuredQuantity!: DeviceProperty

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

  /**
   * a list of AggregationTypes
   */
  @Prop({
    default: () => [] as AggregationType[],
    required: true,
    type: Array
  })
  readonly aggregationTypes!: AggregationType[]

  @Prop({
    required: true
  })
  private deviceId!: string

  @Prop({
    required: true
  })
  private index!: number

  get computedTitle () {
    if (this.measuredQuantity) {
      const propertyName = this.measuredQuantity.propertyName ?? ''
      const label = this.measuredQuantity.label ?? ''
      const unit = this.measuredQuantity.unitName ?? ''
      return `#${this.index + 1} - ${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
    }
    return ''
  }
}
</script>
