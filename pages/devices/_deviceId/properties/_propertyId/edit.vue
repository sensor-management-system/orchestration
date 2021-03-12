<template>
  <DevicePropertyExpansionPanel
    v-model="valueCopy"
  >
    <template #actions>
      <v-btn
        v-if="isLoggedIn"
        text
        small
        nuxt
        :to="'/devices/' + deviceId + '/properties'"
      >
        Cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="save()"
      >
        Apply
      </v-btn>
    </template>
    <DevicePropertyForm
      v-model="valueCopy"
      :compartments="compartments"
      :sampling-medias="samplingMedias"
      :properties="properties"
      :units="units"
      :measured-quantity-units="measuredQuantityUnits"
    />
  </DevicePropertyExpansionPanel>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import DevicePropertyExpansionPanel from '@/components/DevicePropertyExpansionPanel.vue'
import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    DevicePropertyExpansionPanel,
    DevicePropertyForm,
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
  private isSaving: boolean = false
  private valueCopy: DeviceProperty = new DeviceProperty()

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

  created () {
    this.valueCopy = DeviceProperty.createFromObject(this.value)
  }

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
    });
    //(this.$refs.devicePropertyForm as Vue & { focus: () => void}).focus()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  save (): void {
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: DeviceProperty) {
    this.valueCopy = DeviceProperty.createFromObject(val)
  }
}
</script>
