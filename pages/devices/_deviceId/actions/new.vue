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
  <div
    v-if="isLoggedIn"
  >
    <v-card
      flat
    >
      <!-- button-tray -->
      <v-card-actions>
        <v-spacer />
        <ActionButtonTray
          :cancel-url="'/devices/' + deviceId + '/actions'"
          :is-saving="isSaving"
          :show-apply="showApplyButton"
          @apply="onApplyButtonClick"
        />
      </v-card-actions>
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="actionTypeItems"
          :item-text="(x) => x.name"
          :item-value="(x) => x"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
        />
      </v-card-text>
      <!-- deviceCalibration -->
      <v-card-text
        v-if="deviceCalibrationChosen"
      >
        <DeviceCalibrationActionForm
          ref="deviceCalibrationActionForm"
          v-model="deviceCalibrationAction"
          :attachments="attachments"
          :measured-quantities="measuredQuantities"
        />
      </v-card-text>

      <!-- softwareUpdate -->
      <v-card-text
        v-if="softwareUpdateChosen"
      >
        <SoftwareUpdateActionForm
          ref="softwareUpdateActionForm"
          v-model="softwareUpdateAction"
          :attachments="attachments"
        />
      </v-card-text>

      <!-- genericAction -->
      <v-card-text
        v-if="genericActionChosen"
      >
        <GenericActionForm
          ref="genericDeviceActionForm"
          v-model="genericDeviceAction"
          :attachments="attachments"
        />
      </v-card-text>

      <!-- button-tray -->
      <v-card-actions
        v-if="chosenKindOfAction"
      >
        <v-spacer />
        <ActionButtonTray
          :cancel-url="'/devices/' + deviceId + '/actions'"
          :is-saving="isSaving"
          :show-apply="showApplyButton"
          @apply="onApplyButtonClick"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { IActionType, ActionType } from '@/models/ActionType'

import { ACTION_TYPE_API_FILTER_DEVICE } from '@/services/cv/ActionTypeApi'

import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'

const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType = typeof KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION | typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE | typeof KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION | typeof KIND_OF_ACTION_TYPE_UNKNOWN

type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

@Component({
  components: {
    DeviceCalibrationActionForm,
    GenericActionForm,
    SoftwareUpdateActionForm,
    ActionButtonTray
  }
})
export default class ActionAddPage extends Vue {
  private specialActionTypes: IOptionsForActionType[] = [
    {
      id: 'device_calibration',
      name: 'Device Calibration',
      uri: '',
      kind: KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
    },
    {
      id: 'software_update',
      name: 'Software Update',
      uri: '',
      kind: KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
    }
  ]

  private genericActionTypes: ActionType[] = []
  private attachments: Attachment[] = []
  private measuredQuantities: DeviceProperty[] = []

  private _chosenKindOfAction: IOptionsForActionType | null = null

  private deviceCalibrationAction: DeviceCalibrationAction = new DeviceCalibrationAction()
  private genericDeviceAction: GenericAction = new GenericAction()
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()

  private _isSaving: boolean = false

  async fetch () {
    await Promise.all([
      this.fetchGenericActionTypes()
    ])
  }

  async fetchGenericActionTypes (): Promise<any> {
    this.genericActionTypes = await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_DEVICE).build().findMatchingAsList()
  }

  mounted () {
    this.$api.devices.findRelatedDeviceAttachments(this.deviceId).then((foundAttachments) => {
      this.attachments = foundAttachments
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    })
    this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundMeasuredQuantities) => {
      this.measuredQuantities = foundMeasuredQuantities
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
    })
  }

  get chosenKindOfAction () {
    return this.$data._chosenKindOfAction
  }

  set chosenKindOfAction (newValue: IOptionsForActionType | null) {
    if (this.$data._chosenKindOfAction !== newValue) {
      this.$data._chosenKindOfAction = newValue

      if (this.genericActionChosen) {
        this.genericDeviceAction = new GenericAction()
        this.genericDeviceAction.actionTypeName = newValue?.name || ''
        this.genericDeviceAction.actionTypeUrl = newValue?.uri || ''
      }
      if (this.softwareUpdateChosen) {
        this.softwareUpdateAction = new SoftwareUpdateAction()
      }
      if (this.deviceCalibrationChosen) {
        this.deviceCalibrationAction = new DeviceCalibrationAction()
      }
    }
  }

  get deviceCalibrationChosen () {
    return this.$data._chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  }

  get softwareUpdateChosen () {
    return this.$data._chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get genericActionChosen () {
    return this.$data._chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isSaving (): boolean {
    return this.$data._isSaving
  }

  set isSaving (value: boolean) {
    this.$data._isSaving = value
    this.$emit('showsave', value)
  }

  onApplyButtonClick () {
    switch (true) {
      case this.genericActionChosen:
        this.addGenericAction()
        return
      case this.softwareUpdateChosen:
        this.addSoftwareUpdateAction()
        return
      case this.deviceCalibrationChosen:
        this.addDeviceCalibrationAction()
    }
  }

  addDeviceCalibrationAction () {
    if (!this.isLoggedIn) {
      return
    }
    if (!this.deviceCalibrationAction) {
      return
    }
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.isSaving = true
    this.$api.deviceCalibrationActions.add(this.deviceId, this.deviceCalibrationAction).then((action: DeviceCalibrationAction) => {
      this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }

  addSoftwareUpdateAction () {
    if (!this.isLoggedIn) {
      return
    }
    if (!this.softwareUpdateAction) {
      return
    }
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.deviceSoftwareUpdateActions.add(this.deviceId, this.softwareUpdateAction).then((action: SoftwareUpdateAction) => {
      this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }

  addGenericAction () {
    if (!this.isLoggedIn) {
      return
    }
    if (!this.genericDeviceAction) {
      return
    }
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.genericDeviceActions.add(this.deviceId, this.genericDeviceAction).then((action: GenericAction) => {
      this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }

  get showApplyButton (): boolean {
    return this.chosenKindOfAction !== null
  }

  get actionTypeItems (): IOptionsForActionType[] {
    return [
      ...this.specialActionTypes,
      ...this.genericActionTypes.map((i) => {
        return {
          id: i.id,
          name: i.name,
          uri: i.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase())) as IOptionsForActionType[]
  }
}

</script>
