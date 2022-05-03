<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-select
      value="Device Calibration"
      :items="['Device Calibration']"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <DeviceCalibrationActionForm
      ref="deviceCalibrationActionForm"
      v-model="action"
      :attachments="deviceAttachments"
      :measured-quantities="deviceMeasuredQuantities"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

@Component({
  components: {
    ProgressIndicator,
    SaveAndCancelButtons,
    DeviceCalibrationActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('devices', ['deviceCalibrationAction', 'deviceAttachments', 'deviceMeasuredQuantities']),
  methods: mapActions('devices', ['loadDeviceCalibrationAction', 'loadAllDeviceActions', 'loadDeviceAttachments', 'loadDeviceMeasuredQuantities', 'updateDeviceCalibrationAction'])
})
export default class DeviceCalibrationActionEditPage extends Vue {
  private action: DeviceCalibrationAction = new DeviceCalibrationAction()
  private isSaving = false
  private isLoading = false

  // vuex definition for typescript check
  loadDeviceCalibrationAction!: (id:string)=>void
  loadDeviceAttachments!: (id:string)=>void
  loadDeviceMeasuredQuantities!:(id:string)=>void
  deviceCalibrationAction!:DeviceCalibrationAction
  updateDeviceCalibrationAction!:({
    deviceId,
    calibrationDeviceAction
  }: { deviceId: string, calibrationDeviceAction: DeviceCalibrationAction })=>Promise<DeviceCalibrationAction>
  loadAllDeviceActions!:(id:string)=>void

  async created () {
    try {
      this.isLoading = true
      await this.loadDeviceCalibrationAction(this.actionId)
      await this.loadDeviceAttachments(this.deviceId)
      await this.loadDeviceMeasuredQuantities(this.deviceId)
      this.action = DeviceCalibrationAction.createFromObject(this.deviceCalibrationAction)
    } catch {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.isLoading = false
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isLoading = true
      await this.updateDeviceCalibrationAction({
        deviceId: this.deviceId,
        calibrationDeviceAction: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isLoading = false
    }
  }
}
</script>
