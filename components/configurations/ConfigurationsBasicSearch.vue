<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
  <v-row>
    <v-col cols="12" md="5">
      <v-text-field
        v-model="searchTextModel"
        label="Label"
        placeholder="Label of configuration"
        hint="Please enter at least 3 characters"
        @keydown.enter="emitSearch"
      />
    </v-col>
    <v-col
      cols="12"
      md="7"
      align-self="center"
    >
      <v-btn
        color="primary"
        small
        @click="emitSearch"
      >
        Search
      </v-btn>
      <v-btn
        text
        small
        @click="clearSearch"
      >
        Clear
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { IConfigurationBasicSearchParams } from '@/modelUtils/ConfigurationSearchParams'

@Component
export default class ConfigurationsBasicSearch extends Vue {
  @Prop({
    default: '',
    required: false,
    type: String
  })
  private readonly searchText!: string

  private internalSearchText: string | null = null

  get searchTextModel (): string | null {
    return this.internalSearchText || this.searchText
  }

  set searchTextModel (value: string | null) {
    this.internalSearchText = value
  }

  emitSearch () {
    this.$emit('search', {
      searchText: this.searchTextModel
    } as IConfigurationBasicSearchParams)
  }

  clearSearch () {
    this.searchTextModel = null
  }
}
</script>

<style scoped>

</style>
