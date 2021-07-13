<template>
  <v-dialog
    v-model="hasActionToDelete"
    max-width="290"
    @click:outside="hideDeleteDialog"
  >
    <v-card>
      <v-card-title class="headline">
        Delete action
      </v-card-title>
      <v-card-text>
        Do you really want to delete the action?
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="hideDeleteDialog()"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          color="error"
          text
          @click="deleteAction()"
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class PlatformActionDeleteDialog extends Vue {
  @Prop({ type: String, required: true }) platformId!:string;

  get actionIdToDelete (): string | null {
    return this.$store.state.smsActions.actionIdToDelete
  }

  get hasActionToDelete () {
    return this.actionIdToDelete !== null
  }

  get actionDeleteMethod () {
    return this.$api.platforms.deleteRelatedGenericActionsById
  }

  hideDeleteDialog () {
    this.$store.commit('smsActions/setActionIdToDelete', null)
  }

  deleteAction (): void {
    if (!this.hasActionToDelete) {
      return
    }

    this.isSaving = true
    this.$api.genericPlatformActions.deleteById(this.actionIdToDelete).then(() => {
      this.$emit('update')
      this.$store.commit('snackbar/setSuccess', 'Action deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Action could not be deleted')
    }).finally(() => {
      this.hideDeleteDialog()
      this.isSaving = false
    })
  }
}
</script>

<style scoped>

</style>
