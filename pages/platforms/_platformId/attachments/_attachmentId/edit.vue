<template>
  <v-card class="mb-2">
    <v-list-item>
      <v-list-item-avatar>
        <v-icon large>
          {{ filetypeIcon }}
        </v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-subtitle>
          {{ filename }}, uploaded at {{ uploadedDateTime }}
        </v-list-item-subtitle>
        <v-list-item-title>
          <v-text-field
            v-model="valueCopy.label"
          />
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action-text>
        <v-row>
          <v-col align-self="end" class="text-right">
            <v-btn
              icon
              color="primary"
              :href="valueCopy.url"
              target="_blank"
            >
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </v-btn>
            <v-btn
              ref="cancelButton"
              text
              small
              :to="'/platforms/' + platformId + '/attachments'"
            >
              Cancel
            </v-btn>
            <v-btn
              color="green"
              small
              @click.prevent.stop="save"
            >
              Apply
            </v-btn>
          </v-col>
        </v-row>
      </v-list-item-action-text>
    </v-list-item>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AttachmentEditPage extends Vue {
  private valueCopy: Attachment = new Attachment()

  /**
   * an Attachment
   */
  @Prop({
    required: true,
    type: Attachment
  })
  // @ts-ignore
  readonly value!: Attachment

  created () {
    this.valueCopy = Attachment.createFromObject(this.value)
  }

  mounted () {
    const cancelButton = this.$refs.cancelButton as Vue
    // due to the active route (and the button being a router link)
    // this button has the active class
    // however, we don't want this special behaviour for this button
    cancelButton.$el.classList.remove('v-btn--active')
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  /**
   * returns the timestamp of the upload date
   *
   * @TODO this must be implemented when the file API is ready
   * @return {string} a readable timestamp
   */
  get uploadedDateTime (): string {
    return '2020-06-17 16:35 (TODO)'
  }

  /**
   * returns a filename from a full filepath
   *
   * @return {string} the filename
   */
  get filename (): string {
    const UNKNOWN_FILENAME = 'unknown filename'

    if (this.valueCopy.url === '') {
      return UNKNOWN_FILENAME
    }
    const paths = this.valueCopy.url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  save () {
    this.$emit('showsave', true)
    this.$api.platformAttachments.update(this.platformId, this.valueCopy).then((savedAttachment: Attachment) => {
      this.$emit('showsave', false)
      this.$emit('input', savedAttachment)
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    })
  }
}
</script>
