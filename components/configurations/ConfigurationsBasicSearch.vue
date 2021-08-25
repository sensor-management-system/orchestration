<template>
  <v-tab-item :eager="true">
    <v-row>
      <v-col cols="12" md="5">
        <v-text-field v-model="searchText" label="Label" placeholder="Label of configuration" @keydown.enter="emitSearch" />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn
          color="primary"
          @click="emitSearch"
        >
          Search
        </v-btn>
        <v-btn
          text
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-tab-item>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class ConfigurationsBasicSearch extends Vue {
  private searchText:string|null=null

  emitSearch () {
    this.$emit('search', this.searchText)
  }

  clearSearch () {
    this.searchText = null
  }
}
</script>

<style scoped>

</style>
