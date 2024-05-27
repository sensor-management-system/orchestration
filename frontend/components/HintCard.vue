<!--
SPDX-FileCopyrightText: 2021 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-card flat>
    <v-card-text>
      <div class="text-center">
        <slot />
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component to show a hint in a card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component } from 'nuxt-property-decorator'

/**
 * A class component to show a hint in a card.
 * @extends Vue
 */
@Component
// @ts-ignore
export default class HintCard extends Vue {
}
</script>
