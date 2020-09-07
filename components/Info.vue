<template>
  <v-alert
    border="left"
    colored-border
    type="info"
    elevation="2"
    dismissible
  >
    <slot />
  </v-alert>
</template>

<script lang="ts">
/**
 * @file provides a component to show an info text
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component } from 'nuxt-property-decorator'

/**
 * A class component to show an info text
 * @extends Vue
 */
@Component
// @ts-ignore
export default class Info extends Vue {
}
</script>
