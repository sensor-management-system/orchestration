<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
      return `#${this.index + 1} - ${this.measuredQuantity}`
    }
    return ''
  }
}
</script>
