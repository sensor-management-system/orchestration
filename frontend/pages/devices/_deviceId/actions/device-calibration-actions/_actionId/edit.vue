<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
        v-if="editable"
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
        v-if="editable"
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  LoadDeviceCalibrationActionAction,
  LoadAllDeviceActionsAction,
  LoadDeviceAttachmentsAction,
  LoadDeviceMeasuredQuantitiesAction,
  UpdateDeviceCalibrationAction,
  DevicesState
} from '@/store/devices'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceCalibrationActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceCalibrationAction', 'deviceAttachments', 'deviceMeasuredQuantities']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceCalibrationAction', 'loadAllDeviceActions', 'loadDeviceAttachments', 'loadDeviceMeasuredQuantities', 'updateDeviceCalibrationAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceCalibrationActionEditPage extends mixins(CheckEditAccess) {
  private action: DeviceCalibrationAction = new DeviceCalibrationAction()

  // vuex definition for typescript check
  deviceCalibrationAction!: DevicesState['deviceCalibrationAction']
  deviceAttachments!: DevicesState['deviceAttachments']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  loadDeviceCalibrationAction!: LoadDeviceCalibrationActionAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  updateDeviceCalibrationAction!: UpdateDeviceCalibrationAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/actions'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDeviceCalibrationAction(this.actionId),
        this.loadDeviceAttachments(this.deviceId),
        this.loadDeviceMeasuredQuantities(this.deviceId)
      ])
      if (this.deviceCalibrationAction) {
        this.action = DeviceCalibrationAction.createFromObject(this.deviceCalibrationAction)
      }
    } catch {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  async save () {
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.setLoading(true)
      await this.updateDeviceCalibrationAction({
        deviceId: this.deviceId,
        calibrationAction: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
