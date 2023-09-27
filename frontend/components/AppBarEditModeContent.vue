<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
    <v-toolbar-title>{{ title }}</v-toolbar-title>
    <v-spacer />
    <v-btn
      v-if="!cancelBtnHidden"
      color="secondary"
      class="mr-1"
      :disabled="cancelBtnDisabled"
      @click="onCancelButtonClick($event)"
    >
      Cancel
    </v-btn>
    <v-btn
      v-if="!saveBtnHidden"
      color="primary"
      :disabled="saveBtnDisabled"
      @click="onSaveButtonClick($event)"
    >
      Save
    </v-btn>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component with save and cancel buttons for the App-Bar
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A class component to provide a title and two buttons in the App-Bar
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AppBarEditModeContent extends Vue {
  /**
   * the Appbar title
   */
  @Prop({
    default: '',
    type: String
  })
  // @ts-ignore
  readonly title: string

  /**
   * whether to hide the save button or not
   */
  @Prop({
    default: true,
    type: Boolean
  })
  // @ts-ignore
  readonly saveBtnHidden: boolean

  /**
   * whether to hide the cancel button or not
   */
  @Prop({
    default: true,
    type: Boolean
  })
  // @ts-ignore
  readonly cancelBtnHidden: boolean

  /**
   * whether to disable the save button or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly saveBtnDisabled: boolean

  /**
   * whether to disable the cancel button or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly cancelBtnDisabled: boolean

  /**
   * fires the cancel button click event
   *
   * @param {Event} event - the DOM event
   * @fires AppBarEditModeContent:cancel-btn-click
   */
  onCancelButtonClick (event: Event) {
    /**
     * fires the cancel button click event
     * @event AppBarEditModeContent:cancel-btn-click
     * @type {Event}
     */
    this.$nuxt.$emit('AppBarEditModeContent:cancel-btn-click', event)
  }

  /**
   * fires the save button click event
   *
   * @param {Event} event - the DOM event
   * @fires AppBarEditModeContent:save-btn-click
   */
  onSaveButtonClick (event: Event) {
    /**
     * fires the save button click event
     * @event AppBarEditModeContent:save-btn-click
     * @type {Event}
     */
    this.$nuxt.$emit('AppBarEditModeContent:save-btn-click', event)
  }
}
</script>
