<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-alert v-if="canHandleExportControl" text type="info" dismissible>
      <p>
        You are part of the export control group and see more information than
        normal users will see.
        Fields are marked according to their visibility for others:
      </p>
      <p class="mb-0">
        {{ visibiltyMarkerPublic }} visible for everyone
      </p>
      <p class="mb-0">
        {{ visibiltyMarkerInternal }} only visible for export control group
      </p>
    </v-alert>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="canHandleExportControl"
        color="primary"
        small
        nuxt
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control/edit'"
      >
        Edit
      </v-btn>
      <dot-menu v-if="canHandleExportControl && exportControl && exportControl.id">
        <template #actions>
          <dot-menu-action-delete
            @click="initDeleteDialogForExportControl(exportControl)"
          />
        </template>
      </dot-menu>
    </v-card-actions>
    <export-control-basic-data
      v-if="exportControl"
      v-model="exportControl"
      :show-internal-note="canHandleExportControl"
      :visibilty-marker-public="canHandleExportControl? visibiltyMarkerPublic : ''"
      :visibilty-marker-internal="canHandleExportControl? visibiltyMarkerInternal : ''"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="canHandleExportControl"
        color="primary"
        small
        nuxt
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <v-card v-if="publicExportControlAttachments.length > 0" flat>
      <v-card-subtitle>Attachments<span v-if="canHandleExportControl"> {{ visibiltyMarkerPublic }}</span>:</v-card-subtitle>
      <base-list :list-items="publicExportControlAttachments">
        <template #list-item="{ item }">
          <attachment-list-item
            :attachment="item"
            :is-public="true"
          >
            <template v-if="canHandleExportControl" #dot-menu-items>
              <dot-menu-action-delete @click="initDeleteDialogForAttachment(item)" />
            </template>
            <template v-if="canHandleExportControl" #edit-action>
              <v-btn
                color="primary"
                text
                small
                nuxt
                :to="'/manufacturer-models/' + manufacturerModelId + '/export-control/attachments/' + item.id + '/edit'"
              >
                Edit
              </v-btn>
            </template>
          </attachment-list-item>
        </template>
      </base-list>
    </v-card>

    <v-card v-if="internalExportControlAttachments.length > 0 && canHandleExportControl" flat>
      <v-card-subtitle>Internal attachments<span v-if="canHandleExportControl"> {{ visibiltyMarkerInternal }}</span>:</v-card-subtitle>
      <base-list :list-items="internalExportControlAttachments">
        <template #list-item="{ item }">
          <attachment-list-item
            :attachment="item"
            :is-public="false"
            @open-attachment="openAttachment"
          >
            <template #dot-menu-items>
              <dot-menu-action-delete @click="initDeleteDialogForAttachment(item)" />
            </template>
            <template #edit-action>
              <v-btn
                color="primary"
                text
                small
                nuxt
                :to="'/manufacturer-models/' + manufacturerModelId + '/export-control/attachments/' + item.id + '/edit'"
              >
                Edit
              </v-btn>
            </template>
          </attachment-list-item>
        </template>
      </base-list>
    </v-card>
    <v-row
      v-if="exportControl && (exportControlCreatedByContact || exportControlCreatedByContact)"
      class="mt-4"
      dense
    >
      <v-col
        class="text-caption font-weight-thin text-right"
      >
        <template
          v-if="exportControlCreatedByContact"
        >
          created by {{ exportControlCreatedByContact }}<span v-if="exportControl.createdAt"> at {{ exportControl.createdAt | toUtcDateTimeString }}</span><span v-if="exportControlUpdatedByContact">,</span>
        </template>
        <template
          v-if="exportControlCreatedByContact"
        >
          updated by {{ exportControlCreatedByContact }}<span v-if="exportControl.updatedAt"> at {{ exportControl.updatedAt | toUtcDateTimeString }}</span>
        </template>
      </v-col>
    </v-row>
    <delete-dialog
      v-if="exportControlToDelete"
      v-model="showDeleteDialogForExportControl"
      title="Delete Export Control"
      :disabled="isLoading"
      @cancel="closeDeleteDialogForExportControl"
      @delete="deleteAndCloseDialogForExportControl"
    >
      Do you really want to delete the export control information?
    </delete-dialog>
    <delete-dialog
      v-if="attachmentToDelete"
      v-model="showDeleteDialogForAttachment"
      title="Delete Attachment"
      :disabled="isLoading"
      @cancel="closeDeleteDialogForAttachment"
      @delete="deleteAndCloseDialogForAttachment"
    >
      Do you really want to delete the attachment <em>{{ attachmentToDelete.label }}</em>?
    </delete-dialog>
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedAttachmentFilename"
      :url="selectedAttachmentUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import {
  ManufacturermodelsState,
  LoadExportControlAction,
  LoadExportControlAttachmentsAction,
  PublicExportControlAttachmentsGetter,
  InternalExportControlAttachmentsGetter,
  DownloadAttachmentAction,
  DeleteExportControlAttachmentAction,
  LoadExportControlCreatedAndUpdatedByContactsAction,
  DeleteExportControlAction
} from '@/store/manufacturermodels'
import { CanHandleExportControlGetter } from '@/store/permissions'

import { ExportControlAttachment } from '@/models/ExportControlAttachment'

import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import BaseList from '@/components/shared/BaseList.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DotMenu from '@/components/DotMenu.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ExportControlBasicData from '@/components/manufacturerModels/ExportControlBasicData.vue'

