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
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <DeviceCalibrationActionForm
      ref="deviceCalibrationActionForm"
      v-model="deviceCalibrationAction"
      :attachments="deviceAttachments"
      :measured-quantities="deviceMeasuredQuantities"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
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
  AddDeviceCalibrationAction,
  LoadAllDeviceActionsAction,
  DevicesState
} from '@/store/devices'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    DeviceCalibrationActionForm
  },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction', 'deviceMeasuredQuantities']),
  methods: {
    ...mapActions('devices', ['addDeviceCalibrationAction', 'loadAllDeviceActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewDeviceCalibrationAction extends mixins(CheckEditAccess) {
  private deviceCalibrationAction: DeviceCalibrationAction = new DeviceCalibrationAction()

  // vuex definition for typescript check
  deviceAttachments!: DevicesState['deviceAttachments']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  addDeviceCalibrationAction!: AddDeviceCalibrationAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
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

  created () {
    if (this.chosenKindOfDeviceAction === null) {
      this.$router.push('/devices/' + this.deviceId + '/actions')
      return
    }
    if (this.deviceMeasuredQuantities.length === 1) {
      // In case we have only that we could select, we take that as default.
      this.deviceCalibrationAction.measuredQuantities = [...this.deviceMeasuredQuantities]
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.setLoading(true)
      await this.addDeviceCalibrationAction({
        deviceId: this.deviceId,
        calibrationAction: this.deviceCalibrationAction
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
      this.$store.commit('snackbar/setSuccess', 'New Calibration Action added')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
