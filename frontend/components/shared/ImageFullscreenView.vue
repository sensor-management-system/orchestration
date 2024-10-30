<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-fade-transition>
    <v-overlay
      v-if="value"
      opacity="0.8"
      z-index="99"
      @click="close"
    >
      <img :src="value">
    </v-overlay>
  </v-fade-transition>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'nuxt-property-decorator'

@Component
export default class ImageFullscreenView extends Vue {
  /**
   * The url of the image to display.
   */
  @Prop({
    required: false,
    type: String
  })
  private value!: string

  close () {
    this.$emit('input', null)
  }
}
</script>

<style scoped>
img {
  min-height: 70vh;
  min-width: 70vw;
  max-height: 90vh;
  max-width: 90vw;
  aspect-ratio: auto;
  object-fit: contain;
}
</style>
