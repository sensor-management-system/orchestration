<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <span v-if="index < maxEntriesShown && needComma">{{ itemText }},&nbsp;</span>
    <span v-if="index < maxEntriesShown && !needComma">{{ itemText }}</span>
    <span
      v-if="index === maxEntriesShown"
      class="grey--text text-caption"
    >&nbsp;(+{{ selection.length - maxEntriesShown }} {{ pluralize(selection.length-maxEntriesShown,'other') }})</span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { pluralize } from '@/utils/stringHelpers'

@Component({
  methods: { pluralize }
})
export default class MultipleSelectionAbbrevation extends Vue {
  @Prop({
    required: true,
    type: Number
  })
  readonly index!: number

  @Prop({
    required: true,
    type: String
  })
  readonly itemText!: string

  @Prop({
    required: true,
    type: Array
  })
  readonly selection!: Array<Object>

  @Prop({
    required: false,
    default: 3,
    type: Number
  })
  readonly maxEntriesShown!: number

  get needComma (): boolean {
    return this.index !== (Math.min(this.maxEntriesShown, this.selection.length) - 1)
  }
}
</script>

<style scoped>

</style>
