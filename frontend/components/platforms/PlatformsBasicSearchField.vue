<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-text-field
    v-model="text"
    label="Name"
    placeholder="Name of platform"
    hint="Please enter at least 3 characters"
    @keydown.enter="emitKeydown"
  />
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

@Component
export default class PlatformsBasicSearchField extends Vue {
  @Prop({
    required: true
  })
  readonly value!: string|null

  get text () {
    return this.value
  }

  set text (newVal) {
    this.$emit('input', newVal)
  }

  emitKeydown () {
    this.$emit('start-search')
  }
}
</script>

<style scoped>

</style>
