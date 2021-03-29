<template>
  <NuxtChild
    v-model="platform"
  />
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'

@Component
export default class PlatformBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Platform

  get platform (): Platform {
    return this.value
  }

  set platform (value: Platform) {
    this.$emit('input', value)
  }
}
</script>
