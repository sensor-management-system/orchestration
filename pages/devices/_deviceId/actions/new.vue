<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
      v-model="isLoading"
    />
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="deviceActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action Type"
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
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import CheckEditAccess from '@/mixins/CheckEditAccess'
import { ActionType } from '@/models/ActionType'

import {
  LoadDeviceAttachmentsAction,
  SetChosenKindOfDeviceActionAction,
  LoadDeviceMeasuredQuantitiesAction,
  DevicesState
} from '@/store/devices'

import {
  DeviceActionTypeItemsGetter,
  LoadDeviceGenericActionTypesAction
} from '@/store/vocabulary'

import { ACTION_TYPE_API_FILTER_DEVICE } from '@/services/cv/ActionTypeApi'

const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'

@Component({
  components: { ActionTypeDialog, ProgressIndicator },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['deviceActionTypeItems']),
    ...mapState('devices', ['chosenKindOfDeviceAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadDeviceGenericActionTypes']),
    ...mapActions('devices', ['loadDeviceAttachments', 'setChosenKindOfDeviceAction', 'loadDeviceMeasuredQuantities'])
  }
})
export default class ActionAddPage extends mixins(CheckEditAccess) {
  private isLoading: boolean = false
  private showNewActionTypeDialog = false

  // vuex definition for typescript check
  deviceActionTypeItems!: DeviceActionTypeItemsGetter
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  loadDeviceGenericActionTypes!: LoadDeviceGenericActionTypesAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  setChosenKindOfDeviceAction!: SetChosenKindOfDeviceActionAction

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

  async created () {
    try {
      this.isLoading = true
      this.chosenKindOfAction = null
      await Promise.all([
        this.loadDeviceGenericActionTypes(),
        this.loadDeviceAttachments(this.deviceId),
        this.loadDeviceMeasuredQuantities(this.deviceId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    } finally {
      this.isLoading = false
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
      kind: KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION,
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
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
  }

  updateRoute () {
    if (this.genericActionChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/generic-device-actions`)
    }
    if (this.softwareUpdateChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/software-update-actions`)
    }
    if (this.deviceCalibrationChosen) {
      this.$router.push(`/devices/${this.deviceId}/actions/new/device-calibration-actions`)
    }
    if (!this.chosenKindOfAction) {
      this.$router.push(`/devices/${this.deviceId}/actions/new`)
    }
  }
}

</script>
