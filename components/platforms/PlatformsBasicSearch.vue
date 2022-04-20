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
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-tab-item>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'
import { Prop } from 'nuxt-property-decorator'

@Component({
  components: { PlatformsBasicSearchField }
})
export default class PlatformsBasicSearch extends Vue {
  @Prop({
    required: true,
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

  clearSearch () {
    this.searchText = null
  }

}
</script>

<style scoped>

</style>
