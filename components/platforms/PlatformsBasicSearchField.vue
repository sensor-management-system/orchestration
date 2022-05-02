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
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'

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
