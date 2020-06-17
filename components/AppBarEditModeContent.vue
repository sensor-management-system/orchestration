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
