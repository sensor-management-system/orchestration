<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="500"
    @click:outside="$emit('cancel-archiving')"
  >
    <v-card v-if="hasSiteToArchive">
      <v-card-title class="headline">
        Archive site / lab
      </v-card-title>
      <v-card-text>
        <p>Do you really want to archive the site / lab <em>{{ siteToArchive.label }}</em>?</p>
        <p>
          Achived sites &amp; labs can no longer be edited or used until they are restored.
        </p>
        <p>
          They are not included in the sites &amp; labs search by default.
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="$emit('cancel-archiving')"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          text
          @click="$emit('submit-archiving')"
        >
          <v-icon left>
            mdi-archive-lock
          </v-icon>
          Archive
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Site } from '@/models/Site'

@Component({

})
export default class SiteArchiveDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly siteToArchive!: Site

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasSiteToArchive () {
    return this.siteToArchive !== null
  }
}
</script>

<style scoped>

</style>
