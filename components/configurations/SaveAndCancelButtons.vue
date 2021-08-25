<template>
  <div>
    <v-btn
      small
      text
      nuxt
      :to="to"
    >
      cancel
    </v-btn>
    <v-btn
      color="green"
      small
      @click="$emit('save')"
    >
      apply
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class SaveAndCancelButtons extends Vue {
  @Prop({ default: false, type: String }) to!: string
}
</script>

<style scoped>

</style>
