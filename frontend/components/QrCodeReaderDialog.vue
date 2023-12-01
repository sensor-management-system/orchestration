<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
