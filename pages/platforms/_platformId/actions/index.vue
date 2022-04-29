<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card-actions>
      <v-spacer/>
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
              @click="initDeleteDialogGenericAction(action)"
            />
          </template>
        </GenericActionCard>
      </template>

      <template #software-update-action="{action}">
        <SoftwareUpdateActionCard
          :value="action"
          target="Platform"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialogSoftwareUpdateAction(action)"
            />
          </template>
        </SoftwareUpdateActionCard>
      </template>

      <template #platform-mount-action="{action}">
        <PlatformMountActionCard
          :value="action"
        />
      </template>

      <template #platform-unmount-action="{action}">
        <PlatformUnmountActionCard
          :value="action"
        />
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
import { mapActions, mapGetters } from 'vuex'

import { PlatformActionApiDispatcher } from '@/modelUtils/actionHelpers'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'
import { Platform } from '@/models/Platform'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import PlatformMountActionCard from '@/components/actions/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/actions/PlatformUnmountActionCard.vue'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator,
    PlatformUnmountActionCard,
    PlatformMountActionCard,
    SoftwareUpdateActionCard,
    ActionDeleteDialog,
    DotMenuActionDelete,
    GenericActionCard,
    HintCard,
    PlatformActionTimeline
  },
  computed: mapGetters('platforms', ['actions']),
  methods: mapActions('platforms', ['loadAllPlatformActions', 'deletePlatformSoftwareUpdateAction', 'deletePlatformGenericAction'])
})
export default class PlatformActionsShowPage extends Vue {
  private isLoading = false
  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private showDeleteDialog: boolean = false

  get platformId (): string {
    return this.$route.params.platformId
  }

  get apiDispatcher () { // Todo überarbeiten, da z.B. beim Löschen mit dieser Methode die Actions nicht neu geladen werden
    return new PlatformActionApiDispatcher(this.$api)
  }

  get actionToDelete () {
    if (this.genericActionToDelete) {
      return this.genericActionToDelete
    }

    if (this.softwareUpdateActionToDelete) {
      return this.softwareUpdateActionToDelete
    }
    return null
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true
    this.genericActionToDelete = action
    this.softwareUpdateActionToDelete = null
  }

  initDeleteDialogSoftwareUpdateAction (action: SoftwareUpdateAction) {
    this.showDeleteDialog = true
    this.softwareUpdateActionToDelete = action
    this.genericActionToDelete = null
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.softwareUpdateActionToDelete = null
    this.genericActionToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.actionToDelete === null || this.actionToDelete.id === null) {
      return
    }

    if (this.genericActionToDelete !== null && this.softwareUpdateActionToDelete === null) {
      this.deleteGenericAction()
    }

    if (this.softwareUpdateActionToDelete !== null && this.genericActionToDelete === null) {
      this.deleteSoftwareUpdateAction()
    }
  }

  async deleteGenericAction () {
    this.loading = true
    try {
      await this.deletePlatformGenericAction(this.genericActionToDelete!.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Generic action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Generic action could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  async deleteSoftwareUpdateAction () {
    this.loading = true
    try {
      await this.deletePlatformSoftwareUpdateAction(this.softwareUpdateActionToDelete!.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>
