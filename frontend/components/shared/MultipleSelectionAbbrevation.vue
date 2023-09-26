<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
