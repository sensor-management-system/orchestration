<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="680px"
  >
    <v-card>
      <v-card-title class="headline">
        {{ title }}
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="10">
            <div v-if="!disabled">
              <v-text-field v-model="editableText" label="URL" />
            </div>
            <div v-else>
              <label>URL</label>
              <ExpandableText :value="editableText" shorten-at="60" />
            </div>
          </v-col>
          <v-col cols="2" align-self="center">
            <v-btn icon :href="editableText" target="_blank" title="Open in new tab">
              <v-icon small>
                mdi-open-in-new
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <center>
              <vue-qr :text="editableText" :margin="0" />
            </center>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn
          v-if="!disabled"
          :disabled="text === editableText"
          text
          title="Reset to original URL"
          @click="resetText"
        >
          Reset
        </v-btn>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = false">
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
// @ts-ignore
import VueQr from 'vue-qr'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    ExpandableText,
    VueQr
  }
})
export default class QrCodeDialog extends Vue {
  private editableText: string = ''

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: true,
    type: String
  })
  readonly text!: string

  @Prop({
    required: false,
    default: false,
    type: Boolean
  })
  readonly disabled!: boolean

  @Prop({
    default: 'QR code',
    required: false,
    type: String
  })
  readonly title!: string

  created () {
    this.editableText = this.text
  }

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (newValue: boolean) {
    this.$emit('input', newValue)
  }

  resetText () {
    this.editableText = this.text
  }

  @Watch('text')
  onTextChange () {
    this.resetText()
  }

  @Watch('value')
  onValueChange () {
    // also set it to the default value every time the visibilty of the dialog changes
    this.resetText()
  }
}
</script>
