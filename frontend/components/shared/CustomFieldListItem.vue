<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
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
    <template
      v-if="value.description"
      #expandable
    >
      <v-card-text
        class="py-2"
      >
        {{ value.description }}
      </v-card-text>
    </template>
    <template #default>
      <v-row
        no-gutters
      >
        <v-col>
          <label>Key:</label>
          <span @click.stop>
            <expandable-text
              :value="value.key"
              more-icon="mdi-unfold-more-vertical"
              less-icon="mdi-unfold-less-vertical"
            />
          </span>
        </v-col>
        <v-col>
          <label>Value:</label>
          <span @click.stop>
            <expandable-text
              :value="value.value"
              more-icon="mdi-unfold-more-vertical"
              less-icon="mdi-unfold-less-vertical"
            />
          </span>
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

import { CustomTextField } from '@/models/CustomTextField'

import { shortenRight } from '@/utils/stringHelpers'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    BaseExpandableListItem,
    ExpandableText
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

  private isKeyExpanded: boolean = false
  private isValueExpanded: boolean = false

  private shortenKeyLengthAt: number = 60
  private shortenValueLengthAt: number = 60

  get keyLengthExceedsDefault (): boolean {
    return this.value.key.length > this.shortenKeyLengthAt
  }

  get valueLengthExceedsDefault (): boolean {
    return this.value.value.length > this.shortenValueLengthAt
  }

  get shortenedKey (): string {
    return shortenRight(this.value.key, this.shortenKeyLengthAt)
  }

  get shortenedValue (): string {
    return shortenRight(this.value.value, this.shortenValueLengthAt)
  }
}
</script>
