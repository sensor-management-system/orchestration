<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row>
      <v-col cols="12">
        <label>Label</label>
        {{ value.label }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Compartment</label>
        {{ compartmentValue | orDefault }}
        <v-tooltip v-if="compartmentDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ compartmentDefinition }}</span>
        </v-tooltip>
        <a v-if="value.compartmentUri" target="_blank" :href="value.compartmentUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3">
        <label>Sampling Media</label>
        {{ samplingMediaValue | orDefault }}
        <v-tooltip v-if="samplingMediaDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ samplingMediaDefinition }}</span>
        </v-tooltip>
        <a v-if="value.samplingMediaUri" target="_blank" :href="value.samplingMediaUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3">
        <label>Measured Quantity</label>
        {{ measuredQuantityValue | orDefault }}
        <v-tooltip v-if="measuredQuantityDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ measuredQuantityDefinition }}</span>
        </v-tooltip>
        <a v-if="value.propertyUri" target="_blank" :href="value.propertyUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3">
        <label>Aggregation Type</label>
        {{ aggregationTypeValue | orDefault }}
        <v-tooltip v-if="aggregationTypeDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ aggregationTypeDefinition }}</span>
        </v-tooltip>
        <a v-if="value.aggregationTypeUri" target="_blank" :href="value.aggregationTypeUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Unit</label>
        {{ unitValue | orDefault }}
        <v-tooltip v-if="unitDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ unitDefinition }}</span>
        </v-tooltip>
        <a v-if="value.unitUri" target="_blank" :href="value.unitUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3">
        <label>Failure Value</label>
        {{ value.failureValue | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Measuring range min</label>
        {{ value.measuringRange.min | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Measuring range max</label>
        {{ value.measuringRange.max | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Accuracy</label>
        {{ value.accuracy | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Unit of Accuracy</label>
        {{ accuracyUnitValue | orDefault }}
        <v-tooltip v-if="accuracyUnitDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ accuracyUnitDefinition }}</span>
        </v-tooltip>
        <a v-if="value.accuracyUnitUri" target="_blank" :href="value.accuracyUnitUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3">
        <label>Resolution</label>
        {{ value.resolution | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Unit of Resolution</label>
        {{ resolutionUnitValue | orDefault }}
        <v-tooltip v-if="resolutionUnitDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ resolutionUnitDefinition }}</span>
        </v-tooltip>
        <a v-if="value.resolutionUnitUri" target="_blank" :href="value.resolutionUnitUri">
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component that renders a form for a device property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { DeviceProperty } from '@/models/DeviceProperty'
import { AggregationType } from '@/models/AggregationType'

/**
 * A class component that renders a form for a device property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyInfo extends Vue {
  /**
   * a DeviceProperty
   */
  @Prop({
    default: () => new DeviceProperty(),
    required: true,
    type: DeviceProperty
  })
  // @ts-ignore
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

  /**
   * a list of AggregationTypes
   */
  @Prop({
    default: () => [] as AggregationType[],
    required: true,
    type: Array
  })
  readonly aggregationTypes!: AggregationType[]

  get compartmentValue (): string {
    if (!this.value.compartmentName && !this.value.compartmentUri) {
      return ''
    }
    const compartment = this.compartments.find(c => c.uri === this.value.compartmentUri)
    if (compartment) {
      return compartment.name
    }
    return this.value.compartmentName
  }

  get compartmentDefinition (): string {
    if (!this.value.compartmentName && !this.value.compartmentUri) {
      return ''
    }
    const compartment = this.compartments.find(c => c.uri === this.value.compartmentUri)
    if (compartment) {
      return compartment.definition
    }
    return ''
  }

  get samplingMediaValue (): string {
    if (!this.value.samplingMediaName && !this.value.samplingMediaUri) {
      return ''
    }
    const samplingMedia = this.samplingMedias.find(c => c.uri === this.value.samplingMediaUri)
    if (samplingMedia) {
      return samplingMedia.name
    }
    return this.value.samplingMediaName
  }

  get samplingMediaDefinition (): string {
    if (!this.value.samplingMediaName && !this.value.samplingMediaUri) {
      return ''
    }
    const samplingMedia = this.samplingMedias.find(c => c.uri === this.value.samplingMediaUri)
    if (samplingMedia) {
      return samplingMedia.definition
    }
    return ''
  }

  get measuredQuantityValue (): string {
    if (!this.value.propertyName && !this.value.propertyUri) {
      return ''
    }
    const property = this.properties.find(c => c.uri === this.value.propertyUri)
    if (property) {
      return property.name
    }
    return this.value.propertyName
  }

  get measuredQuantityDefinition (): string {
    if (!this.value.propertyName && !this.value.propertyUri) {
      return ''
    }
    const property = this.properties.find(c => c.uri === this.value.propertyUri)
    if (property) {
      return property.definition
    }
    return ''
  }

  get aggregationTypeValue (): string {
    // We could think about using also aggregation type id of the associated
    // property. However, this would give the imagination that the value
    // would be set - even if it is not so in the database.
    // So we stick the "standard" way of searching for the name.
    if (!this.value.aggregationTypeName && !this.value.aggregationTypeUri) {
      return ''
    }
    const aggregationType = this.aggregationTypes.find(c => c.uri === this.value.aggregationTypeUri)
    if (aggregationType) {
      return aggregationType.name
    }
    return this.value.aggregationTypeName
  }

  get aggregationTypeDefinition (): string {
    if (!this.value.aggregationTypeName && !this.value.aggregationTypeUri) {
      return ''
    }
    const aggregationType = this.aggregationTypes.find(c => c.uri === this.value.aggregationTypeUri)
    if (aggregationType) {
      return aggregationType.definition
    }
    return ''
  }

  get unitValue (): string {
    if (!this.value.unitName && !this.value.unitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.unitUri)
    if (unit) {
      return unit.name
    }
    return this.value.unitName
  }

  get unitDefinition (): string {
    if (!this.value.unitName && !this.value.unitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.unitUri)
    if (unit) {
      return unit.definition
    }
    return ''
  }

  get accuracyUnitValue (): string {
    if (!this.value.accuracyUnitName && !this.value.accuracyUnitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.accuracyUnitUri)
    if (unit) {
      return unit.name
    }
    return this.value.accuracyUnitName
  }

  get accuracyUnitDefinition (): string {
    if (!this.value.accuracyUnitName && !this.value.accuracyUnitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.accuracyUnitUri)
    if (unit) {
      return unit.definition
    }
    return ''
  }

  get resolutionUnitValue (): string {
    if (!this.value.resolutionUnitName && !this.value.resolutionUnitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.resolutionUnitUri)
    if (unit) {
      return unit.name
    }
    return this.value.resolutionUnitName
  }

  get resolutionUnitDefinition (): string {
    if (!this.value.resolutionUnitName && !this.value.resolutionUnitUri) {
      return ''
    }
    const unit = this.units.find(c => c.uri === this.value.resolutionUnitUri)
    if (unit) {
      return unit.definition
    }
    return ''
  }
}
</script>
