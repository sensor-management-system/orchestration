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
        :to="'/devices/' + deviceId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
    <hint-card v-if="actions.length === 0">
      There are no actions for this device.
    </hint-card>
    <DeviceActionTimeline
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
              :to="'/devices/' + deviceId + '/actions/generic-device-actions/' + action.id + '/edit'"
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
          target="Device"
          :is-public="isPublic"
          @open-attachment="openAttachment"
        >
          <template #actions>
            <v-btn
              v-if="editable"
              :to="'/devices/' + deviceId + '/actions/software-update-actions/' + action.id + '/edit'"
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
      <template #calibration-action="{action}">
        <DeviceCalibrationActionCard
          :value="action"
          :is-public="isPublic"
          @open-attachment="openAttachment"
        >
          <template #actions>
            <v-btn
              v-if="editable"
              :to="'/devices/' + deviceId + '/actions/device-calibration-actions/' + action.id + '/edit'"
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
              @click="initDeleteDialogCalibrationAction(action)"
            />
          </template>
        </DeviceCalibrationActionCard>
      </template>
      <template #device-mount-action="{action}">
        <DeviceMountActionCard
          :value="action"
        />
      </template>
      <template #device-unmount-action="{action}">
        <DeviceUnmountActionCard
          :value="action"
        />
      </template>
    </DeviceActionTimeline>
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
  DeleteDeviceSoftwareUpdateAction,
  DeleteDeviceGenericAction,
  DeleteDeviceCalibrationAction,
  LoadAllDeviceActionsAction,
  DevicesState,
  DownloadAttachmentAction
} from '@/store/devices'

import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

import HintCard from '@/components/HintCard.vue'
import DeviceActionTimeline from '@/components/actions/DeviceActionTimeline.vue'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeviceMountActionCard from '@/components/actions/DeviceMountActionCard.vue'
import DeviceUnmountActionCard from '@/components/actions/DeviceUnmountActionCard.vue'
import DeviceCalibrationActionCard from '@/components/actions/DeviceCalibrationActionCard.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import { Visibility } from '@/models/Visibility'
import { Attachment } from '@/models/Attachment'
import { getLastPathElement } from '@/utils/urlHelpers'

@Component({
  components: {
    SoftwareUpdateActionCard,
    ProgressIndicator,
    DeleteDialog,
    DeviceCalibrationActionCard,
    DeviceUnmountActionCard,
    DeviceMountActionCard,
    DotMenuActionDelete,
    GenericActionCard,
    DeviceActionTimeline,
    HintCard,
    DownloadDialog
  },
  computed: {
    ...mapGetters('devices', ['actions']),
    ...mapState('devices', ['device'])
  },
  methods: mapActions('devices', [
    'deleteDeviceSoftwareUpdateAction',
    'deleteDeviceGenericAction',
    'deleteDeviceCalibrationAction',
    'loadAllDeviceActions',
    'downloadAttachment'
  ])
})
export default class DeviceActionsShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private isSaving: boolean = false
  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private calibrationActionToDelete: DeviceCalibrationAction | null = null
  private showDeleteDialog: boolean = false

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  actions!: ActionsGetter
  device!: DevicesState['device']
  deleteDeviceGenericAction!: DeleteDeviceGenericAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
  deleteDeviceSoftwareUpdateAction!: DeleteDeviceSoftwareUpdateAction
  deleteDeviceCalibrationAction!: DeleteDeviceCalibrationAction
  downloadAttachment!: DownloadAttachmentAction

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionToDelete () {
    if (this.genericActionToDelete) {
      return this.genericActionToDelete
    }

    if (this.softwareUpdateActionToDelete) {
      return this.softwareUpdateActionToDelete
    }

    if (this.calibrationActionToDelete) {
      return this.calibrationActionToDelete
    }
    return null
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true

    this.genericActionToDelete = action
    this.softwareUpdateActionToDelete = null
    this.calibrationActionToDelete = null
  }

  initDeleteDialogSoftwareUpdateAction (action: SoftwareUpdateAction) {
    this.showDeleteDialog = true

    this.softwareUpdateActionToDelete = action
    this.genericActionToDelete = null
    this.calibrationActionToDelete = null
  }

  initDeleteDialogCalibrationAction (action: DeviceCalibrationAction) {
    this.showDeleteDialog = true

    this.calibrationActionToDelete = action
    this.softwareUpdateActionToDelete = null
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

    if (this.genericActionToDelete !== null && this.softwareUpdateActionToDelete === null && this.calibrationActionToDelete === null) {
      this.deleteGenericAction()
    }

    if (this.softwareUpdateActionToDelete !== null && this.genericActionToDelete === null && this.calibrationActionToDelete === null) {
      this.deleteSoftwareUpdateAction()
    }
    if (this.calibrationActionToDelete !== null && this.genericActionToDelete === null && this.softwareUpdateActionToDelete === null) {
      this.deleteCalibrationAction()
    }
  }

  async deleteGenericAction () {
    if (this.genericActionToDelete === null || this.genericActionToDelete.id === null) {
      return
    }

    try {
      this.isSaving = true
      await this.deleteDeviceGenericAction(this.genericActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
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
      await this.deleteDeviceSoftwareUpdateAction(this.softwareUpdateActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }

  async deleteCalibrationAction () {
    if (this.calibrationActionToDelete === null || this.calibrationActionToDelete.id === null) {
      return
    }

    try {
      this.isSaving = true
      await this.deleteDeviceCalibrationAction(this.calibrationActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Calibration action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Calibration action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
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
    return (this.device?.visibility === Visibility.Public) || false
  }
}
</script>

<style scoped>

</style>
