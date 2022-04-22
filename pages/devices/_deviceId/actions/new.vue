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
    <v-card
      flat
    >
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
          return-object
          @change="updateRoute"
        />
      </v-card-text>
    </v-card>
    <NuxtChild/>
  </div>

<!--  <div>-->
<!--    <v-card-->
<!--      flat-->
<!--    >-->
<!--      &lt;!&ndash; button-tray &ndash;&gt;-->
<!--      <v-card-actions>-->
<!--        <v-spacer />-->
<!--        <ActionButtonTray-->
<!--          :cancel-url="'/devices/' + deviceId + '/actions'"-->
<!--          :is-saving="isSaving"-->
<!--          :show-apply="showApplyButton"-->
<!--          @apply="onApplyButtonClick"-->
<!--        />-->
<!--      </v-card-actions>-->
<!--      <v-card-text>-->
<!--        <v-select-->
<!--          v-model="chosenKindOfAction"-->
<!--          :items="actionTypeItems"-->
<!--          :item-text="(x) => x.name"-->
<!--          :item-value="(x) => x"-->
<!--          clearable-->
<!--          label="Action Type"-->
<!--          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"-->
<!--          persistent-hint-->
<!--        />-->
<!--      </v-card-text>-->
<!--      &lt;!&ndash; deviceCalibration &ndash;&gt;-->
<!--      <v-card-text-->
<!--        v-if="deviceCalibrationChosen"-->
<!--      >-->
<!--        <DeviceCalibrationActionForm-->
<!--          ref="deviceCalibrationActionForm"-->
<!--          v-model="deviceCalibrationAction"-->
<!--          :attachments="attachments"-->
<!--          :measured-quantities="measuredQuantities"-->
<!--          :current-user-mail="$auth.user.email"-->
<!--        />-->
<!--      </v-card-text>-->

<!--      &lt;!&ndash; softwareUpdate &ndash;&gt;-->
<!--      <v-card-text-->
<!--        v-if="softwareUpdateChosen"-->
<!--      >-->
<!--        <SoftwareUpdateActionForm-->
<!--          ref="softwareUpdateActionForm"-->
<!--          v-model="softwareUpdateAction"-->
<!--          :attachments="attachments"-->
<!--          :current-user-mail="$auth.user.email"-->
<!--        />-->
<!--      </v-card-text>-->

<!--      &lt;!&ndash; genericAction &ndash;&gt;-->
<!--      <v-card-text-->
<!--        v-if="genericActionChosen"-->
<!--      >-->
<!--        <GenericActionForm-->
<!--          ref="genericDeviceActionForm"-->
<!--          v-model="genericDeviceAction"-->
<!--          :attachments="attachments"-->
<!--          :current-user-mail="$auth.user.email"-->
<!--        />-->
<!--      </v-card-text>-->

