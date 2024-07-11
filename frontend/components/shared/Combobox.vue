<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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

  blur (): void {
    (this.$refs.combobox as Vue & { blur: () => void }).blur()
  }
}
</script>
