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
    max-width="290"
    @click:outside="$emit('cancel-deletion')"
  >
    <v-card v-if="hasSiteToDelete">
      <v-card-title class="headline">
        Delete site / lab
      </v-card-title>
      <v-card-text>
        Do you really want to delete the site / lab <em>{{ siteToDelete.label }}</em>?
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="$emit('cancel-deletion')"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          color="error"
          text
          @click="$emit('submit-deletion')"
        >
          <v-icon left>
            mdi-delete
          </v-icon>
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { Site } from '@/models/Site'

@Component
export default class SiteDeleteDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly siteToDelete!: Site

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasSiteToDelete () {
    return this.siteToDelete !== null
  }
}
</script>

<style scoped>

</style>
