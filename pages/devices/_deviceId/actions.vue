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
  <NuxtChild/>
<!--  <div>-->
<!--    <ProgressIndicator-->
<!--      v-model="isInProgress"-->
<!--      :dark="isSaving"-->
<!--    />-->
<!--    <v-card-actions>-->
<!--      <v-spacer />-->
<!--      <v-btn-->
<!--        v-if="$auth.loggedIn && isActionsPage"-->
<!--        color="primary"-->
<!--        small-->
<!--        :to="'/devices/' + deviceId + '/actions/new'"-->
<!--      >-->
<!--        Add Action-->
<!--      </v-btn>-->
<!--    </v-card-actions>-->
<!--    <template-->
<!--      v-if="isAddActionPage"-->
<!--    >-->
<!--      <NuxtChild-->
<!--        @input="$fetch"-->
<!--        @showsave="showsave"-->
<!--      />-->
<!--    </template>-->
<!--    <template-->
<!--      v-else-if="isEditActionPage"-->
<!--    >-->
<!--      <NuxtChild-->
<!--        @input="$fetch"-->
<!--        @showload="showload"-->
<!--        @showsave="showsave"-->
<!--      />-->
<!--    </template>-->
<!--    <template v-else>-->
<!--      <hint-card v-if="actions.length === 0">-->
<!--        There are no actions for this device.-->
<!--      </hint-card>-->
<!--      <DeviceActionTimeline-->
<!--        v-else-->
<!--        :value="actions"-->
<!--        :device-id="deviceId"-->
<!--        :action-api-dispatcher="apiDispatcher"-->
<!--        :is-user-authenticated="$auth.loggedIn"-->
<!--        @input="$fetch"-->
<!--        @showdelete="showsave"-->
<!--      />-->
<!--    </template>-->
<!--  </div>-->
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { GenericAction } from '@/models/GenericAction'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/views/devices/actions/DeviceUnmountAction'
import { DeviceMountActionWrapper } from '@/viewmodels/DeviceMountActionWrapper'
import { DeviceUnmountActionWrapper } from '@/viewmodels/DeviceUnmountActionWrapper'

import { DateComparator, isDateCompareable } from '@/modelUtils/Compareables'
import { DeviceActionApiDispatcher } from '@/modelUtils/actionHelpers'

import DeviceActionTimeline from '@/components/actions/DeviceActionTimeline.vue'
import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions } from 'vuex'

const toUtcDate = (dt: DateTime) => {
  return dt.toUTC().toFormat('yyyy-MM-dd TT')
}

@Component({
  // components: {
  //   DeviceActionTimeline,
  //   HintCard,
  //   ProgressIndicator
  // },
  // filters: {
  //   toUtcDate
  // }
  methods:mapActions('devices',['loadAllDeviceActions'])
})
export default class DeviceActionsPage extends Vue {
  async created(){
    await this.loadAllDeviceActions(this.deviceId)
  }
  // async fetchActions () {
  //   this.actions = []
  //   await Promise.all([
  //     this.fetchGenericActions(),
  //     this.fetchSoftwareUpdateActions(),
  //     this.fetchDeviceCalibrationActions(),
  //     this.fetchMountActions(),
  //     this.fetchUnmountActions()
  //   ])
  //
  //   // sort the actions
  //   const comparator = new DateComparator()
  //   this.actions.sort((i: IActionCommonDetails, j: IActionCommonDetails): number => {
  //     if (isDateCompareable(i) && isDateCompareable(j)) {
  //       // multiply result with -1 to get descending order
  //       return comparator.compare(i, j) * -1
  //     }
  //     if (isDateCompareable(i)) {
  //       return -1
  //     }
  //     if (isDateCompareable(j)) {
  //       return 1
  //     }
  //     return 0
  //   })
  // }

  // async fetchGenericActions (): Promise<void> {
  //   const actions: GenericAction[] = await this.$api.devices.findRelatedGenericActions(this.deviceId)
  //   actions.forEach((action: GenericAction) => this.actions.push(action))
  // }
  //
  // async fetchSoftwareUpdateActions (): Promise<void> {
  //   const actions: SoftwareUpdateAction[] = await this.$api.devices.findRelatedSoftwareUpdateActions(this.deviceId)
  //   actions.forEach((action: SoftwareUpdateAction) => this.actions.push(action))
  // }
  //
  // async fetchMountActions (): Promise<void> {
  //   const actions: DeviceMountAction[] = await this.$api.devices.findRelatedMountActions(this.deviceId)
  //   actions.forEach((action: DeviceMountAction) => this.actions.push(new DeviceMountActionWrapper(action)))
  // }
  //
  // async fetchUnmountActions (): Promise<void> {
  //   const actions: DeviceUnmountAction[] = await this.$api.devices.findRelatedUnmountActions(this.deviceId)
  //   actions.forEach((action: DeviceUnmountAction) => this.actions.push(new DeviceUnmountActionWrapper(action)))
  // }
  //
  // async fetchDeviceCalibrationActions (): Promise<void> {
  //   const actions: DeviceCalibrationAction[] = await this.$api.devices.findRelatedCalibrationActions(this.deviceId)
  //   actions.forEach((action: DeviceCalibrationAction) => this.actions.push(action))
  // }

  head () {
    return {
      titleTemplate: 'Actions - %s'
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  // get isInProgress (): boolean {
  //   return this.isLoading || this.isSaving
  // }
  //
  // get isActionsPage (): boolean {
  //   return !this.isEditActionPage && !this.isAddActionPage
  // }
  //
  // get isAddActionPage (): boolean {
  //   // eslint-disable-next-line no-useless-escape
  //   const addUrl = '^\/devices\/' + this.deviceId + '\/actions\/new$'
  //   return !!this.$route.path.match(addUrl)
  // }
  //
  // get isEditActionPage (): boolean {
  //   // eslint-disable-next-line no-useless-escape
  //   const editUrl = '^\/devices\/' + this.deviceId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
  //   return !!this.$route.path.match(editUrl)
  // }
  //
  // showsave (isSaving: boolean) {
  //   this.isSaving = isSaving
  // }
  //
  // showload (isLoading: boolean) {
  //   this.isLoading = isLoading
  // }
  //
  // get apiDispatcher () {
  //   return new DeviceActionApiDispatcher(this.$api)
  // }
}
</script>
