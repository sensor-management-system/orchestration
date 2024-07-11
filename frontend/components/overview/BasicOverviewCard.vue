<!--
SPDX-FileCopyrightText: 2022 - 2024
- Erik Pongratz <erik.pongratz@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-card class="mx-auto d-flex flex-column" min-height="100%">
    <v-card-title class="primary white--text rounded rounded-b-0">
      <v-icon
        left
        color="white"
      >
        {{ icon }}
      </v-icon>
      <span class="text-h6 font-weight-bold">{{ entityNamePlural }}</span>
    </v-card-title>

    <v-divider />

    <v-card-text class="primary_text--text">
      {{ description }}
    </v-card-text>
    <v-spacer />
    <v-divider />

    <v-card-actions>
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-btn :to="url" color="primary" v-on="on">
            <v-icon>{{ icon }}</v-icon>
          </v-btn>
        </template>
        <span>Go to {{ entityNamePlural }}</span>
      </v-tooltip>

      <v-spacer />

      <v-tooltip v-if="isLoggedIn" bottom>
        <template #activator="{ on }">
          <v-btn :to="url + '/new'" color="accent" v-on="on">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <span>Create new {{ entityName }}</span>
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class BasicOverviewCard extends Vue {
  @Prop({
    type: String,
    required: true
  })
  private entityName!: string

  @Prop({
    type: String,
    required: true
  })
  private entityNamePlural!: string

  @Prop({
    type: String,
    required: true
  })
  private description!: string

  @Prop({
    type: String,
    required: true
  })
  private url!: string

  @Prop({
    type: String,
    required: true
  })
  private icon!: string

  get isLoggedIn () {
    return this.$auth.loggedIn
  }
}
</script>

<style scoped>

</style>
