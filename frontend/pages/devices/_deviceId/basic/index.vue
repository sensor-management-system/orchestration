<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
            @click="openSensorMLDialog"
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
            @click="openSensorMLDialog"
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
    <DeleteDialog
      v-if="device"
      v-model="showDeleteDialog"
      title="Delete Device"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the device <em>{{ device.shortName }}</em>?
    </DeleteDialog>
    <DeviceArchiveDialog
      v-if="device"
      v-model="showArchiveDialog"
      :device-to-archive="device"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="deviceSensorMLFilename"
      :url="deviceSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { ArchiveDeviceAction, DeleteDeviceAction, DevicesState, LoadDeviceAction, RestoreDeviceAction, ExportAsSensorMLAction, GetSensorMLUrlAction } from '@/store/devices'

import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DeviceArchiveDialog from '@/components/devices/DeviceArchiveDialog.vue'
import DeviceBasicData from '@/components/DeviceBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { Visibility } from '@/models/Visibility'

@Component({
  components: {
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenuActionSensorML,
    DotMenu,
    DeleteDialog,
    DeviceBasicData,
    DotMenuActionRestore,
    DotMenuActionArchive,
    DeviceArchiveDialog,
    DownloadDialog
  },
  computed: {
    ...mapState('devices', ['device']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDevice', 'deleteDevice', 'archiveDevice', 'restoreDevice', 'exportAsSensorML', 'getSensorMLUrl']),
    ...mapActions('progressindicator', ['setLoading'])
  }
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

  private showDeleteDialog: boolean = false
  private showArchiveDialog: boolean = false
  private showDownloadDialog: boolean = false

  // vuex definition for typescript check
  device!: DevicesState['device']
  loadDevice!: LoadDeviceAction
  deleteDevice!: DeleteDeviceAction
  archiveDevice!: ArchiveDeviceAction
  restoreDevice!: RestoreDeviceAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  get deviceId () {
    return this.$route.params.deviceId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  openSensorMLDialog () {
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
  }

  get deviceSensorMLFilename (): string {
    if (this.device != null) {
      return `${this.device.shortName}.xml`
    }
    return 'device.xml'
  }

  async deviceSensorMLUrl (): Promise<string | null> {
    if (!this.device) {
      return null
    }
    if (this.device?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.device.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.device!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Device could not be exported as SensorML')
        return null
      }
    }
  }

  async deleteAndCloseDialog () {
    if (this.device === null || this.device.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteDevice(this.device.id)
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
      this.$router.push('/devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    } finally {
      this.setLoading(false)
      this.showDeleteDialog = false
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
      this.setLoading(true)
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
      this.setLoading(false)
      this.showArchiveDialog = false
    }
  }

  async runRestore () {
    if (this.device === null || this.device.id === null) {
      return
    }
    this.setLoading(true)
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
      this.setLoading(false)
    }
  }
}
</script>
