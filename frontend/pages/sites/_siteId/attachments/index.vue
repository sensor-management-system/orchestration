<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
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
        :to="'/sites/' + siteId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="siteAttachments.length === 0">
      There are no attachments for this site.
    </hint-card>

    <BaseList
      :list-items="siteAttachments"
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
              :to="'/sites/' + siteId + '/attachments/' + item.id + '/edit'"
            >
              Edit
            </v-btn>
          </template>
        </AttachmentListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="siteAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/sties/' + siteId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <DeleteDialog
      v-if="attachmentToDelete"
      v-model="showDeleteDialog"
      title="Delete Attachment"
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

import { LoadSiteAttachmentsAction, DeleteSiteAttachmentAction, SitesState, DownloadAttachmentAction, DeleteSiteImageAction, LoadSiteAction } from '@/store/sites'

import { Attachment } from '@/models/Attachment'
import { Visibility } from '@/models/Visibility'

import BaseList from '@/components/shared/BaseList.vue'
import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import HintCard from '@/components/HintCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { getLastPathElement } from '@/utils/urlHelpers'
import { Image } from '@/models/Image'

@Component({
  components: { DotMenuActionDelete, HintCard, DeleteDialog, AttachmentListItem, BaseList, DownloadDialog },
  computed: mapState('sites', ['siteAttachments', 'site']),
  methods: {
    ...mapActions('sites', ['laodSite', 'loadSiteAttachments', 'deleteSiteAttachment', 'deleteSiteImage', 'downloadAttachment']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteAttachmentShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private attachmentToDelete: Attachment | null = null

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  siteAttachments!: SitesState['siteAttachments']
  site!: SitesState['site']
  loadSite!: LoadSiteAction
  deleteSiteAttachment!: DeleteSiteAttachmentAction
  deleteSiteImage!: DeleteSiteImageAction
  loadSiteAttachments!: LoadSiteAttachmentsAction
  downloadAttachment!: DownloadAttachmentAction
  setLoading!: SetLoadingAction

  get siteId (): string {
    return this.$route.params.siteId
  }

  initDeleteDialog (attachment: Attachment) {
    this.showDeleteDialog = true
    this.attachmentToDelete = attachment
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.attachmentToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      if (this.siteImageUsingAttachment?.id) {
        await this.deleteSiteImage(this.siteImageUsingAttachment.id)
      }
      const attachmendId = this.attachmentToDelete.id
      this.closeDialog()
      await this.deleteSiteAttachment(attachmendId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')

      // update attachment previews
      try {
        await this.loadSiteAttachments(this.siteId)
        this.loadSite({
          siteId: this.siteId,
          includeImages: true,
          includeCreatedBy: true,
          includeUpdatedBy: true
        })
      } catch (_error) {
        this.$store.commit('snackbar/setWarning', 'Failed to load site')
      }
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.setLoading(false)
    }
  }

  initDowloadDialog (attachment: Attachment) {
    this.attachmentToDownload = attachment
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
    this.attachmentToDownload = null
  }

  openAttachment (attachment: Attachment) {
    this.initDowloadDialog(attachment)
  }

  get siteImageUsingAttachment (): Image | null {
    return this.site?.images.find(image => image.attachment?.id === this.attachmentToDelete?.id) ?? null
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
    return this.site?.visibility === Visibility.Public
  }
}
</script>

<style scoped>

</style>
