<template>
  <div>
    <InfoBox v-if="!value.length">
      Please add some devices to the configuration.
    </InfoBox>
    <v-subheader
      v-if="value.length"
    >
      Devices
      <v-spacer />
      <v-btn
        v-if="!devicePanelsHidden"
        text
        small
        @click="hideAllPanels"
      >
        hide all
      </v-btn>
      <v-btn
        v-if="devicePanelsHidden"
        text
        small
        @click="expandAllPanels"
      >
        expand all
      </v-btn>
    </v-subheader>
    <v-expansion-panels
      v-if="value.length"
      v-model="openedDevicePanels"
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
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import InfoBox from '@/components/InfoBox.vue'
import DeviceConfigurationAttributesForm from '@/components/DeviceConfigurationAttributesForm.vue'

import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'

/**
 * A class component to list device configuration attributes as expansion panels
 * @extends Vue
 */
@Component({
  components: {
    InfoBox,
    DeviceConfigurationAttributesForm
  }
})
// @ts-ignore
export default class DeviceConfigurationAttributesExpansionPanels extends Vue {
  private openedDevicePanels: number[] = []

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

  hideAllPanels (): void {
    this.openedDevicePanels = []
  }

  expandAllPanels (): void {
    this.openedDevicePanels = this.value.map((_, i) => i)
  }

  get devicePanelsHidden (): boolean {
    return this.value.map((_, i) => i).length > this.openedDevicePanels.length
  }

  /**
   * Updates the openedDevicePanels property for each device that was added or
   * removed. New devices are opened by default.
   */
  @Watch('value')
  // @ts-ignore
  onValueChanged (value: DeviceConfigurationAttributes[], oldValue: DeviceConfigurationAttributes[] = []) {
    if (!oldValue) {
      oldValue = []
    }
    // find the indices of the items that were removed
    oldValue.forEach((attribute, i) => {
      if (!value.includes(attribute)) {
        const index = this.openedDevicePanels.indexOf(i)
        if (index > -1) {
          this.openedDevicePanels.splice(index, 1)
        }
      }
    })
    // find the indices of the items that were added
    value.forEach((attribute, i) => {
      if (!oldValue.includes(attribute)) {
        this.openedDevicePanels.push(i)
      }
    })
  }
}
</script>
