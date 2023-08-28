<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
