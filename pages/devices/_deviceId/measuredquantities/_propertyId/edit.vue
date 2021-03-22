<template>
  <div>
    <DevicePropertyForm
      v-model="valueCopy"
      :readonly="false"
      :compartments="compartments"
      :sampling-medias="samplingMedias"
      :properties="properties"
      :units="units"
      :measured-quantity-units="measuredQuantityUnits"
    />
    <v-row>
      <col>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click.prevent.stop="save"
      >
        Apply
      </v-btn>
    </v-row>
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
  components: { DevicePropertyForm }
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
  compartments!: Compartment[]

  /**
   * a list of SamplingMedias
   */
  @Prop({
    default: () => [] as SamplingMedia[],
    required: true,
    type: Array
  })
  samplingMedias!: SamplingMedia[]

  /**
   * a list of Properties
   */
  @Prop({
    default: () => [] as Property[],
    required: true,
    type: Array
  })
  properties!: Property[]

  /**
   * a list of Units
   */
  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  units!: Unit[]

  /**
   * a list of MeasuredQuantityUnits
   */
  @Prop({
    default: () => [] as MeasuredQuantityUnit[],
    required: true,
    type: Array
  })
  measuredQuantityUnits!: MeasuredQuantityUnit[]

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
      this.$store.commit('snackbar/setError', 'Failed to save property')
    })
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
