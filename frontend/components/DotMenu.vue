<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-menu
    close-on-click
    close-on-content-click
    offset-x
    left
    z-index="999"
  >
    <template #activator="{ on }">
      <v-btn
        data-role="property-menu"
        icon
        small
        v-on="on"
      >
        <v-icon
          dense
          small
        >
          mdi-dots-vertical
        </v-icon>
      </v-btn>
    </template>

    <v-list>
      <slot name="actions" />
    </v-list>
  </v-menu>
</template>
<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
@Component
export default class DotMenu extends Vue {
}
</script>
