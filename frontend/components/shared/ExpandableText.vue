<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Rubankumar Moorthy <r.moorthy@fz-juelich.de>
- Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div class="d-inline">
    <span
      v-if="valueLengthExceedsDefault && !isValueExpanded"
    >
      {{ shortenedValue }}
    </span>
    <span
      v-else
      class="word-break-text"
    >
      {{ value | orDefault }}
    </span>
    <v-btn
      v-if="valueLengthExceedsDefault"
      icon
      small
      :title="isValueExpanded ? 'show less' : 'show more'"
      @click.stop.prevent="isValueExpanded = !isValueExpanded"
    >
      <v-icon
        small
      >
        {{ isValueExpanded ? lessIcon : moreIcon }}
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { shortenRight } from '@/utils/stringHelpers'

@Component
export default class ExpandableText extends Vue {
    @Prop({
      default: 'mdi-unfold-more-vertical',
      required: false,
      type: String
    })
  private moreIcon!: string

    @Prop({
      default: 'mdi-unfold-less-vertical',
      required: false,
      type: String
    })
    private lessIcon!: string

    @Prop({
      required: true,
      type: String
    })
    private value!: string

    @Prop({
      default: 60,
      required: false,
      type: Number
    })
    private shortenAt!: number

    private isValueExpanded: boolean = false

    get valueLengthExceedsDefault (): boolean {
      return this.value.length > this.shortenAt
    }

    get shortenedValue (): string {
      return shortenRight(this.value, this.shortenAt)
    }
}
</script>

<style scoped>
.word-break-text {
  word-break: break-word;
}
</style>
