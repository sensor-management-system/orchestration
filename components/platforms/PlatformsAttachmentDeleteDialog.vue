<template>
  <v-dialog
    v-model="showDialog"
    max-width="290"
    @click:outside="$emit('cancel-deletion')"
  >
    <v-card v-if="hasAttachmentToDelete">
      <v-card-title class="headline">
        Delete Attachment
      </v-card-title>
      <v-card-text>
        Do you really want to delete the attachment <em>{{ attachmentToDelete.label }}</em>?
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
import { Attachment } from '@/models/Attachment'

@Component
export default class PlatformsAttachmentDeleteDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly attachmentToDelete!: Attachment

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasAttachmentToDelete () {
    return this.attachmentToDelete !== null
  }
}
</script>

<style scoped>

</style>
