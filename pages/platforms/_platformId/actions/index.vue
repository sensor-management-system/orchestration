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
      <template #parameter-change-action="{action}">
        <ParameterChangeActionCard
          :value="action"
        >
          <template #actions>
            <v-btn
              v-if="editable"
              :to="'/platforms/' + platformId + '/actions/parameter-change-actions/' + action.id + '/edit'"
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
              @click="initDeleteDialogParameterChangeAction(action)"
            />
          </template>
        </ParameterChangeActionCard>
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
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedAttachmentFilename"
      :url="selectedAttachmentUrl"
      @cancel="closeDownloadDialog"
    />
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
  PlatformsState,
  DeletePlatformParameterChangeActionAction
} from '@/store/platforms'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { Visibility } from '@/models/Visibility'

import { getLastPathElement } from '@/utils/urlHelpers'

import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import HintCard from '@/components/HintCard.vue'
import ParameterChangeActionCard from '@/components/actions/ParameterChangeActionCard.vue'
import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import PlatformMountActionCard from '@/components/actions/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/actions/PlatformUnmountActionCard.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'

@Component({
  components: {
    DeleteDialog,
    DotMenuActionDelete,
    DownloadDialog,
    GenericActionCard,
    HintCard,
    ParameterChangeActionCard,
    PlatformActionTimeline,
    PlatformMountActionCard,
    PlatformUnmountActionCard,
    SoftwareUpdateActionCard
  },
  computed: {
    ...mapGetters('platforms', ['actions']),
    ...mapState('platforms', ['platform'])
  },
  methods: {
    ...mapActions('platforms', [
      'loadAllPlatformActions',
      'deletePlatformSoftwareUpdateAction',
      'deletePlatformGenericAction',
      'deletePlatformParameterChangeAction',
      'downloadAttachment'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformActionsShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private parameterChangeActionToDelete: ParameterChangeAction | null = null
  private showDeleteDialog: boolean = false

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  actions!: ActionsGetter
  platform!: PlatformsState['platform']
  loadAllPlatformActions!: LoadAllPlatformActionsAction
  deletePlatformGenericAction!: DeletePlatformGenericActionAction
  deletePlatformSoftwareUpdateAction!: DeletePlatformSoftwareUpdateActionAction
  deletePlatformParameterChangeAction!: DeletePlatformParameterChangeActionAction
  downloadAttachment!: DownloadAttachmentAction
  setLoading!: SetLoadingAction

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
    if (this.parameterChangeActionToDelete) {
      return this.parameterChangeActionToDelete
    }
    return null
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true
    this.genericActionToDelete = action
    this.softwareUpdateActionToDelete = null
    this.parameterChangeActionToDelete = null
  }

  initDeleteDialogSoftwareUpdateAction (action: SoftwareUpdateAction) {
    this.showDeleteDialog = true
    this.softwareUpdateActionToDelete = action
    this.genericActionToDelete = null
    this.parameterChangeActionToDelete = null
  }

  initDeleteDialogParameterChangeAction (action: ParameterChangeAction) {
    this.showDeleteDialog = true
    this.parameterChangeActionToDelete = action
    this.genericActionToDelete = null
    this.softwareUpdateActionToDelete = null
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

    try {
      switch (true) {
        case this.genericActionToDelete !== null:
          await this.deleteGenericAction()
          break
        case this.softwareUpdateActionToDelete !== null:
          await this.deleteSoftwareUpdateAction()
          break
        case this.parameterChangeActionToDelete !== null:
          await this.deleteParameterChangeAction()
          break
      }
    } finally {
      this.closeDialog()
    }
  }

  async deleteGenericAction () {
    if (this.genericActionToDelete === null || this.genericActionToDelete.id === null) {
      return
    }

    try {
      this.setLoading(true)
      await this.deletePlatformGenericAction(this.genericActionToDelete.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Generic action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Generic action could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  async deleteSoftwareUpdateAction () {
    if (this.softwareUpdateActionToDelete === null || this.softwareUpdateActionToDelete.id === null) {
      return
    }

    try {
      this.setLoading(true)
      await this.deletePlatformSoftwareUpdateAction(this.softwareUpdateActionToDelete.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  async deleteParameterChangeAction () {
    if (this.parameterChangeActionToDelete === null || this.parameterChangeActionToDelete.id === null) {
      return
    }

    try {
      this.setLoading(true)
      await this.deletePlatformParameterChangeAction(this.parameterChangeActionToDelete.id)
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Parameter value change action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Parameter value change action could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  initDowloadDialog (attachment: Attachment) {
    this.attachmentToDownload = attachment
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
    this.attachmentToDownload = null
  }

  openAttachment (attachment: Attachment) {
    this.initDowloadDialog(attachment)
  }

  get selectedAttachmentFilename (): string {
    if (this.attachmentToDownload) {
      return getLastPathElement(this.attachmentToDownload.url)
    }
    return 'attachment'
  }

  async selectedAttachmentUrl (): Promise<string | null> {
    if (!this.attachmentToDownload) {
      return null
    }
    try {
      const blob = await this.downloadAttachment(this.attachmentToDownload.url)
      const url = window.URL.createObjectURL(blob)
      return url
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Attachment could not be loaded')
    }
    return null
  }

  get isPublic (): boolean {
    return (this.platform?.visibility === Visibility.Public) || false
  }
}
</script>

<style scoped>

</style>
