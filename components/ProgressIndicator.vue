<template>
  <div>
    <v-overlay
      :value="isInProgress"
      :opacity="dark ? 0.5 : 0.05"
    >
      <v-progress-circular
        indeterminate
        class="center-absolute"
      />
    </v-overlay>
  </div>
</template>

<style>
  .center-absolute {
    position: fixed;
    top: 50%;
    left: 50%;
    margin-top: -16px;
    margin-left: -16px;
  }
</style>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

@Component
export default class ProgressIndicator extends Vue {
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  // @ts-ignore
  readonly value!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  // @ts-ignore
  readonly dark!: boolean

  get isInProgress (): boolean {
    return this.value
  }
}
</script>
