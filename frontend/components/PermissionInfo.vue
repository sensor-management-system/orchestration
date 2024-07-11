<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-icon v-if="value" color="green">
      mdi-check
    </v-icon>
    <v-icon v-else color="red">
      mdi-close
    </v-icon>
    {{ label }}
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to show an info text
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A class component to show an info text
 * @extends Vue
 */
@Component
// @ts-ignore
export default class PermissionInfo extends Vue {
  /**
   * a list of projects
   */
  @Prop({
    default: false,
    required: true,
    type: Boolean
  })
  // @ts-ignore
  readonly value!: boolean

  /**
   * a label for the permission info
   */
  @Prop({
    default: '',
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string
}
</script>
