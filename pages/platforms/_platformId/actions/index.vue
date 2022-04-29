<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
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
      v-else
      :value="actions"
    >
      <template #generic-action="{action}">
        <GenericActionCard
          :value="action"
        >
          <template #actions>
            <v-btn
              v-if="$auth.loggedIn"
              :to="'/platforms/' + platformId + '/actions/generic-platform-actions/' + action.id + '/edit'"
              color="primary"
              text
              @click.stop.prevent
            >
              Edit
            </v-btn>
          </template>
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
          <template #actions>
            <v-btn
              v-if="$auth.loggedIn"
              :to="'/platforms/' + platformId + '/actions/software-update-actions/' + action.id + '/edit'"
              color="primary"
              text
              @click.stop.prevent
            >
              Edit
            </v-btn>
          </template>
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
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import PlatformMountActionCard from '@/components/actions/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/actions/PlatformUnmountActionCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Platform } from '@/models/Platform'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { mapActions, mapGetters } from 'vuex'

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
  private isSaving: boolean = false
  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private showDeleteDialog: boolean = false

  get platformId (): string {
    return this.$route.params.platformId
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
    try {
      this.isSaving = true
      await this.deletePlatformGenericAction(this.genericActionToDelete!.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Generic action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Generic action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }

  async deleteSoftwareUpdateAction () {
    try {
      this.isSaving = true
      await this.deletePlatformSoftwareUpdateAction(this.softwareUpdateActionToDelete!.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>
