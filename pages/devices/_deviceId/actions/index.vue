<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
        v-if="$auth.loggedIn"
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
        >
          <template #actions>
            <v-btn
              v-if="$auth.loggedIn"
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
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialogGenericAction(action)"
            />
          </template>
        </GenericActionCard>
      </template>
      <template #software-update-action="{action}">
        <SoftwareUpdateActionCard
          :value="action"
          target="Device"
        >
          <template #actions>
            <v-btn
              v-if="$auth.loggedIn"
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
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialogSoftwareUpdateAction(action)"
            />
          </template>
        </SoftwareUpdateActionCard>
      </template>
      <template #calibration-action="{action}">
        <DeviceCalibrationActionCard
          :value="action"
        >
          <template #actions>
            <v-btn
              v-if="$auth.loggedIn"
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
              :readonly="!$auth.loggedIn"
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

import { mapActions, mapGetters } from 'vuex'
import HintCard from '@/components/HintCard.vue'
import DeviceActionTimeline from '@/components/actions/DeviceActionTimeline.vue'
import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeviceMountActionCard from '@/components/actions/DeviceMountActionCard.vue'
import DeviceUnmountActionCard from '@/components/actions/DeviceUnmountActionCard.vue'
import DeviceCalibrationActionCard from '@/components/actions/DeviceCalibrationActionCard.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'

import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'

@Component({
  components: {
    SoftwareUpdateActionCard,
    ProgressIndicator,
    ActionDeleteDialog,
    DeviceCalibrationActionCard,
    DeviceUnmountActionCard,
    DeviceMountActionCard,
    DotMenuActionDelete,
    GenericActionCard,
    DeviceActionTimeline,
    HintCard
  },
  computed: mapGetters('devices', ['actions']),
  methods: mapActions('devices', ['deleteDeviceSoftwareUpdateAction', 'deleteDeviceGenericAction', 'deleteDeviceCalibrationAction', 'loadAllDeviceActions'])
})
export default class DeviceActionsShowPage extends Vue {
  private isSaving: boolean = false
  private genericActionToDelete: GenericAction | null = null
  private softwareUpdateActionToDelete: SoftwareUpdateAction | null = null
  private calibrationActionToDelete: DeviceCalibrationAction | null = null
  private showDeleteDialog: boolean = false

  // vuex definition for typescript check
  deleteDeviceGenericAction!:(genericDeviceActionId: string)=>Promise<void>
  loadAllDeviceActions!:(id:string)=>void
  deleteDeviceSoftwareUpdateAction!:(softwareUpdateActionId: string)=>Promise<void>
  deleteDeviceCalibrationAction!:(calibrationDeviceActionId: string)=>Promise<void>

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
    if(this.genericActionToDelete === null || this.genericActionToDelete.id ===null){
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
    if(this.softwareUpdateActionToDelete === null || this.softwareUpdateActionToDelete.id ===null){
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
    if(this.calibrationActionToDelete === null || this.calibrationActionToDelete.id ===null){
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
}
</script>

<style scoped>

</style>
