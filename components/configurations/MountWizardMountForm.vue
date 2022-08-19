<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <v-card v-for="(device, i) in selectedDevices" :key="`device-${i}`" class="mb-6">
      <v-card-title>Mounting info for {{ device.shortName }}</v-card-title>
      <v-card-subtitle>{{ dateRangeString }}</v-card-subtitle>
      <ConfigurationsPlatformDeviceMountForm
        :entity="device"
        :readonly="false"
        :contacts="contacts"
        :current-user-mail="currentUserMail"
        :with-unmount="selectedEndDate !== null"
        @add="setDeviceToMount(device, $event)"
      />
    </v-card>
    <v-card v-for="(platform, i) in selectedPlatforms" :key="`platform-${i}`" class="mb-6">
      <v-card-title>Mounting info for {{ platform.shortName }}</v-card-title>
      <v-card-subtitle>{{ dateRangeString }}</v-card-subtitle>
      <ConfigurationsPlatformDeviceMountForm
        :entity="platform"
        :readonly="false"
        :contacts="contacts"
        :current-user-mail="currentUserMail"
        :with-unmount="selectedEndDate !== null"
        @add="setPlatformToMount(platform, $event)"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, PropSync, InjectReactive } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import { DateTime } from 'luxon'

import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

import ConfigurationsPlatformDeviceMountForm from '@/components/ConfigurationsPlatformDeviceMountForm.vue'

@Component({
  components: {
    ConfigurationsPlatformDeviceMountForm
  },
  filters: { dateToDateTimeStringHHMM },
  computed: {
    ...mapState('contacts', ['contacts'])
  }
})
export default class MountWizardMountForm extends Vue {
  @PropSync('selectedDevices', {
    required: false,
    type: Array
  })
    syncedSelectedDevices!: Device[]

  @PropSync('selectedPlatforms', {
    required: false,
    type: Array
  })
    syncedSelectedPlatforms!: Platform[]

  @PropSync('devicesToMount', {
    required: false,
    type: Array
  })
    syncedDevicesToMount!: { entity: Device, mountInfo: DeviceMountAction }[]

  @PropSync('platformsToMount', {
    required: false,
    type: Array
  })
    syncedPlatformsToMount!: { entity: Platform, mountInfo: PlatformMountAction }[]

  @InjectReactive() selectedDate!: DateTime
  @InjectReactive() selectedEndDate!: DateTime | null

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  get dateRangeString (): string {
    const start = `From ${dateToDateTimeStringHHMM(this.selectedDate)}`
    const end = (this.selectedEndDate === null) ? ' with open end' : ` until ${dateToDateTimeStringHHMM(this.selectedEndDate)}`
    return start + end
  }

  setPlatformToMount (platform: Platform, mountInfo: PlatformMountAction) {
    mountInfo.beginDate = this.selectedDate
    mountInfo.endDate = this.selectedEndDate
    const platformToMount = {
      entity: platform,
      mountInfo
    }

    const mountIndex = this.syncedPlatformsToMount.findIndex(platformMount => platformMount.entity.id === platform.id)

    if (mountIndex < 0) {
      this.syncedPlatformsToMount.push(platformToMount)
    } else {
      this.syncedPlatformsToMount[mountIndex].mountInfo = mountInfo
    }
  }

  setDeviceToMount (device: Device, mountInfo: DeviceMountAction) {
    mountInfo.beginDate = this.selectedDate
    mountInfo.endDate = this.selectedEndDate
    const deviceToMount = {
      entity: device,
      mountInfo
    }

    const mountIndex = this.syncedDevicesToMount.findIndex(deviceMount => deviceMount.entity.id === device.id)

    if (mountIndex < 0) {
      this.syncedDevicesToMount.push(deviceToMount)
    } else {
      this.syncedDevicesToMount[mountIndex].mountInfo = mountInfo
    }
  }
}
</script>

<style scoped>

</style>
