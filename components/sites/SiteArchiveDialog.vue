<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    max-width="500"
    @click:outside="$emit('cancel-archiving')"
  >
    <v-card v-if="hasSiteToArchive">
      <v-card-title class="headline">
        Archive site
      </v-card-title>
      <v-card-text>
        <p>Do you really want to archive the site <em>{{ siteToArchive.label }}</em>?</p>
        <p>
          Achived sites can no longer be edited or used until they are restored.
        </p>
        <p>
          They are not included in the site search by default.
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
