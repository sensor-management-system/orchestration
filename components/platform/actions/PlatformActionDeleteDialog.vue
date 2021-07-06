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

<script>
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class PlatformActionDeleteDialog extends Vue {
  get hasActionToDelete () {
    return this.$store.state.smsActions.actionIdToDelete !== null
  }

  hideDeleteDialog () {
    this.$store.commit('smsActions/removeActionId')
  }
}
</script>

<style scoped>

</style>
