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
      v-if="!isCancelBtnHidden"
      color="secondary"
      class="mr-1"
      :disabled="isCancelBtnDisabled"
      @click="$nuxt.$emit('AppBarContent:cancel-button-click')"
    >
      Cancel
    </v-btn>
    <v-btn
      v-if="!isSaveBtnHidden"
      color="primary"
      :disabled="isSaveBtnDisabled"
      @click="$nuxt.$emit('AppBarContent:save-button-click')"
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
import { Vue, Component } from 'nuxt-property-decorator'

/**
 * A class component to provide a title and two buttons in the App-Bar
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AppBarEditModeContent extends Vue {
  private title: string = ''
  private saveBtnHidden: boolean = true
  private cancelBtnHidden: boolean = true
  private saveBtnDisabled: boolean = false
  private cancelBtnDisabled: boolean = false

  get isSaveBtnHidden () {
    return this.saveBtnHidden
  }

  get isCancelBtnHidden () {
    return this.cancelBtnHidden
  }

  get isSaveBtnDisabled () {
    return this.saveBtnDisabled
  }

  get isCancelBtnDisabled () {
    return this.cancelBtnDisabled
  }

  created () {
    this.$nuxt.$on('AppBarContent:title', (title: string) => {
      this.title = title
    })
    this.$nuxt.$on('AppBarContent:save-button-hidden', (hidden: boolean) => {
      this.saveBtnHidden = hidden
    })
    this.$nuxt.$on('AppBarContent:save-button-disabled', (disabled: boolean) => {
      this.saveBtnDisabled = disabled
    })
    this.$nuxt.$on('AppBarContent:cancel-button-hidden', (hidden: boolean) => {
      this.cancelBtnHidden = hidden
    })
    this.$nuxt.$on('AppBarContent:cancel-button-disabled', (disabled: boolean) => {
      this.cancelBtnDisabled = disabled
    })
  }
}
</script>
