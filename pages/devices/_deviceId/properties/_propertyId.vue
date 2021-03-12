<template>
  <div class="mb-1" style="flex: 0 0 100%; align-self: flex-start;">
    <NuxtChild
      v-if="isEditModeForProperty"
      v-model="property"
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
  private compartments: Compartment[] = []
  private samplingMedias: SamplingMedia[] = []
  private properties: Property[] = []
  private units: Unit[] = []
  private measuredQuantityUnits: MeasuredQuantityUnit[] = []

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: DeviceProperty

  mounted () {
    this.$api.compartments.findAllPaginated().then((foundCompartments) => {
      this.compartments = foundCompartments
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of compartments failed')
    })
    this.$api.samplingMedia.findAllPaginated().then((foundSamplingMedias) => {
      this.samplingMedias = foundSamplingMedias
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of sampling medias failed')
    })
    this.$api.properties.findAllPaginated().then((foundProperties) => {
      this.properties = foundProperties
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of properties failed')
    })
    this.$api.units.findAllPaginated().then((foundUnits) => {
      this.units = foundUnits
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of units failed')
    })
    this.$api.measuredQuantityUnits.findAllPaginated().then((foundUnits) => {
      this.measuredQuantityUnits = foundUnits
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of measuredquantityunits failed')
    })
  }

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
