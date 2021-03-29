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
import { Component, Vue } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'

import AttachmentListItem from '@/components/AttachmentListItem.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    AttachmentListItem,
    ProgressIndicator
  }
})
export default class PlatformAttachmentsPage extends Vue {
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

  /**
   * returns a filename from a full filepath
   *
   * @return {string} the filename
   */
  filename (attachment: Attachment): string {
    const UNKNOWN_FILENAME = 'unknown filename'

    if (attachment.url === '') {
      return UNKNOWN_FILENAME
    }
    const paths = attachment.url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  /**
   * returns the timestamp of the upload date
   *
   * @TODO this must be implemented when the file API is ready
   * @return {string} a readable timestamp
   */
  uploadedDateTime (_attachment: Attachment): string {
    return '2020-06-17 16:35 (TODO)'
  }

  /**
   * returns a material design icon name based on the file type extension
   *
   * @return {string} a material design icon name
   */
  filetypeIcon (attachment: Attachment): string {
    let extension = ''
    const paths = this.filename(attachment).split('.')
    if (paths.length) {
      // @ts-ignore
      extension = paths.pop().toLowerCase()
    }
    switch (extension) {
      case 'png':
      case 'jpg':
      case 'jpeg':
        return 'mdi-image'
      case 'pdf':
        return 'mdi-file-pdf-box'
      case 'doc':
      case 'docx':
      case 'odt':
        return 'mdi-text-box'
      default:
        return 'mdi-paperclip'
    }
  }
}
</script>
