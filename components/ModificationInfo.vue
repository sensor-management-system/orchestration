<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
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
