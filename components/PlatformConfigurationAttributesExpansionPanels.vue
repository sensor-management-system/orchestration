<template>
  <div>
    <v-subheader
      v-if="value.length"
    >
      Platforms
      <v-spacer />
      <v-btn
        v-if="!platformPanelsHidden"
        text
        small
        @click="platformPanelsHidden = true"
      >
        hide all
      </v-btn>
      <v-btn
        v-if="platformPanelsHidden"
        text
        small
        @click="platformPanelsHidden = false"
      >
        expand all
      </v-btn>
    </v-subheader>
    <v-expansion-panels
      v-if="value.length"
      :value="openedPlatformPanels"
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import PlatformConfigurationAttributesForm from '@/components/PlatformConfigurationAttributesForm.vue'

import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

/**
 * A class component to list platform configuration attributes as expansion panels
 * @extends Vue
 */
@Component({
  components: {
    PlatformConfigurationAttributesForm
  }
})
// @ts-ignore
export default class PlatformConfigurationAttributesExpansionPanels extends Vue {
  private platformPanelsHidden: boolean = false

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

  get openedPlatformPanels (): number[] {
    return !this.platformPanelsHidden ? this.value.map((_, i) => i) : []
  }
}
</script>
