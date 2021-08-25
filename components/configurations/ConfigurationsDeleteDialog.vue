<template>
  <v-dialog
    v-model="showDialog"
    max-width="290"
    @click:outside="$emit('cancel-deletion')"
  >
    <v-card v-if="hasConfigurationToDelete">
      <v-card-title class="headline">
        Delete configuration
      </v-card-title>
      <v-card-text>
        Do you really want to delete the configuration <em>{{ configurationToDelete.label }}</em>
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="$emit('cancel-deletion')"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          color="error"
          text
          @click="$emit('submit-deletion')"
        >
          <v-icon left>
            mdi-delete
          </v-icon>
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

@Component
export default class ConfigurationsDeleteDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  configurationToDelete!: Configuration

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasConfigurationToDelete () {
    return this.configurationToDelete !== null
  }
}
</script>

<style scoped>

</style>
