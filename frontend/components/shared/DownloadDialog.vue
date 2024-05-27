<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="500"
    @click:outside="$emit('cancel')"
  >
    <v-card>
      <v-card-title>
        Opening {{ filename }}
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>You have chosen to open:</v-col>
        </v-row>
        <v-row>
          <v-col><v-icon>mdi-file</v-icon><b>{{ filename }}</b></v-col>
        </v-row>
        <v-row>
          <v-col>What should be done with this file?</v-col>
        </v-row>
        <v-radio-group v-model="selectedAction">
          <v-radio label="Open in browser" value="open" />
          <v-radio label="Save file" value="download" />
        </v-radio-group>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('cancel')">
          Cancel
        </v-btn>
        <v-btn text color="primary" :disabled="selectedAction == null" @click="doAction">
          Ok
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

@Component
export default class DownloadDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: true,
    type: String
  })
  readonly filename!: string

  @Prop({
    required: true,
    type: Function
  })
  readonly url!: () => Promise<string>

  private selectedAction: string | null = null

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  doAction () {
    const actions: {[idx: string]: () => any} = {
      open: this.open,
      download: this.download
    }
    if (this.selectedAction !== null) {
      if (actions[this.selectedAction]) {
        actions[this.selectedAction]()
      } else {
        this.$emit(this.selectedAction)
      }
    }
  }

  async open () {
    window.open(await this.url())
    this.showDialog = false
  }

  async download () {
    const link = document.createElement('a')
    link.href = await this.url()
    link.download = this.filename
    link.click()
    this.showDialog = false
  }
}
</script>
