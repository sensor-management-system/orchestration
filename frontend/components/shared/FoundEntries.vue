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
    {{ foundText }}
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { pluralize } from '@/utils/stringHelpers'

@Component
export default class FoundEntries extends Vue {
  @Prop({
    required: true,
    type: Number
  })
  readonly value!: number

  @Prop({
    required: true,
    type: String
  })
    entityName!: string

  @Prop({
    required: false,
    type: String,
    default: ''
  })
    entityNamePlural!: string

  get foundText (): String {
    return `${this.value} ${pluralize(this.value, this.entityName, this.entityNamePlural)} found`
  }
}
</script>

<style scoped>

</style>
