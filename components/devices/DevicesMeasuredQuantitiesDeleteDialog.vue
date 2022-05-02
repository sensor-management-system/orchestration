<template>
  <v-dialog
    v-model="showDialog"
    max-width="290"
    @click:outside="$emit('cancel-deletion')"
  >
    <v-card v-if="hasMeasuredQuantityToDelete">
      <v-card-title class="headline">
        Delete Measured Quantity
      </v-card-title>
      <v-card-text>
        Do you really want to delete the field <em>{{ measuredQuantity.label }}</em>?
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
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'

@Component
export default class DevicesCustomFieldDeleteDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly measuredQuantity!: DeviceProperty

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasMeasuredQuantityToDelete () {
    return this.measuredQuantity !== null
  }
}
</script>

<style scoped>

</style>
