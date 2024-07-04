<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-container class="d-flex fill-height align-center align-content-center">
    <v-row>
      <v-col class="text-center" cols="12">
        <v-icon size="80">
          mdi-image-off-outline
        </v-icon><br>
      </v-col>
      <v-col class="text-center">
        <v-label>The image is not available.</v-label>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class ImageNotAvailable extends Vue {}
</script>
