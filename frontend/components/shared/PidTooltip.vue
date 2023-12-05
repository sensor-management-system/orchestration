<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
  <div>
    <v-tooltip
      :disabled="!value"
      :color="color"
      bottom
    >
      <template #activator="{ on, attrs }">
        <span
          :class="value ? 'clickable' : ''"
          v-bind="attrs"
          v-on="on"
          @click="copyToClipboard()"
          @mouseenter="reset()"
        >{{ value | orDefault }}</span>
      </template>
      <span>{{ text }}</span>
    </v-tooltip>
    <v-btn
      v-if="value && showButton"
      icon
      @click="showQrCode = true"
    >
      <v-icon>
        mdi-qrcode
      </v-icon>
    </v-btn>
    <qr-code-dialog v-model="showQrCode" :text="url" />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import QrCodeDialog from '@/components/QrCodeDialog.vue'

const PID_BASE_URL = process.env.pidBaseUrl
const TOOLTIP_DEFAULT_COLOR = 'default'
const TOOLTIP_SUCCESS_COLOR = 'green'
const TOOLTIP_DEFAULT_TEXT = 'Click to copy PID-URL'
const TOOLTIP_SUCCESS_TEXT = 'PID-URL copied'

enum STATES {
  default,
  success
}

@Component({
  components: {
    QrCodeDialog
  }
})
export default class PidTooltip extends Vue {
  private states = {
    [STATES.default]: {
      color: TOOLTIP_DEFAULT_COLOR,
      text: TOOLTIP_DEFAULT_TEXT
    },
    [STATES.success]: {
      color: TOOLTIP_SUCCESS_COLOR,
      text: TOOLTIP_SUCCESS_TEXT
    }
  }

  private state: STATES = STATES.default
  private showQrCode: boolean = false

  @Prop({
    default: () => '',
    required: true,
    type: String
  })
  readonly value!: string

  @Prop({
    default: () => false,
    required: false,
    type: Boolean
  })
  readonly showButton!: boolean

  get url (): string {
    if (!PID_BASE_URL) {
      return ''
    }
    if (!this.value) {
      return ''
    }
    return PID_BASE_URL + '/' + this.value
  }

  get text (): string {
    return this.states[this.state].text
  }

  get color (): string {
    return this.states[this.state].color
  }

  copyToClipboard (): void {
    if (!this.value) { return }
    navigator.clipboard.writeText(this.url)
    this.state = STATES.success
  }

  reset (): void {
    this.state = STATES.default
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
