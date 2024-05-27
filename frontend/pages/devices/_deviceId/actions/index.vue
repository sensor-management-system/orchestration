<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-container v-if="!(actions.length === 0 && !isFilterUsed)">
        <DeviceActionsFilter
          v-model="filter"
        />
      </v-container>
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
    <hint-card v-if="actions.length === 0 && !isFilterUsed">
      There are no actions for this device.
    </hint-card>
    <hint-card v-if="actions.length === 0 && isFilterUsed">
      There are no actions that match the filter criteria.
    </hint-card>
    <DeviceActionTimeline
      v-if="actions.length > 0"
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
      <template #parameter-change-action="{action}">
        <ParameterChangeActionCard
          :value="action"
        >
          <template #actions>
            <v-btn
              v-if="editable"
              :to="'/devices/' + deviceId + '/actions/parameter-change-actions/' + action.id + '/edit'"
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
      <template #device-mount-action="{action}">
        <MountActionCard :value="action" />
      </template>
      <template #device-unmount-action="{action}">
        <UnmountActionCard :value="action" />
      </template>
    </DeviceActionTimeline>

    <v-card-actions
      v-if="actions.length>3"
    >
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

    <DeleteDialog
      v-if="actionToDelete"
      v-model="showDeleteDialog"
      title="Delete Action"
      :disabled="isLoading"
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
  DeleteDeviceSoftwareUpdateAction,
  DeleteDeviceGenericAction,
  DeleteDeviceCalibrationAction,
  DeleteDeviceParameterChangeActionAction,
  LoadAllDeviceActionsAction,
  DevicesState,
  DownloadAttachmentAction,
  FilteredActionsGetter,
  DeviceFilter
} from '@/store/devices'

import { Attachment } from '@/models/Attachment'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { GenericAction } from '@/models/GenericAction'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { Visibility } from '@/models/Visibility'

import { getLastPathElement } from '@/utils/urlHelpers'

import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DeviceActionTimeline from '@/components/actions/DeviceActionTimeline.vue'
import DeviceCalibrationActionCard from '@/components/actions/DeviceCalibrationActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import HintCard from '@/components/HintCard.vue'
import ParameterChangeActionCard from '@/components/actions/ParameterChangeActionCard.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import MountActionCard from '@/components/actions/MountActionCard.vue'
import UnmountActionCard from '@/components/actions/UnmountActionCard.vue'
import { LoadDeviceGenericActionTypesAction } from '@/store/vocabulary'
import DeviceActionsFilter from '@/components/devices/DeviceActionsFilter.vue'

@Component({
  components: {
    DeviceActionsFilter,
    UnmountActionCard,
    MountActionCard,
    SoftwareUpdateActionCard,
    DeleteDialog,
    DeviceActionTimeline,
    DeviceCalibrationActionCard,
    DotMenuActionDelete,
    DownloadDialog,
    GenericActionCard,
    HintCard,
    ParameterChangeActionCard
  },
  computed: {
    ...mapGetters('devices', ['filteredActions']),
    ...mapState('devices', ['device']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadDeviceGenericActionTypes']),
    ...mapActions('devices', [
      'deleteDeviceSoftwareUpdateAction',
      'deleteDeviceGenericAction',
      'deleteDeviceCalibrationAction',
      'deleteDeviceParameterChangeAction',
      'loadAllDeviceActions',
      'downloadAttachment'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceActionsShowPage extends Vue {
  @InjectReactive()
  private editable!: boolean

  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private calibrationActionToDelete: DeviceCalibrationAction | null = null
  private parameterChangeActionToDelete: ParameterChangeAction | null = null
  private showDeleteDialog: boolean = false

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  private filter: DeviceFilter = {
    selectedActionTypes: [],
    selectedYears: [],
    selectedContacts: []
  }

  // vuex definition for typescript check
  filteredActions!: FilteredActionsGetter
  device!: DevicesState['device']
  deleteDeviceGenericAction!: DeleteDeviceGenericAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
  deleteDeviceSoftwareUpdateAction!: DeleteDeviceSoftwareUpdateAction
  deleteDeviceCalibrationAction!: DeleteDeviceCalibrationAction
  deleteDeviceParameterChangeAction!: DeleteDeviceParameterChangeActionAction
  downloadAttachment!: DownloadAttachmentAction
  loadDeviceGenericActionTypes!: LoadDeviceGenericActionTypesAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

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
    if (this.parameterChangeActionToDelete) {
      return this.parameterChangeActionToDelete
    }
    return null
  }

  get actions () {
    return this.filteredActions(this.filter)
  }

  get isFilterUsed () {
    return this.filter.selectedActionTypes.length > 0 || this.filter.selectedYears.length > 0 || this.filter.selectedContacts.length > 0
  }

  async created () {
    await this.loadDeviceGenericActionTypes()
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true

    this.genericActionToDelete = action
    this.calibrationActionToDelete = null
    this.parameterChangeActionToDelete = null
    this.softwareUpdateActionToDelete = null
  }

  initDeleteDialogSoftwareUpdateAction (action: SoftwareUpdateAction) {
    this.showDeleteDialog = true

    this.softwareUpdateActionToDelete = action
    this.calibrationActionToDelete = null
    this.genericActionToDelete = null
    this.parameterChangeActionToDelete = null
  }

  initDeleteDialogCalibrationAction (action: DeviceCalibrationAction) {
    this.showDeleteDialog = true

    this.calibrationActionToDelete = action
    this.genericActionToDelete = null
    this.parameterChangeActionToDelete = null
    this.softwareUpdateActionToDelete = null
  }

  initDeleteDialogParameterChangeAction (action: ParameterChangeAction) {
    this.showDeleteDialog = true

    this.parameterChangeActionToDelete = action
    this.calibrationActionToDelete = null
    this.genericActionToDelete = null
    this.softwareUpdateActionToDelete = null
  }

  closeDialog () {
    this.showDeleteDialog = false

    this.calibrationActionToDelete = null
    this.genericActionToDelete = null
    this.parameterChangeActionToDelete = null
    this.softwareUpdateActionToDelete = null
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
        case this.calibrationActionToDelete !== null:
          await this.deleteCalibrationAction()
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
      await this.deleteDeviceGenericAction(this.genericActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
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
      await this.deleteDeviceSoftwareUpdateAction(this.softwareUpdateActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Software update action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Software update action could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  async deleteCalibrationAction () {
    if (this.calibrationActionToDelete === null || this.calibrationActionToDelete.id === null) {
      return
    }

    try {
      this.setLoading(true)
      await this.deleteDeviceCalibrationAction(this.calibrationActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Calibration action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Calibration action could not be deleted')
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
      await this.deleteDeviceParameterChangeAction(this.parameterChangeActionToDelete.id)
      this.loadAllDeviceActions(this.deviceId)
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
    return (this.device?.visibility === Visibility.Public) || false
  }
}
</script>
