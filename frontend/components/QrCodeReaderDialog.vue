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
        Scan QR code
      </v-card-title>
      <v-card-text>
        <v-card v-if="!initialized" flat>
          Waiting for the scanner to be ready.
          You may need to allow the camera usage.
        </v-card>
        <v-card v-if="scanningActive" flat>
          <!-- You may wonder about the additional v-if here for the reader.
               Reason is that we can make sure that it is properly initialized
               after we re-opened the dialog.
               Otherwise it may cause problems with the reset function of
               the scanners codeReader.
          -->
          <stream-barcode-reader
            v-if="showDialog"
            ref="scanner"
            @decode="onDecode"
            @loaded="onLoaded"
          />
        </v-card>
        <v-card v-else flat>
          <v-row>
            <v-col cols="12">
              <label>URL</label>
              <ExpandableText :value="scanResult" :shorten-at="60" />
              <v-btn icon :href="scanResult" target="_blank">
                <v-icon small title="Open in new tab">
                  mdi-open-in-new
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-card-text>
      <v-card-actions>
        <v-btn :disabled="scanningActive" text title="Rescan QR code" @click="reset">
          <v-icon small>
            mdi-qrcode-scan
          </v-icon>
          &nbsp;Rescan
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
import { StreamBarcodeReader } from 'vue-barcode-reader'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    ExpandableText,
    StreamBarcodeReader
  }
})
export default class QrCodeReaderDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  private scanningActive = true
  private scanResult = ''
  private initialized = false

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (newValue: boolean) {
    this.$emit('input', newValue)
  }

  onDecode (text: string) {
    this.deactivateScanning()
    this.scanResult = text
    this.scanningActive = false
  }

  deactivateScanning () {
    if (this.$refs.scanner) {
      (this.$refs.scanner as any).codeReader.reset()
    }
  }

  onLoaded () {
    this.initialized = true
  }

  reset () {
    this.scanResult = ''
    this.scanningActive = true
  }

  @Watch('value')
  onVisibilityChange (newVal: boolean) {
    this.reset()
    if (!newVal) {
      // In case we close the dialog, we want to stop the camera usage.
      this.deactivateScanning()
    }
  }
}
</script>
