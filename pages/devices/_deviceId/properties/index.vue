<template>
  <DevicePropertyExpansionPanel
    v-model="value"
  >
    <template #actions>
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        text
        small
        nuxt
        :to="'/devices/' + deviceId + '/properties/' + value.id + '/edit'"
      >
        Edit
      </v-btn>
      <v-menu
        v-if="isLoggedIn"
        close-on-click
        close-on-content-click
        offset-x
        left
        z-index="999"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            data-role="property-menu"
            icon
            small
            v-on="on"
          >
            <v-icon
              dense
              small
            >
              mdi-dots-vertical
            </v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            dense
            @click="deleteProperty"
          >
            <v-list-item-content>
              <v-list-item-title
                class="red--text"
              >
                <v-icon
                  left
                  small
                  color="red"
                >
                  mdi-delete
                </v-icon>
                Remove Property
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <DevicePropertyInfo
      v-model="value"
      :compartments="compartments"
      :sampling-medias="samplingMedias"
      :properties="properties"
      :units="units"
      :measured-quantity-units="measuredQuantityUnits"
    />
  </DevicePropertyExpansionPanel>
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
export default class DevicePropertiesShowPage extends Vue {
  private isLoading = false
  private isSaving = false

  /**
   * a DeviceProperty
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
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

  mounted () {
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  deleteProperty () {
    this.$emit('delete', this.value)
  }
}
</script>
