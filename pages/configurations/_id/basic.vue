<template>
  <NuxtChild
    :value="configuration"
  />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { Configuration } from '@/models/Configuration'

@Component
export default class ConfigurationBasic extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  get configuration (): Configuration {
    return this.value
  }

  set configuration (value: Configuration) {
    this.$emit('input', value)
  }
}
</script>
