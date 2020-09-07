<template>
  <div>
    <v-subheader
      v-if="value.length"
    >
      Devices
      <v-spacer />
      <v-btn
        v-if="!devicePanelsHidden"
        text
        small
        @click="devicePanelsHidden = true"
      >
        hide all
      </v-btn>
      <v-btn
        v-if="devicePanelsHidden"
        text
        small
        @click="devicePanelsHidden = false"
      >
        expand all
      </v-btn>
    </v-subheader>
    <v-expansion-panels
      v-if="value.length"
      :value="openedDevicePanels"
      multiple
    >
      <v-expansion-panel
        v-for="(item, index) in value"
        :key="'deviceAttribute-' + item.id"
      >
        <v-expansion-panel-header>{{ item.device.shortName }}</v-expansion-panel-header>
        <v-expansion-panel-content>
          <DeviceConfigurationAttributesForm
            v-model="value[index]"
            :readonly="readonly"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for to list device configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import DeviceConfigurationAttributesForm from '@/components/DeviceConfigurationAttributesForm.vue'

import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'

/**
 * A class component to list device configuration attributes as expansion panels
 * @extends Vue
 */
@Component({
  components: {
    DeviceConfigurationAttributesForm
  }
})
// @ts-ignore
export default class DeviceConfigurationAttributesExpansionPanels extends Vue {
  private devicePanelsHidden: boolean = false

  @Prop({
    default: () => [] as DeviceConfigurationAttributes[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value: DeviceConfigurationAttributes[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  get openedDevicePanels (): number[] {
    return !this.devicePanelsHidden ? this.value.map((_, i) => i) : []
  }
}
</script>
