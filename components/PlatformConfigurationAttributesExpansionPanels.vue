<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
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
 * @file provides a component to list platform configuration attributes
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

  /**
   * a list of PlatformConfigurationAttributes
   */
  @Prop({
    default: () => [] as PlatformConfigurationAttributes[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value: PlatformConfigurationAttributes[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * closes all platform panels
   *
   */
  hideAllPanels (): void {
    this.openedPlatformPanels = []
  }

  /**
   * expands all platform panels
   *
   */
  expandAllPanels (): void {
    this.openedPlatformPanels = this.value.map((_, i) => i)
  }

  /**
   * returns of all platform panels are hidden
   *
   * @return {boolean} whether all platform panels are hidden or not
   */
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
