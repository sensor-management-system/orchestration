<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="deviceActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        >
          <template #append-outer>
            <v-btn icon @click="showNewActionTypeDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
        </v-select>
      </v-card-text>
    </v-card>
    <v-card-actions v-if="!chosenKindOfAction">
      <v-spacer />
      <v-btn
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/actions'"
      >
        cancel
      </v-btn>
    </v-card-actions>
    <NuxtChild />
    <action-type-dialog
      v-model="showNewActionTypeDialog"
      :initial-action-type-api-filter-type="selectedActionCategory"
      @aftersubmit="setChosenKindOfDeviceActionAndUpdateRoute"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import ActionTypeDialog from '@/components/shared/ActionTypeDialog.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { ActionType } from '@/models/ActionType'

import {
  LoadDeviceAttachmentsAction,
  SetChosenKindOfDeviceActionAction,
  LoadDeviceMeasuredQuantitiesAction,
  LoadDeviceParametersAction,
  DevicesState, SetDevicePresetParameterAction
} from '@/store/devices'

import { DeviceActionTypeItemsGetter, LoadDeviceGenericActionTypesAction } from '@/store/vocabulary'

import { ACTION_TYPE_API_FILTER_DEVICE } from '@/services/cv/ActionTypeApi'
import {
  KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION,
  KIND_OF_ACTION_TYPE_GENERIC_ACTION,
  KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION,
  KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
} from '@/models/ActionKind'

@Component({
  components: { ActionTypeDialog },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['deviceActionTypeItems']),
    ...mapState('devices', ['chosenKindOfDeviceAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadDeviceGenericActionTypes']),
    ...mapActions('devices', ['loadDeviceAttachments', 'setChosenKindOfDeviceAction', 'loadDeviceMeasuredQuantities', 'loadDeviceParameters', 'setDevicePresetParameter']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ActionAddPage extends mixins(CheckEditAccess) {
  private showNewActionTypeDialog = false

  // vuex definition for typescript check
  deviceActionTypeItems!: DeviceActionTypeItemsGetter
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  loadDeviceGenericActionTypes!: LoadDeviceGenericActionTypesAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  loadDeviceParameters!: LoadDeviceParametersAction
  setChosenKindOfDeviceAction!: SetChosenKindOfDeviceActionAction
  setLoading!: SetLoadingAction
  setDevicePresetParameter!: SetDevicePresetParameterAction

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

  get isBasePath (): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/actions/new'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      if (this.isBasePath) {
        this.chosenKindOfAction = null
        this.setDevicePresetParameter(null)
      }
      await Promise.all([
        this.loadDeviceGenericActionTypes(),
        this.loadDeviceAttachments(this.deviceId),
        this.loadDeviceMeasuredQuantities(this.deviceId),
        this.loadDeviceParameters(this.deviceId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action resources')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get chosenKindOfAction () {
    return this.chosenKindOfDeviceAction
  }

  set chosenKindOfAction (newVal) {
    this.setChosenKindOfDeviceAction(newVal)
  }

  setChosenKindOfDeviceActionAndUpdateRoute (newVal: ActionType) {
    this.setChosenKindOfDeviceAction({
      kind: KIND_OF_ACTION_TYPE_GENERIC_ACTION,
      id: newVal.id,
      name: newVal.name,
      uri: newVal.uri
    })
    this.updateRoute()
  }

  get selectedActionCategory (): string {
    return ACTION_TYPE_API_FILTER_DEVICE
  }

  get deviceCalibrationChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get genericActionChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION
  }

  get parameterChangeActionChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
  }

  updateRoute () {
    if (this.genericActionChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/generic-device-actions`)
      return
    }
    if (this.softwareUpdateChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/software-update-actions`)
      return
    }
    if (this.deviceCalibrationChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/device-calibration-actions`)
      return
    }
    if (this.parameterChangeActionChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/parameter-change-actions`)
      return
    }
    if (!this.chosenKindOfAction) {
      this.$router.push(`/devices/${this.deviceId}/actions/new`)
    }
  }
}

</script>
