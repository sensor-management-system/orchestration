<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
  <base-expandable-list-item>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template
      v-if="to"
      #actions
    >
      <v-btn
        v-if="editable"
        color="primary"
        text
        small
        nuxt
        :to="to"
      >
        Edit
      </v-btn>
    </template>
    <template #default>
      <v-row
        no-gutters
      >
        <v-col>
          <label>Key:</label>
          {{ value.key | shortenRight(40) }}
        </v-col>
        <v-col>
          <label>Value:</label>
          {{ value.value | shortenRight }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

import { CustomTextField } from '@/models/CustomTextField'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

@Component({
  components: {
    BaseExpandableListItem
  }
})
export default class CustomFieldListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private value!: CustomTextField

  @Prop({
    default: null,
    required: false,
    type: [String, Object]
  })
  private to!: RawLocation | null

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private editable!: boolean
}
</script>
