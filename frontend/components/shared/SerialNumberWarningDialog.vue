<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showSerialNumberWarning"
    width="500"
    @click:outside="closeDialog"
  >
    <v-card class="">
      <v-card-title class="text-h5">
        <v-icon>mdi-alert</v-icon>
        No serial number
      </v-card-title>

      <v-card-text>
        Saving without a serial number is not recommended. You might not be able to find this {{ entity }} again.
      </v-card-text>

      <v-card-actions>
        <v-spacer />

        <v-btn
          color=""
          text
          @click.stop="closeDialog"
        >
          Cancel
        </v-btn>

        <v-btn
          color="warning"
          @click="confirm"
        >
          Save anyway
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, ModelSync, Prop, Vue } from 'nuxt-property-decorator'

@Component({})
export default class SerialNumberWarningDialog extends Vue {
  @ModelSync('show', 'change', { type: Boolean })
    showSerialNumberWarning!: boolean

  @Prop({
    required: true
  })
    entity!: string

  closeDialog () {
    this.showSerialNumberWarning = false
    this.$emit('close')
  }

  confirm () {
    this.showSerialNumberWarning = false
    this.$emit('confirm')
  }
}
</script>
