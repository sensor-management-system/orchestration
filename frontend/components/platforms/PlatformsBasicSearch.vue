<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-tab-item :eager="true">
    <v-row>
      <v-col cols="12" md="5">
        <PlatformsBasicSearchField
          v-model="searchText"
          @start-search="emitSearch"
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
          @click="emitClear"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-tab-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'

@Component({
  components: { PlatformsBasicSearchField }
})
export default class PlatformsBasicSearch extends Vue {
  @Prop({
    required: true
  })
  readonly value!: string | null

  get searchText () {
    return this.value
  }

  set searchText (newVal) {
    this.$emit('input', newVal)
  }

  emitSearch () {
    this.$emit('search')
  }

  emitClear () {
    this.$emit('clear')
  }
}
</script>

<style scoped>

</style>
