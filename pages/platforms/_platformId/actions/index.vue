<template>
<div>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="$auth.loggedIn"
      color="primary"
      small
      :to="'/platforms/' + platformId + '/actions/new'"
    >
      Add Action
    </v-btn>
  </v-card-actions>
  <hint-card v-if="actions.length === 0">
    There are no actions for this platform.
  </hint-card>
  <PlatformActionTimeline
    :value="actions"
    :platform-id="platformId"
    :action-api-dispatcher="apiDispatcher"
    :is-user-authenticated="$auth.loggedIn"
  >
    <template #generic-action="{action}">
      <GenericActionCard
        :value="action"
      >
        <template #dot-menu-items>
          <DotMenuActionDelete
            :readonly="!$auth.loggedIn"
            @click="initDeleteDialog(action)"
          />
        </template>
      </GenericActionCard>
    </template>
  </PlatformActionTimeline>
  <ActionDeleteDialog
    v-model="showDeleteDialog"
    :action-to-delete="actionToDelete"
    @cancel-deletion="closeDialog"
    @submit-deletion="deleteAndCloseDialog"
  />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import HintCard from '@/components/HintCard.vue'
import { mapGetters } from 'vuex'

import { PlatformActionApiDispatcher } from '@/modelUtils/actionHelpers'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'
import { Platform } from '@/models/Platform'

@Component({
  components: { ActionDeleteDialog, DotMenuActionDelete, GenericActionCard, HintCard, PlatformActionTimeline },
  computed:mapGetters('platforms',['actions'])
})
export default class PlatformActionsShowPage extends Vue {
  private actionToDelete = null
  private showDeleteDialog: boolean = false

  get platformId (): string {
    return this.$route.params.platformId
  }
  get apiDispatcher () { // Todo überarbeiten, da z.B. beim Löschen mit dieser Methode die Actions nicht neu geladen werden
    return new PlatformActionApiDispatcher(this.$api)
  }

  initDeleteDialog (action) {
    this.showDeleteDialog = true
    this.showDeleteDialog = action
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.showDeleteDialog = null
  }

  async deleteAndCloseDialog () {
    // if (this.platformToDelete === null || this.platformToDelete.id === null) {
    //   return
    // }
    // this.loading = true
    // try {
    //   await this.deletePlatform(this.platformToDelete.id)
    //   this.runSearch()
    //   this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    // } catch (_error) {
    //   this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    // } finally {
    //   this.loading = false
    //   this.closeDialog()
    // }
  }
}
</script>

<style scoped>

</style>
