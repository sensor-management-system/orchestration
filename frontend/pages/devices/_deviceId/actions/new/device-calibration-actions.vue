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
      :current-user-contact-id="userInfo.contactId"
      :used-calibration-parameter-change-actions="usedCalibrationParameterChangeActions"
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
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddDeviceCalibrationAction,
  LoadAllDeviceActionsAction,
  DevicesState, CalibrationRelevantParametersGetter, AddDeviceParameterChangeActionAction
} from '@/store/devices'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'

import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { UsedCalibrationParameterChangeActions, ParameterChangeAction } from '@/models/ParameterChangeAction'

@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    DeviceCalibrationActionForm
  },
  computed: {
    ...mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction', 'deviceMeasuredQuantities']),
    ...mapGetters('devices', ['calibrationRelevantParameters']),
    ...mapState('permissions', ['userInfo'])
  },
  methods: {
    ...mapActions('devices', ['addDeviceCalibrationAction', 'loadAllDeviceActions', 'addDeviceParameterChangeAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewDeviceCalibrationAction extends mixins(CheckEditAccess) {
  private deviceCalibrationAction: DeviceCalibrationAction = new DeviceCalibrationAction()
  private usedCalibrationParameterChangeActions: UsedCalibrationParameterChangeActions[] = []

  // vuex definition for typescript check
  deviceAttachments!: DevicesState['deviceAttachments']
  deviceMeasuredQuantities!: DevicesState['deviceMeasuredQuantities']
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  calibrationRelevantParameters!: CalibrationRelevantParametersGetter
  addDeviceCalibrationAction!: AddDeviceCalibrationAction
  addDeviceParameterChangeAction!: AddDeviceParameterChangeActionAction
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

    this.initalizeCalibrationParameterChangeActions()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initalizeCalibrationParameterChangeActions () {
    for (const parameter of this.calibrationRelevantParameters) {
      const tmp = new ParameterChangeAction()
      tmp.parameter = parameter
      const action = ParameterChangeAction.createFromObject(tmp)
      const obj = {
        is_used: true,
        action
      }
      this.usedCalibrationParameterChangeActions.push(obj)
    }
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

      // save parameter change actions relevant for the calibration
      await this.saveCalibrationRelevantParameterChangeActions()

      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
      this.$store.commit('snackbar/setSuccess', 'New Calibration Action added')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }

  async saveCalibrationRelevantParameterChangeActions () {
    for (const entry of this.usedCalibrationParameterChangeActions) {
      if (entry.is_used === true && entry.action.parameter && entry.action.parameter.id !== null) {
        // We'll take the date and the contact of the associated device calibration action
        entry.action.date = this.deviceCalibrationAction.date
        entry.action.contact = this.deviceCalibrationAction.contact

        await this.addDeviceParameterChangeAction({
          parameterId: entry.action.parameter.id,
          action: entry.action
        })
      }
    }
  }
}

</script>

<style scoped>

</style>
