<template>
  <div>
    <InfoBox v-if="!value.length">
      Please add some platforms to the configuration.
    </InfoBox>
    <v-subheader
      v-if="value.length"
    >
      Platforms
      <v-spacer />
      <v-btn
        v-if="!allPlatformPanelsHidden"
        text
        small
        @click="hideAllPanels"
      >
        hide all
      </v-btn>
      <v-btn
        v-if="allPlatformPanelsHidden"
        text
        small
        @click="expandAllPanels"
      >
        expand all
      </v-btn>
    </v-subheader>
    <v-expansion-panels
      v-if="value.length"
      v-model="openedPlatformPanels"
      multiple
    >
      <v-expansion-panel
        v-for="(item, index) in value"
        :key="'platformAttribute-' + item.id"
      >
        <v-expansion-panel-header>{{ item.platform.shortName }}</v-expansion-panel-header>
        <v-expansion-panel-content>
          <PlatformConfigurationAttributesForm
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
 * @file provides a component for to list platform configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import InfoBox from '@/components/InfoBox.vue'
import PlatformConfigurationAttributesForm from '@/components/PlatformConfigurationAttributesForm.vue'

import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

/**
 * A class component to list platform configuration attributes as expansion panels
 * @extends Vue
 */
@Component({
  components: {
    InfoBox,
    PlatformConfigurationAttributesForm
  }
})
// @ts-ignore
export default class PlatformConfigurationAttributesExpansionPanels extends Vue {
  private openedPlatformPanels: number[] = []

  @Prop({
    default: () => [] as PlatformConfigurationAttributes[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value: PlatformConfigurationAttributes[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  hideAllPanels (): void {
    this.openedPlatformPanels = []
  }

  expandAllPanels (): void {
    this.openedPlatformPanels = this.value.map((_, i) => i)
  }

  get allPlatformPanelsHidden (): boolean {
    return this.openedPlatformPanels.length === 0
  }

  /**
   * Updates the openedPlatformPanels property for each platform that was added or
   * removed. New platforms are opened by default.
   */
  @Watch('value')
  // @ts-ignore
  onValueChanged (value: PlatformConfigurationAttributes[], oldValue: PlatformConfigurationAttributes[] = []) {
    // find the indices of the items that were removed
    oldValue.forEach((attribute, i) => {
      if (!value.includes(attribute)) {
        const index = this.openedPlatformPanels.indexOf(i)
        if (index > -1) {
          this.openedPlatformPanels.splice(index, 1)
        }
      }
    })
    // find the indices of the items that were added
    value.forEach((attribute, i) => {
      if (!oldValue.includes(attribute)) {
        this.openedPlatformPanels.push(i)
      }
    })
  }
}
</script>
