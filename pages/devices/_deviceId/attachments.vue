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
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions
      v-if="$auth.loggedIn && !(isAddAttachmentPage)"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :disabled="isEditAttachmentPage"
        :to="'/devices/' + deviceId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <template v-if="isAddAttachmentPage">
      <NuxtChild @showsave="showsave" @input="addAttachmentToList" />
    </template>
    <template
      v-for="(attachment, index) in attachments"
    >
      <template v-if="$auth.loggedIn && isEditModeForAttachment(attachment)">
        <NuxtChild
          :key="attachment.id"
          v-model="attachments[index]"
          @showsave="showsave"
        />
      </template>
      <v-card v-else :key="attachment.id" class="mb-2">
        <v-list-item>
          <v-list-item-avatar>
            <v-icon large>
              {{ filetypeIcon(attachment) }}
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-subtitle>
              {{ filename(attachment) }}
            </v-list-item-subtitle>
            <v-list-item-title v-if="attachment.label">
              <a :href="attachment.url" target="_blank">{{ attachment.label }}</a>
            </v-list-item-title>
            <v-list-item-title v-else>
              <a :href="attachment.url" target="_blank">
                <v-icon color="primary">mdi-open-in-new</v-icon>
              </a>
            </v-list-item-title>
            <v-list-item-action-text>
              <v-row>
                <v-col align-self="end" class="text-right">
                  <v-btn
                    v-if="$auth.loggedIn && !isEditAttachmentPage && !isAddAttachmentPage"
                    color="primary"
                    text
                    small
                    nuxt
                    :to="'/devices/' + deviceId + '/attachments/' + attachment.id + '/edit'"
                  >
                    Edit
                  </v-btn>
                  <v-menu
                    v-if="$auth.loggedIn"
                    close-on-click
                    close-on-content-click
                    offset-x
                    left
                    z-index="999"
                  >
                    <template #activator="{ on }">
                      <v-btn
                        data-role="property-menu"
                        icon
                        small
                        v-on="on"
                      >
                        <v-icon
                          dense
                          small
                        >
                          mdi-dots-vertical
                        </v-icon>
                      </v-btn>
                    </template>
                    <v-list>
                      <v-list-item
                        v-if="$auth.loggedIn && !isAddAttachmentPage && !isEditAttachmentPage"
                        dense
                        @click="showDeleteDialogFor(attachment.id)"
                      >
                        <v-list-item-content>
                          <v-list-item-title
                            class="red--text"
                          >
                            <v-icon
                              left
                              small
                              color="red"
                            >
                              mdi-delete
                            </v-icon>
                            Delete
                          </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </v-col>
              </v-row>
            </v-list-item-action-text>
          </v-list-item-content>
        </v-list-item>
        <v-dialog v-model="showDeleteDialog[attachment.id]" max-width="290">
          <v-card>
            <v-card-title class="headline">
              Delete Attachment
            </v-card-title>
            <v-card-text>
              Do you really want to delete the attachment <em>{{ attachment.label }}</em>?
            </v-card-text>
            <v-card-actions>
              <v-btn
                text
                @click="hideDeleteDialogFor(attachment.id)"
              >
                No
              </v-btn>
              <v-spacer />
              <v-btn
                color="error"
                text
                @click="deleteAndCloseDialog(attachment.id)"
              >
                <v-icon left>
                  mdi-delete
                </v-icon>
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card>
    </template>
    <v-card-actions
      v-if="attachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        :disabled="isEditAttachmentPage || isAddAttachmentPage"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

import AttachmentListItem from '@/components/AttachmentListItem.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    AttachmentListItem,
    ProgressIndicator
  }
})
export default class DeviceAttachmentsPage extends mixins(AttachmentsMixin) {
  private attachments: Attachment[] = []
  private showDeleteDialog: {[idx: string]: boolean} = {}
  private isLoading = false
  private isSaving = false

  async fetch () {
    this.isLoading = true
    try {
      this.attachments = await this.$api.devices.findRelatedDeviceAttachments(this.deviceId)
      this.isLoading = false
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      this.isLoading = false
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isEditAttachmentPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/attachments\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isAddAttachmentPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/devices\/' + this.deviceId + '\/attachments\/new$'
    return !!this.$route.path.match(addUrl)
  }

  showsave (shouldShowSave: boolean) {
    this.isSaving = shouldShowSave
  }

  addAttachmentToList (newAttachment: Attachment) {
    this.attachments.push(newAttachment)
  }

  deleteAndCloseDialog (id: string) {
    if (id) {
      this.isSaving = true
      this.showDeleteDialog = {}

      this.$api.deviceAttachments.deleteById(id).then(() => {
        const searchIndex = this.attachments.findIndex(a => a.id === id)
        if (searchIndex > -1) {
          this.attachments.splice(searchIndex, 1)
        }
        this.isSaving = false
      }).catch((_error) => {
        this.isSaving = false
        this.$store.commit('snackbar/setError', 'Failed to delete attachment')
      })
    }
  }

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
  }

  isEditModeForAttachment (attachment: Attachment): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/attachments/' + attachment.id + '/edit'
  }

  attachmentLabel (attachment: Attachment) : string {
    return attachment.label || 'Attachment'
  }
}
</script>
