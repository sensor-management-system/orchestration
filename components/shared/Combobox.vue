<!--
Web client of the Sensor Management System software developed within
the Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <v-combobox
    ref="combobox"
    v-bind="$attrs"
    v-on="$listeners"
    @blur="onBlur"
  >
    <slot v-for="(_, slot) in $slots" :slot="slot" :name="slot" />
    <template v-for="(_, slot) of $scopedSlots" #[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
  </v-combobox>
</template>

<script lang="ts">
/**
 * @file provides a wrapper component to v-combobox
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component } from 'nuxt-property-decorator'

/**
 * A wrapper component to v-combobox. Supports all props, events and slots.
 *
 * In addition to it, it triggers the update of the v-combobox immediately as
 * soon as the component looses it focus. See
 * https://codebase.helmholtz.cloud/hub-terra/sms/frontend/-/issues/412
 *
 * @extends Vue
 */
@Component
export default class Combobox extends Vue {
  onBlur (): void {
    (this.$refs.combobox as Vue & { updateSelf: () => void}).updateSelf()
  }

  focus (): void {
    (this.$refs.combobox as Vue & { focus: () => void }).focus()
  }
}
</script>
