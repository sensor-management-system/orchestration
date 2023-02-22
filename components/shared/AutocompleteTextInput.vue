/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

<template>
  <v-combobox
    v-bind="$attrs"
    :items="suggestionsWithHeader"
    :loading="loading"
    v-on="$listeners"
    @update:search-input="updateValue"
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
  </v-combobox>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component({})
export default class AutocompleteTextInput extends Vue {
  @Prop({
    required: true,
    type: String
  })
  readonly endpoint!: string

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
      this.autocompleteItems = await this.$api.autocomplete.getSuggestions(endpoint)
    } catch (_error) {
    } finally {
      this.loading = false
    }
  }

  updateValue (value: string) {
    this.$emit('input', value)
  }
}
</script>
