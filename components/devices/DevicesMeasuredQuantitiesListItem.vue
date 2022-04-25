<template>
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-card-text
        @click.stop.prevent="show = !show"
      >
        <v-row
          no-gutters
        >
          <v-col
            align-self="end"
            class="text-right"
          >
            <DotMenu>
              <template #actions>
                <slot name="dot-menu-items">
                </slot>
              </template>
            </DotMenu>
          </v-col>
        </v-row>
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{computedTitel}}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              v-if="$auth.loggedIn"
              :to="'/devices/'+deviceId+'/measuredquantities/'+measuredQuantity.id+'/edit'"
              color="primary"
              text
              @click.stop.prevent
            >
              Edit
            </v-btn>
            <v-btn
              icon
              @click.stop.prevent="show = !show"
            >
              <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-expand-transition>
        <v-container>
              <DevicePropertyInfo
                v-show="show"
                v-model="measuredQuantity"
                :compartments="compartments"
                :sampling-medias="samplingMedias"
                :properties="properties"
                :units="units"
                :measured-quantity-units="measuredQuantityUnits"
              />
        </v-container>

      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import DotMenu from '@/components/DotMenu.vue'
import { Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'
import DevicePropertyInfo from '@/components/DevicePropertyInfo.vue'
import { Compartment } from '@/models/Compartment'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Property } from '@/models/Property'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
@Component({
  components: { DevicePropertyInfo, DotMenu }
})
export default class DevicesMeasuredQuantitiesListItem extends Vue {
  @Prop({
    required:true,
    type: Object
  })
  private measuredQuantity!:DeviceProperty;

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

  @Prop({
    required:true
  })
  private deviceId!:string;

  @Prop({
    required:true
  })
  private index!:number;

  private show=false

  get computedTitle(){
    let additionaLabel = '';
    if(this.measuredQuantity.label){
      additionaLabel= ' - ' +this.measuredQuantity.label
    }
    return `Measured quantity ${this.index+1}` + additionaLabel;
  }

}
</script>

<style scoped>

</style>