<!--      &lt;!&ndash; button-tray &ndash;&gt;-->
<!--      <v-card-actions-->
<!--        v-if="chosenKindOfAction"-->
<!--      >-->
<!--        <v-spacer />-->
<!--        <ActionButtonTray-->
<!--          :cancel-url="'/devices/' + deviceId + '/actions'"-->
<!--          :is-saving="isSaving"-->
<!--          :show-apply="showApplyButton"-->
<!--          @apply="onApplyButtonClick"-->
<!--        />-->
<!--      </v-card-actions>-->
<!--    </v-card>-->
<!--  </div>-->
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
import { mapActions, mapState } from 'vuex'

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
  },
  middleware: ['auth'],
  computed:{
    ...mapState('vocabulary',['deviceGenericActionTypes']),
    ...mapState('devices',['chosenKindOfDeviceAction'])
  },
  methods:{
    ...mapActions('vocabulary',['loadDeviceGenericActionTypes']),
    ...mapActions('devices',['loadDeviceAttachments','setChosenKindOfDeviceAction'])
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

  async created(){
    try {
      await this.loadDeviceGenericActionTypes()
      await this.loadDeviceAttachments(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    }
    // this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundMeasuredQuantities) => { // todo einbauen in store
    //   this.measuredQuantities = foundMeasuredQuantities
    // }).catch((_error) => {
    //   this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
    // })
  }

  get chosenKindOfAction(){
    return this.chosenKindOfDeviceAction
  }

  set chosenKindOfAction(newVal){
    this.setChosenKindOfDeviceAction(newVal)
  }


  updateRoute(){
    console.log('here');
    if(this.genericActionChosen){
      this.$router.push(`/devices/${this.deviceId}/actions/new/generic-platform-actions`)
    }
    if(this.softwareUpdateChosen){
      this.$router.push(`/devices/${this.deviceId}/actions/new/software-update-actions`)
    }
    if(this.deviceCalibrationChosen){
      this.$router.push(`/devices/${this.deviceId}/actions/new/device-calibration-actions`)
    }
    if(!this.chosenKindOfAction){
      this.$router.push(`/devices/${this.deviceId}/actions/new`)
    }
  }

  // async fetch () {
  //   await Promise.all([
  //     this.fetchGenericActionTypes()
  //   ])
  // }
  //
  // async fetchGenericActionTypes (): Promise<any> {
  //   this.genericActionTypes = await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_DEVICE).build().findMatchingAsList()
  // }
  //
  // mounted () {
  //   this.$api.devices.findRelatedDeviceAttachments(this.deviceId).then((foundAttachments) => {
  //     this.attachments = foundAttachments
  //   }).catch((_error) => {
  //     this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
  //   })
  //   this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundMeasuredQuantities) => {
  //     this.measuredQuantities = foundMeasuredQuantities
  //   }).catch((_error) => {
  //     this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
  //   })
  // }

  get deviceCalibrationChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get genericActionChosen () {
    return this.chosenKindOfDeviceAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  // addDeviceCalibrationAction () {
  //   if (!this.$auth.loggedIn) {
  //     return
  //   }
  //   if (!this.deviceCalibrationAction) {
  //     return
  //   }
  //   if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
  //     this.isSaving = false
  //     this.$store.commit('snackbar/setError', 'Please correct the errors')
  //     return
  //   }
  //
  //   this.isSaving = true
  //   this.$api.deviceCalibrationActions.add(this.deviceId, this.deviceCalibrationAction).then((action: DeviceCalibrationAction) => {
  //     this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
  //   }).catch(() => {
  //     this.$store.commit('snackbar/setError', 'Failed to save the action')
  //   }).finally(() => {
  //     this.isSaving = false
  //   })
  // }

  // addSoftwareUpdateAction () {
  //   if (!this.$auth.loggedIn) {
  //     return
  //   }
  //   if (!this.softwareUpdateAction) {
  //     return
  //   }
  //   if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
  //     this.isSaving = false
  //     this.$store.commit('snackbar/setError', 'Please correct the errors')
  //     return
  //   }
  //   this.isSaving = true
  //   this.$api.deviceSoftwareUpdateActions.add(this.deviceId, this.softwareUpdateAction).then((action: SoftwareUpdateAction) => {
  //     this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
  //   }).catch(() => {
  //     this.$store.commit('snackbar/setError', 'Failed to save the action')
  //   }).finally(() => {
  //     this.isSaving = false
  //   })
  // }

  // addGenericAction () {
  //   if (!this.$auth.loggedIn) {
  //     return
  //   }
  //   if (!this.genericDeviceAction) {
  //     return
  //   }
  //   if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
  //     this.isSaving = false
  //     this.$store.commit('snackbar/setError', 'Please correct the errors')
  //     return
  //   }
  //   this.isSaving = true
  //   this.$api.genericDeviceActions.add(this.deviceId, this.genericDeviceAction).then((action: GenericAction) => {
  //     this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
  //   }).catch(() => {
  //     this.$store.commit('snackbar/setError', 'Failed to save the action')
  //   }).finally(() => {
  //     this.isSaving = false
  //   })
  // }

  get actionTypeItems (): IOptionsForActionType[] {
    return [
      ...this.specialActionTypes,
      ...this.deviceGenericActionTypes.map((i) => {
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
