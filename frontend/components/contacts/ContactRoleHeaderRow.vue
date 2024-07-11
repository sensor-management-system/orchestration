<!--
SPDX-FileCopyrightText: 2022 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-row no-gutters>
    <v-col cols="12" md="11" sm="11">
      <p class="text-subtitle-1 mb-0">
        {{ value.contact.toString() }}
        <v-badge :content="value.roleName" inline />
      </p>
    </v-col>
    <v-col
      cols="12"
      md="1"
      sm="1"
      align-self="end"
      class="text-right"
    >
      <!-- And after our main information, we have a slot to add the actions. -->
      <slot />
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { ContactRole } from '@/models/ContactRole'

@Component({})
export default class ContactRoleHeaderRow extends Vue {
  @Prop({
    type: Object,
    required: true
  })
  private readonly value!: ContactRole
}
</script>
