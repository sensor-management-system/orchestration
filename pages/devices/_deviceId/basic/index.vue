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
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu>
        <template #actions>
          <DotMenuActionSensorML
            @click="openSensorML"
          />
          <DotMenuActionCopy
            v-if="$auth.loggedIn"
            :path="'/devices/copy/' + deviceId"
          />
          <DotMenuActionArchive
            :readonly="!archivable"
            @click="initArchiveDialog"
          />
          <DotMenuActionRestore
            :readonly="!restoreable"
            @click="runRestore"
          />
          <DotMenuActionDelete
            v-if="$auth.loggedIn"
            :readonly="!deletable"
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <DeviceBasicData
      v-if="device"
      v-model="device"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu>
        <template #actions>
          <DotMenuActionSensorML
            @click="openSensorML"
          />
          <DotMenuActionCopy
            v-if="$auth.loggedIn"
            :path="'/devices/copy/' + deviceId"
          />
          <DotMenuActionArchive
            :readonly="!archivable"
            @click="initArchiveDialog"
          />
          <DotMenuActionRestore
            :readonly="!restoreable"
            @click="runRestore"
          />
          <DotMenuActionDelete
            v-if="$auth.loggedIn"
            :readonly="!deletable"
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <DeviceDeleteDialog
      v-if="device"
      v-model="showDeleteDialog"
      :device-to-delete="device"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <DeviceArchiveDialog
      v-if="device"
      v-model="showArchiveDialog"
      :device-to-archive="device"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { ArchiveDeviceAction, DeleteDeviceAction, DevicesState, LoadDeviceAction, RestoreDeviceAction, ExportAsSensorMLAction, GetSensorMLUrlAction } from '@/store/devices'

import DeviceDeleteDialog from '@/components/devices/DeviceDeleteDialog.vue'
import DeviceArchiveDialog from '@/components/devices/DeviceArchiveDialog.vue'
import DeviceBasicData from '@/components/DeviceBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Visibility } from '@/models/Visibility'

@Component({
  components: {
    ProgressIndicator,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenuActionSensorML,
    DotMenu,
    DeviceDeleteDialog,
    DeviceBasicData,
    DotMenuActionRestore,
    DotMenuActionArchive,
    DeviceArchiveDialog
  },
  computed: mapState('devices', ['device']),
  methods: mapActions('devices', ['loadDevice', 'deleteDevice', 'archiveDevice', 'restoreDevice', 'exportAsSensorML', 'getSensorMLUrl'])
})
export default class DeviceShowBasicPage extends Vue {
  @InjectReactive()
    editable!: boolean

  @InjectReactive()
    deletable!: boolean

  @InjectReactive()
    archivable!: boolean

  @InjectReactive()
    restoreable!: boolean

  private isSaving = false

  private showDeleteDialog: boolean = false
  private showArchiveDialog: boolean = false

  // vuex definition for typescript check
  device!: DevicesState['device']
  loadDevice!: LoadDeviceAction
  deleteDevice!: DeleteDeviceAction
  archiveDevice!: ArchiveDeviceAction
  restoreDevice!: RestoreDeviceAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction

  get deviceId () {
    return this.$route.params.deviceId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async openSensorML () {
    if (this.device?.visibility === Visibility.Public) {
      const url = await this.getSensorMLUrl(this.deviceId)
      window.open(url)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.deviceId)
        const url = window.URL.createObjectURL(blob)
        window.open(url)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Device could not be exported as SensorML')
      }
    }
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.device === null || this.device.id === null) {
      return
    }
    try {
      this.isSaving = true
      await this.deleteDevice(this.device.id)
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
      this.$router.push('/devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    } finally {
      this.isSaving = false
    }
  }

  initArchiveDialog () {
    this.showArchiveDialog = true
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
  }

  async archiveAndCloseDialog () {
    this.showArchiveDialog = false
    if (this.device === null || this.device.id === null) {
      return
    }
    try {
      this.isSaving = true
      await this.archiveDevice(this.device.id)
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.$store.commit('snackbar/setSuccess', 'Device archived')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Device could not be archived')
    } finally {
      this.isSaving = false
      this.showArchiveDialog = false
    }
  }

  async runRestore () {
    if (this.device === null || this.device.id === null) {
      return
    }
    this.isSaving = true
    try {
      await this.restoreDevice(this.device.id)
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.$store.commit('snackbar/setSuccess', 'Device restored')
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Device could not be restored')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
