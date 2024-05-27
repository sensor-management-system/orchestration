<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
