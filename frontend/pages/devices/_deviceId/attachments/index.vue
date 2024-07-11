<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/devices/' + deviceId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceAttachments.length === 0">
      There are no attachments for this device.
    </hint-card>

    <BaseList
      :list-items="deviceAttachments"
    >
      <template #list-item="{item}">
        <AttachmentListItem
          :attachment="item"
          :is-public="isPublic"
          @open-attachment="openAttachment"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!editable"
              @click="initDeleteDialog(item)"
            />
          </template>
          <template #edit-action>
            <v-btn
              v-if="editable"
              color="primary"
              text
              small
              nuxt
              :to="'/devices/' + deviceId + '/attachments/' + item.id + '/edit'"
            >
              Edit
            </v-btn>
          </template>
        </AttachmentListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <DeleteDialog
      v-if="attachmentToDelete"
      v-model="showDeleteDialog"
      title="Delete Attachment"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the attachment <em>{{ attachmentToDelete.label }}</em>?
    </DeleteDialog>
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedAttachmentFilename"
      :url="selectedAttachmentUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { LoadDeviceAction, LoadDeviceAttachmentsAction, DeleteDeviceImageAction, DeleteDeviceAttachmentAction, DevicesState, DownloadAttachmentAction } from '@/store/devices'

import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'

import BaseList from '@/components/shared/BaseList.vue'
import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import HintCard from '@/components/HintCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { Visibility } from '@/models/Visibility'
import { getLastPathElement } from '@/utils/urlHelpers'

@Component({
  components: { DotMenuActionDelete, HintCard, DeleteDialog, AttachmentListItem, BaseList, DownloadDialog },
  computed: {
    ...mapState('devices', ['deviceAttachments', 'device']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDevice', 'loadDeviceAttachments', 'deleteDeviceAttachment', 'downloadAttachment', 'deleteDeviceImage']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceAttachmentShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private attachmentToDelete: Attachment | null = null

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  deviceAttachments!: DevicesState['deviceAttachments']
  device!: DevicesState['device']
  loadDevice!: LoadDeviceAction
  deleteDeviceAttachment!: DeleteDeviceAttachmentAction
  deleteDeviceImage!: DeleteDeviceImageAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  downloadAttachment!: DownloadAttachmentAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initDeleteDialog (attachment: Attachment) {
    this.showDeleteDialog = true
    this.attachmentToDelete = attachment
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.attachmentToDelete = null
  }

  initDownloadDialog (attachment: Attachment) {
    this.attachmentToDownload = attachment
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
    this.attachmentToDownload = null
  }

  async deleteAndCloseDialog () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      if (this.deviceImageUsingAttachment?.id) {
        await this.deleteDeviceImage(this.deviceImageUsingAttachment.id)
      }
      const attachmentId = this.attachmentToDelete.id
      await this.deleteDeviceAttachment(attachmentId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')

      // update attachment previews
      try {
        await this.loadDeviceAttachments(this.deviceId)
        this.loadDevice({
          deviceId: this.deviceId,
          includeImages: true,
          includeCreatedBy: true,
          includeUpdatedBy: true
        })
      } catch (_error) {
        this.$store.commit('snackbar/setWarning', 'Failed to load device')
      }
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  openAttachment (attachment: Attachment) {
    this.initDownloadDialog(attachment)
  }

  get deviceImageUsingAttachment (): Image | null {
    return this.device?.images.find(image => image.attachment?.id === this.attachmentToDelete?.id) ?? null
  }

  get selectedAttachmentFilename (): string {
    if (this.attachmentToDownload) {
      return getLastPathElement(this.attachmentToDownload.url)
    }
    return 'attachment'
  }

  async selectedAttachmentUrl (): Promise<string | null> {
    if (!this.attachmentToDownload) {
      return null
    }
    try {
      const blob = await this.downloadAttachment(this.attachmentToDownload.url)
      const url = window.URL.createObjectURL(blob)
      return url
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Attachment could not be loaded')
    }
    return null
  }

  get isPublic () {
    return this.device?.visibility === Visibility.Public
  }
}
</script>

<style scoped>

</style>
