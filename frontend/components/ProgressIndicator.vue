<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-overlay
      :value="isInProgress"
      :opacity="dark ? 0.5 : 0.05"
    >
      <v-progress-circular
        indeterminate
        class="center-absolute"
        :color="color"
      />
    </v-overlay>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

@Component
export default class ProgressIndicator extends Vue {
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  // @ts-ignore
  readonly value!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  // @ts-ignore
  readonly dark!: boolean

  @Prop({
    default: 'primary',
    required: false,
    type: String
  })
  // @ts-ignore
  readonly color!: string

  get isInProgress (): boolean {
    return this.value
  }
}
</script>

<style>
  .center-absolute {
    position: fixed;
    top: 50%;
    left: 50%;
    margin-top: -16px;
    margin-left: -16px;
  }
</style>
