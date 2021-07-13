<template>
  <div>
    <v-btn
      small
      text
      nuxt
      :to="cancelUrl"
    >
      cancel
    </v-btn>
    <v-btn
      v-if="showApply"
      color="green"
      small
      :disabled="isSaving"
      @click="$emit('apply')"
    >
      apply
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

@Component
export default class PlatformActionCancelAddButtons extends Vue {
  @Prop({ type: String, required: true }) cancelUrl!:string;
  @Prop({ type: Boolean, required: true }) isSaving!:boolean;
  @Prop({ type: Boolean, default: true }) showApply!:boolean;
}
</script>

<style scoped>

</style>
