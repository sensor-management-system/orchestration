<!--
SPDX-FileCopyrightText: 2020 - 2023
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/platforms/' + platformId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="platformAttachments.length === 0">
      There are no attachments for this platform.
    </hint-card>

    <BaseList
      :list-items="platformAttachments"
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
              :to="'/platforms/' + platformId + '/attachments/' + item.id + '/edit'"
            >
              Edit
            </v-btn>
          </template>
        </AttachmentListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="platformAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/platforms/' + platformId + '/attachments/new'"
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

import { PlatformsState, LoadPlatformAttachmentsAction, DeletePlatformAttachmentAction, DownloadAttachmentAction, LoadPlatformAction, DeletePlatformImageAction } from '@/store/platforms'

import { Attachment } from '@/models/Attachment'
import { Visibility } from '@/models/Visibility'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import HintCard from '@/components/HintCard.vue'
import BaseList from '@/components/shared/BaseList.vue'
import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'

import { getLastPathElement } from '@/utils/urlHelpers'
import { Image } from '@/models/Image'

@Component({
  components: { DeleteDialog, DotMenuActionDelete, AttachmentListItem, BaseList, HintCard, DownloadDialog },
  computed: {
    ...mapState('platforms', ['platformAttachments', 'platform']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatform', 'loadPlatformAttachments', 'deletePlatformAttachment', 'deletePlatformImage', 'downloadAttachment']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformAttachmentShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private attachmentToDelete: Attachment|null = null

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  platformAttachments!: PlatformsState['platformAttachments']
  platform!: PlatformsState['platform']
  loadPlatform!: LoadPlatformAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  deletePlatformAttachment!: DeletePlatformAttachmentAction
  deletePlatformImage!: DeletePlatformImageAction
  downloadAttachment!: DownloadAttachmentAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  get platformId (): string {
    return this.$route.params.platformId
  }

  initDeleteDialog (attachment: Attachment) {
    this.showDeleteDialog = true
    this.attachmentToDelete = attachment
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.attachmentToDelete = null
  }

  initDowloadDialog (attachment: Attachment) {
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
      if (this.platformImageUsingAttachment?.id) {
        await this.deletePlatformImage(this.platformImageUsingAttachment.id)
      }
      const attachmentId = this.attachmentToDelete.id
      await this.deletePlatformAttachment(attachmentId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')

      // update attachment previews
      try {
        this.loadPlatformAttachments(this.platformId)
        await this.loadPlatformAttachments(this.platformId)
        this.loadPlatform({
          platformId: this.platformId,
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
    this.initDowloadDialog(attachment)
  }

  get platformImageUsingAttachment (): Image | null {
    return this.platform?.images.find(image => image.attachment?.id === this.attachmentToDelete?.id) ?? null
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
    return this.platform?.visibility === Visibility.Public
  }
}
</script>

<style scoped>

</style>
