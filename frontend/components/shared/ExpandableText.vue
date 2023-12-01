<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Rubankumar Moorthy (FZJ, r.moorthy@fz-juelich.de)
- Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
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
