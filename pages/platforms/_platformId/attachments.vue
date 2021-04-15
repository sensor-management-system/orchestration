<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn && !(isAddAttachmentPage)"
        color="primary"
        small
        :disabled="isEditAttachmentPage"
        :to="'/platforms/' + platformId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <template v-if="isAddAttachmentPage">
      <v-card class="mb-2">
        <NuxtChild @showsave="showsave" @input="addAttachmentToList" />
      </v-card>
    </template>
    <template
      v-for="(attachment, index) in attachments"
    >
      <template v-if="isLoggedIn && isEditModeForAttachment(attachment)">
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
              {{ filename(attachment) }}, uploaded at {{ uploadedDateTime(attachment) }}
            </v-list-item-subtitle>
            <v-list-item-title>
              <a :href="attachment.url" target="_blank">{{ attachment.label }}</a>
            </v-list-item-title>
            <v-list-item-action-text>
              <v-row>
                <v-col align-self="end" class="text-right">
                  <v-btn
                    v-if="isLoggedIn && !isEditAttachmentPage && !isAddAttachmentPage"
                    color="primary"
                    text
                    small
                    nuxt
                    :to="'/platforms/' + platformId + '/attachments/' + attachment.id + '/edit'"
                  >
                    Edit
                  </v-btn>
                  <v-menu
                    v-if="isLoggedIn"
                    close-on-click
                    close-on-content-click
                    offset-x
                    left
                    z-index="999"
                  >
                    <template v-slot:activator="{ on }">
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
                        v-if="isLoggedIn && !isAddAttachmentPage && !isEditAttachmentPage"
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
        v-if="isLoggedIn"
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
export default class PlatformAttachmentsPage extends mixins(AttachmentsMixin) {
  private attachments: Attachment[] = []
  private showDeleteDialog: {[idx: string]: boolean} = {}
  private isLoading = false
  private isSaving = false

  async fetch () {
    this.isLoading = true
    try {
      this.attachments = await this.$api.platforms.findRelatedPlatformAttachments(this.platformId)
      this.isLoading = false
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      this.isLoading = false
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditAttachmentPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/platforms\/' + this.platformId + '\/attachments\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isAddAttachmentPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/platforms\/' + this.platformId + '\/attachments\/new$'
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

      this.$api.platformAttachments.deleteById(id).then(() => {
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
    return this.$route.path === '/platforms/' + this.platformId + '/attachments/' + attachment.id + '/edit'
  }
}
</script>
