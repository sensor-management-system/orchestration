<template>
  <v-card
    class="mb-2"
  >
    <v-card-text>
      <v-row
        no-gutters
      >
        <v-col
          cols="12"
          md="2"
        >
          <label>Key:</label>
          {{ value.key }}
        </v-col>
        <v-col
          cols="12"
          md="8"
        >
          <label>Value:</label>
          {{ value.value }}
        </v-col>
        <v-col
          cols="12"
          md="2"
          class="text-right"
          align-self="center"
        >
          <slot name="actions" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { CustomTextField } from '@/models/CustomTextField'

@Component
export default class CustomFieldCard extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  get field (): CustomTextField {
    return this.value
  }

  set field (value: CustomTextField) {
    this.$emit('input', value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
