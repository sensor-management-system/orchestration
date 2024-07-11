<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showNavigationWarning"
    width="500"
    @click:outside="closeDialog"
  >
    <v-card class="">
      <v-card-title class="text-h5">
        <v-icon>mdi-alert</v-icon>
        Unsaved changes
      </v-card-title>

      <v-card-text>
        You have unsaved changes. Are you sure you want to leave the page?
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
          @click="discardChanges"
        >
          Yes, discard changes
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, Prop, ModelSync, Vue } from 'nuxt-property-decorator'

@Component({})
export default class NavigationGuardDialog extends Vue {
  @Prop({
    type: Boolean,
    required: true,
    default: false
  })
  readonly hasEntityChanged!: boolean

  @Prop({
    type: [Object, String]
  })
  readonly to!: string

  @ModelSync('show', 'change', { type: Boolean })
    showNavigationWarning!: boolean

  closeDialog () {
    this.showNavigationWarning = false
    this.$emit('close')
  }

  discardChanges () {
    this.showNavigationWarning = false
    this.$router.push(this.to)
  }
}
</script>
