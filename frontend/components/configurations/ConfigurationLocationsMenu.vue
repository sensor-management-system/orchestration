<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-menu
    v-if="showMenu"
    close-on-click
    close-on-content-click
    offset-x
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
      <v-list-item
        v-if="showEdit"
        dense
        @click="$emit('edit-click')"
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-icon
              left
              small
            >
              mdi-pen
            </v-icon>
            Edit
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="showDelete"
        dense
        @click="$emit('delete-click')"
      >
        <v-list-item-content>
          <v-list-item-title
            class="red--text"
          >
            <v-icon
              left
              small
              color="red"
            >
              mdi-delete
            </v-icon>
            Delete
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

export type CallbackFunction = (event?: any) => any

@Component
export default class ConfigurationLocationMenu extends Vue {
  @Prop({
    default: true,
    type: Boolean
  })
  readonly showEdit!: boolean

  @Prop({
    default: true,
    type: Boolean
  })
  readonly showDelete!: boolean

  get showMenu (): boolean {
    return this.showEdit || this.showDelete
  }
}
</script>
