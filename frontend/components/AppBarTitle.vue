<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
  <div class="v-toolbar__content" style="width:100%">
    <v-btn
      v-if="showBackButton"
      :to="backTo"
      icon
      title="Back to the search result"
      @click="$emit('back-click', $event)"
    >
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <v-toolbar-title>{{ title }}</v-toolbar-title>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component with save and cancel buttons for the App-Bar
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

/**
 * A class component to provide a title and two buttons in the App-Bar
 * @extends Vue
 */
@Component
export default class AppBarTitle extends Vue {
  /**
   * the Appbar title
   */
  @Prop({
    default: '',
    type: String
  })
  readonly title!: string

  /**
   * whether to show the back button or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  readonly showBackButton!: boolean

  /**
   * title of the back button
   */
  @Prop({
    default: '',
    type: String
  })
  readonly backButtonTitle!: string

  /**
   * link of the back button
   */
  @Prop({
    default: '',
    type: String
  })
  readonly backButtonTo!: string

  /**
   * link of the back button
   */
  @Prop({
    default: '',
    type: [Object, String]
  })
  readonly backTo!: RawLocation
}
</script>
