<!--
SPDX-FileCopyrightText: 2020 - 2023
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
        :to="'/configurations/' + configurationId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="configurationAttachments.length === 0">
      There are no attachments for this configuration.
    </hint-card>

    <BaseList
      :list-items="configurationAttachments"
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
              :to="'/configurations/' + configurationId + '/attachments/' + item.id + '/edit'"
            >
              Edit
            </v-btn>
          </template>
        </AttachmentListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="configurationAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/attachments/new'"
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

import { LoadConfigurationAttachmentsAction, DeleteConfigurationAttachmentAction, ConfigurationsState, DownloadAttachmentAction, DeleteConfigurationImageAction, LoadConfigurationAction } from '@/store/configurations'

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
  computed: {
    ...mapState('configurations', ['configurationAttachments', 'configuration']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfiguration', 'loadConfigurationAttachments', 'deleteConfigurationAttachment', 'deleteConfigurationImage', 'downloadAttachment']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationAttachmentShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private attachmentToDelete: Attachment | null = null

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  // vuex definition for typescript check
  configurationAttachments!: ConfigurationsState['configurationAttachments']
  configuration!: ConfigurationsState['configuration']
  deleteConfigurationAttachment!: DeleteConfigurationAttachmentAction
  deleteConfigurationImage!: DeleteConfigurationImageAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  downloadAttachment!: DownloadAttachmentAction
  setLoading!: SetLoadingAction
  loadConfiguration!: LoadConfigurationAction

  get configurationId (): string {
    return this.$route.params.configurationId
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
      if (this.configurationImageUsingAttachment?.id) {
        await this.deleteConfigurationImage(this.configurationImageUsingAttachment.id)
      }
      const attachmendId = this.attachmentToDelete.id
      this.closeDialog()
      await this.deleteConfigurationAttachment(attachmendId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')

      // update attachment previews
      try {
        await this.loadConfigurationAttachments(this.configurationId)
        this.loadConfiguration(this.configurationId)
      } catch (_error) {
        this.$store.commit('snackbar/setWarning', 'Failed to load configuration')
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

  get configurationImageUsingAttachment (): Image | null {
    return this.configuration?.images.find(image => image.attachment?.id === this.attachmentToDelete?.id) ?? null
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
    return this.configuration?.visibility === Visibility.Public
  }
}
</script>

<style scoped>

</style>
