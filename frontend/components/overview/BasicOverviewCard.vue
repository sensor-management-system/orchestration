<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
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
      <span class="text-h6 font-weight-bold">{{ entityName }}s</span>
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
        <span>Go to {{ entityName }}s</span>
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
