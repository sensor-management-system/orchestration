<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-row
    v-if="value"
    class="mt-4"
    dense
  >
    <v-col
      class="text-caption font-weight-thin text-right"
    >
      <template
        v-if="createdBy"
      >
        created by {{ createdBy }}<span v-if="value.createdAt"> at {{ value.createdAt | toUtcDateTimeString }}</span><span v-if="updatedBy">,</span>
      </template>
      <template
        v-if="updatedBy"
      >
        updated by {{ updatedBy }}<span v-if="value.updatedAt"> at {{ value.updatedAt | toUtcDateTimeString }}</span>
      </template>
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { IMetaCreationInfo } from '@/models/MetaCreationInfo'
import { Contact } from '@/models/Contact'

@Component
export default class ModificationInfo extends Vue {
  /**
   * the visibility of the entity
   */
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: IMetaCreationInfo

  get createdBy (): string {
    if (!this.value.createdBy) {
      return ''
    }
    // as we just get an IContact we have to create a full Contact instance
    // again
    return Contact.createFromObject(this.value.createdBy).fullName
  }

  get updatedBy (): string {
    if (!this.value.updatedBy) {
      return ''
    }
    // as we just get an IContact we have to create a full Contact instance
    // again
    return Contact.createFromObject(this.value.updatedBy).fullName
  }
}
</script>