import { getLastPathElement } from '@/utils/urlHelpers'
import { LoadingSpinnerState, SetLoadingAction } from '@/store/progressindicator'
import { ExportControl } from '@/models/ExportControl'

@Component({
  computed: {
    ...mapState('manufacturermodels', ['exportControl', 'exportControlCreatedByContact', 'exportControlUpdatedByContact']),
    ...mapGetters('manufacturermodels', ['publicExportControlAttachments', 'internalExportControlAttachments']),
    ...mapGetters('permissions', ['canHandleExportControl']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('manufacturermodels', [
      'loadExportControl',
      'loadExportControlAttachments',
      'downloadAttachment',
      'deleteExportControlAttachment',
      'loadExportControlCreatedAndUpdatedByContacts',
      'deleteExportControl'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    AttachmentListItem,
    BaseList,
    DeleteDialog,
    DotMenu,
    DownloadDialog,
    DotMenuActionDelete,
    ExportControlBasicData
  }
})
export default class ManufacturerModelShowExportControlPage extends Vue {
  private attachmentToDownload: ExportControlAttachment | null = null
  private showDownloadDialog = false

  private showDeleteDialogForAttachment = false
  private attachmentToDelete: ExportControlAttachment | null = null

  private showDeleteDialogForExportControl = false
  private exportControlToDelete: ExportControl | null = null

  private readonly visibiltyMarkerPublic = '👁' // an eye to indicate that it is visible
  private readonly visibiltyMarkerInternal = 'Ⓔ' // an E to indicate it is visible for the export control group

  exportControl!: ManufacturermodelsState['exportControl']
  exportControlCreatedByContact!: ManufacturermodelsState['exportControlCreatedByContact']
  exportControlUpdatedByContact!: ManufacturermodelsState['exportControlUpdatedByContact']
  isLoading!: LoadingSpinnerState['isLoading']
  canHandleExportControl!: CanHandleExportControlGetter
  publicExportControlAttachments!: PublicExportControlAttachmentsGetter
  internalExportControlAttachments!: InternalExportControlAttachmentsGetter
  loadExportControl!: LoadExportControlAction
  loadExportControlAttachments!: LoadExportControlAttachmentsAction
  downloadAttachment!: DownloadAttachmentAction
  deleteExportControlAttachment!: DeleteExportControlAttachmentAction
  loadExportControlCreatedAndUpdatedByContacts!: LoadExportControlCreatedAndUpdatedByContactsAction
  setLoading!: SetLoadingAction
  deleteExportControl!: DeleteExportControlAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadExportControl({ manufacturerModelId: this.manufacturerModelId }),
        this.loadExportControlAttachments(this.manufacturerModelId)
      ])
      this.loadExportControlCreatedAndUpdatedByContacts(this.exportControl)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of export control information failed')
    } finally {
      this.setLoading(false)
    }
  }

  get manufacturerModelId () {
    return this.$route.params.manufacturerModelId
  }

  openAttachment (attachment: ExportControlAttachment) {
    this.initDownloadDialog(attachment)
  }

  initDownloadDialog (attachment: ExportControlAttachment) {
    this.attachmentToDownload = attachment
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
    this.attachmentToDownload = null
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

  get selectedAttachmentFilename (): string {
    if (this.attachmentToDownload) {
      return getLastPathElement(this.attachmentToDownload.url)
    }
    return 'attachment'
  }

  initDeleteDialogForAttachment (attachment: ExportControlAttachment) {
    this.showDeleteDialogForAttachment = true
    this.attachmentToDelete = attachment
  }

  closeDeleteDialogForAttachment () {
    this.showDeleteDialogForAttachment = false
    this.attachmentToDelete = null
  }

  async deleteAndCloseDialogForAttachment () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      const attachmentId = this.attachmentToDelete.id
      await this.deleteExportControlAttachment(attachmentId)
      let switchToSearchPage = false
      try {
        await this.loadExportControlAttachments(this.manufacturerModelId)
      } catch (_error) {
        // manufacturer model entry was deleted due to bookkeeping rules,
        // so loading the information failed.
        switchToSearchPage = true
      }
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')
      if (switchToSearchPage) {
        this.$router.push('/manufacturer-models/')
      }
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.setLoading(false)
      this.closeDeleteDialogForAttachment()
    }
  }

  initDeleteDialogForExportControl (exportControl: ExportControl) {
    this.showDeleteDialogForExportControl = true
    this.exportControlToDelete = exportControl
  }

  closeDeleteDialogForExportControl () {
    this.showDeleteDialogForExportControl = false
    this.exportControlToDelete = null
  }

  async deleteAndCloseDialogForExportControl () {
    if (this.exportControlToDelete === null || this.exportControlToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      const exportControlId = this.exportControlToDelete.id
      await this.deleteExportControl(exportControlId)
      let switchToSearchPage = false
      try {
        await this.loadExportControl({ manufacturerModelId: this.manufacturerModelId })
      } catch (_error) {
        // manufacturer model entry was deleted due to bookkeeping rules,
        // so loading the information failed.
        switchToSearchPage = true
      }
      this.$store.commit('snackbar/setSuccess', 'Export control information deleted')
      if (switchToSearchPage) {
        this.$router.push('/manufacturer-models/')
      }
    } catch (_errror) {
      this.$store.commit('snackbar/setError', 'Failed to delete export control information')
    } finally {
      this.setLoading(false)
      this.closeDeleteDialogForExportControl()
    }
  }
}
</script>
