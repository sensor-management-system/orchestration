<template>
  <div class="v-toolbar__content" style="width:100%">
    <v-toolbar-title>{{ title }}</v-toolbar-title>
    <v-spacer />
    <v-btn v-if="!cancelBtnHidden" color="secondary" class="mr-1" :disabled="cancelBtnDisabled" @click="$nuxt.$emit('AppBarContent:cancel-button-click')">Cancel</v-btn>
    <v-btn v-if="!saveBtnHidden" color="primary" :disabled="saveBtnDisabled" @click="$nuxt.$emit('AppBarContent:save-button-click')">Save</v-btn>
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
  get title (): string {
    return ''
  }

  private saveBtnHidden: boolean = true
  private cancelBtnHidden: boolean = true
  private saveBtnDisabled: boolean = false
  private cancelBtnDisabled: boolean = false

  created () {
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
