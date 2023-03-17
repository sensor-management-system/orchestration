<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
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
          :is-public="isPublic"
          @open-attachment="openAttachment"
        >
          <template #actions>
            <v-btn
              v-if="editable"
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
              :readonly="!editable"
              @click="initDeleteDialogGenericAction(action)"
            />
          </template>
        </GenericActionCard>
      </template>

      <template #software-update-action="{action}">
        <SoftwareUpdateActionCard
          :value="action"
          target="Platform"
          :is-public="isPublic"
          @open-attachment="openAttachment"
        >
          <template #actions>
            <v-btn
              v-if="editable"
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
              :readonly="!editable"
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
    <DeleteDialog
      v-if="actionToDelete"
      v-model="showDeleteDialog"
      title="Delete Action"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the action?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import {
  ActionsGetter,
  LoadAllPlatformActionsAction,
  DeletePlatformSoftwareUpdateActionAction,
  DeletePlatformGenericActionAction,
  DownloadAttachmentAction,
  PlatformsState
} from '@/store/platforms'

import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import HintCard from '@/components/HintCard.vue'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import PlatformMountActionCard from '@/components/actions/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/actions/PlatformUnmountActionCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Attachment } from '@/models/Attachment'
import { Visibility } from '@/models/Visibility'

@Component({
  components: {
    ProgressIndicator,
    PlatformUnmountActionCard,
    PlatformMountActionCard,
    SoftwareUpdateActionCard,
    DeleteDialog,
    DotMenuActionDelete,
    GenericActionCard,
    HintCard,
    PlatformActionTimeline
  },
  computed: {
    ...mapGetters('platforms', ['actions']),
    ...mapState('platforms', ['platform'])
  },
  methods: mapActions('platforms', [
    'loadAllPlatformActions',
    'deletePlatformSoftwareUpdateAction',
    'deletePlatformGenericAction',
    'downloadAttachment'
  ])
})
export default class PlatformActionsShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private isSaving: boolean = false
  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private showDeleteDialog: boolean = false

  // vuex definition for typescript check
  actions!: ActionsGetter
  platform!: PlatformsState['platform']
  loadAllPlatformActions!: LoadAllPlatformActionsAction
  deletePlatformGenericAction!: DeletePlatformGenericActionAction
  deletePlatformSoftwareUpdateAction!: DeletePlatformSoftwareUpdateActionAction
  downloadAttachment!: DownloadAttachmentAction

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

  deleteAndCloseDialog () {
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
    if (this.genericActionToDelete === null || this.genericActionToDelete.id === null) {
      return
    }

    try {
      this.isSaving = true
      await this.deletePlatformGenericAction(this.genericActionToDelete.id)
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
    if (this.softwareUpdateActionToDelete === null || this.softwareUpdateActionToDelete.id === null) {
      return
    }

    try {
      this.isSaving = true
      await this.deletePlatformSoftwareUpdateAction(this.softwareUpdateActionToDelete.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }

  async openAttachment (attachment: Attachment) {
    try {
      const blob = await this.downloadAttachment(attachment.url)
      const url = window.URL.createObjectURL(blob)
      window.open(url)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Attachment could not be loaded')
    }
  }

  get isPublic (): boolean {
    return (this.platform?.visibility === Visibility.Public) || false
  }
}
</script>

<style scoped>

</style>
