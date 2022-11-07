<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <AttachmentDeleteDialog
      v-model="showDeleteDialog"
      :attachment-to-delete="attachmentToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { PlatformsState, LoadPlatformAttachmentsAction, DeletePlatformAttachmentAction, DownloadAttachmentAction } from '@/store/platforms'

import { Attachment } from '@/models/Attachment'
import { Visibility } from '@/models/Visibility'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import HintCard from '@/components/HintCard.vue'
import BaseList from '@/components/shared/BaseList.vue'
import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import AttachmentDeleteDialog from '@/components/shared/AttachmentDeleteDialog.vue'

@Component({
  components: { AttachmentDeleteDialog, DotMenuActionDelete, AttachmentListItem, BaseList, HintCard, ProgressIndicator },
  computed: mapState('platforms', ['platformAttachments', 'platform']),
  methods: mapActions('platforms', ['loadPlatformAttachments', 'deletePlatformAttachment', 'downloadAttachment'])
})
export default class PlatformAttachmentShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private isSaving = false
  private showDeleteDialog = false
  private attachmentToDelete: Attachment|null = null

  // vuex definition for typescript check
  platformAttachments!: PlatformsState['platformAttachments']
  platform!: PlatformsState['platform']
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  deletePlatformAttachment!: DeletePlatformAttachmentAction
  downloadAttachment!: DownloadAttachmentAction

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

  async deleteAndCloseDialog () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      this.isSaving = true
      const attachmentId = this.attachmentToDelete.id
      this.closeDialog()
      await this.deletePlatformAttachment(attachmentId)
      this.loadPlatformAttachments(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.isSaving = false
    }
  }

  async openAttachment (attachment: Attachment) {
    try {
      const blob = await this.downloadAttachment(attachment.url)
      const url = window.URL.createObjectURL(blob)
      window.open(url)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Attachment could not be loaded')
    }
  }

  get isPublic () {
    return this.platform?.visibility === Visibility.Public
  }
}
</script>

<style scoped>

</style>
