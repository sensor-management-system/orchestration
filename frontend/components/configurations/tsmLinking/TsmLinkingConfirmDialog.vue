<!--
SPDX-FileCopyrightText: 2020 - 2025

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="20vw"
    @click:outside="$emit('cancel')"
  >
    <v-card>
      <v-card-title class="headline">
        {{ title }}
      </v-card-title>
      <v-card-text>
        <slot />
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="$emit('cancel')"
        >
          Cancel
        </v-btn>
        <v-spacer />
        <v-btn
          color="primary"
          text
          @click="$emit('confirm')"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

@Component
export default class TsmLinkingConfirmDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    default: '',
    required: false,
    type: String
  })
  readonly title!: string

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }
}
</script>

<style scoped>

</style>
