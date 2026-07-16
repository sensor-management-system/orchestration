<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <label>Name</label>
        {{ value.name }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>ROR</label>
        {{ value.ror | orDefault }}
        <a v-if="value.ror && value.ror.length > 0" :href="ensureHttpOrHttpsPrefix(value.ror)" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="6">
        <label>Abbreviation</label>
        {{ value.abbreviation | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, mixins, Prop } from 'nuxt-property-decorator'
import { Organization } from '@/models/Organization'
import { ExternalUrlLinkMixin } from '@/mixins/ExternalUrlLinkMixin'

@Component({})
export default class OrganizationBasicData extends mixins(ExternalUrlLinkMixin) {
  @Prop({
    default: () => new Organization(),
    type: Organization
  })
  readonly value!: Organization
}
</script>
<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
