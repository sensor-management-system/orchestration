/**
 * @license
 * SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 */

<template>
  <combobox
    ref="combobox"
    v-bind="$attrs"
    :items="suggestionsWithHeader"
    :loading="loading"
    validate-on-blur
    v-on="$listeners"
    @focus="loadSuggestions(endpoint)"
  >
    <!-- pass through scoped slots -->
    <template v-for="(_, name) in $scopedSlots" #[name]="data">
      <slot :name="name" v-bind="data" />
    </template>

    <!-- pass through normal slots -->
    <template v-for="(_, name) in $slots" #[name]>
      <slot :name="name" />
    </template>
  </combobox>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import Combobox from '@/components/shared/Combobox.vue'

@Component({
  components: {
    Combobox
  }
})
export default class AutocompleteTextInput extends Vue {
  @Prop({
    required: true,
    type: String
  })
  readonly endpoint!: string

  @Prop({
    default: () => {},
    type: Object
  })
  readonly filters!: Object

  private loading = false
  private autocompleteItems: string[] = []

  get suggestionsWithHeader () {
    const header = {
      header: ''
    }
    if (this.autocompleteItems.length > 0) {
      header.header = 'Pick a suggestion or add a new entry'
    } else {
      header.header = 'No suggestions available'
    }
    const items = [header, ...this.autocompleteItems]
    return items
  }

  async loadSuggestions (endpoint: string) {
    this.loading = true
    try {
      this.autocompleteItems = await this.$api.autocomplete.getSuggestions(endpoint, this.filters)
    } catch (_error) {
    } finally {
      this.loading = false
    }
  }

  focus (): void {
    (this.$refs.combobox as Vue & { focus: () => void }).focus()
  }

  blur (): void {
    (this.$refs.combobox as Vue & { blur: () => void }).blur()
  }
}
</script>
