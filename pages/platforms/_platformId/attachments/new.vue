<template>
  <v-form ref="attachmentsForm" class="pl-10" @submit.prevent>
    <v-row>
      <v-col cols="12" md="3">
        <v-radio-group
          v-model="attachmentType"
          label="Type"
          row
        >
          <v-radio label="File" value="file" />
          <v-radio label="Url" value="url" />
        </v-radio-group>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-file-input
          v-if="attachmentType === 'file'"
          v-model="file"
          :accept="mimeTypeList"
          label="File"
          required
          class="required"
          :rules="[rules.required]"
          show-size
        />
        <v-text-field
          v-if="attachmentType === 'url'"
          v-model="attachment.url"
          label="URL"
          type="url"
          placeholder="http://"
          required
          class="required"
          :rules="[rules.required, rules.validUrl]"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="attachment.label"
          label="Label"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-spacer />
        <v-btn
          v-if="isLoggedIn"
          ref="cancelButton"
          text
          small
          :to="'/platforms/' + platformId + '/attachments'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
          color="green"
          small
          data-role="add-attachment"
          @click="add()"
        >
          {{ attachmentType === 'url' ? 'Add' : 'Upload' }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { Rules } from '@/mixins/Rules'

import { Attachment } from '@/models/Attachment'

@Component({
  components: {}
})
export default class AttachmentAddPage extends mixins(Rules) {
  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null

  mounted () {
    const cancelButton = this.$refs.cancelButton as Vue
    // due to the active route (and the button being a router link)
    // this button has the active class
    // however, we don't want this special behaviour for this button
    cancelButton.$el.classList.remove('v-btn--active')
  }

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return Object.keys(Attachment.mimeTypes).join(',')
  }

  add () {
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    this.$emit('showsave', true)
    this.$api.platformAttachments.add(this.platformId, this.attachment).then((newAttachment: Attachment) => {
      this.$emit('showsave', false)
      this.$emit('input', newAttachment)
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    })
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
