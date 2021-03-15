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

  created () {
    this.valueCopy = DeviceProperty.createFromObject(this.value)
  }

  mounted () {
    //(this.$refs.devicePropertyForm as Vue & { focus: () => void}).focus()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  save (): void {
    this.isSaving = true
    this.$api.deviceProperties.update(this.deviceId, this.valueCopy).then((newProperty: DeviceProperty) => {
      this.isSaving = false
      this.$emit('input', newProperty)
      this.$router.push('/devices/' + this.deviceId + '/properties')
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save property')
    })
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: DeviceProperty) {
    this.valueCopy = DeviceProperty.createFromObject(val)
  }
}
</script>
