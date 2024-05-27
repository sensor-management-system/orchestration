<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
            <ExpandableText
              :value="value.key"
            />
          </span>
        </v-col>
        <v-col>
          <label>Value:</label>
          <span @click.stop>
            <ExpandableText
              :value="value.value"
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
