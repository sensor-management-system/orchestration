<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item expandable-color="grey lighten-5" background-color="white">
    <template #actions>
      <v-btn
        :to="detailLink"
        color="primary"
        text
        small
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #default>
      {{ organization.name }}
    </template>
    <template #expandable>
      <v-row no-gutters>
        <v-col cols="3" md="3" class="font-weight-medium">
          ROR:
        </v-col>
        <v-col cols="3" md="3" class="nowrap-truncate">
          {{ organization.ror | orDefault }}
        </v-col>
        <v-col cols="3" md="3" class="font-weight-medium">
          Abbreviation:
        </v-col>
        <v-col cols="3" md="3" class="nowrap-truncate">
          {{ organization.abbreviation | orDefault }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { Organization } from '@/models/Organization'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

@Component({
  components: {
    BaseExpandableListItem
  }
})
export default class OrganizationsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private organization!: Organization

  @Prop({
    default: '',
    type: String
  })
  private from!: string

  get detailLink (): string {
    let params = ''
    if (this.from) {
      params = '?' + (new URLSearchParams({ from: this.from })).toString()
    }
    return `/organizations/${this.organization.id}${params}`
  }
}
</script>
