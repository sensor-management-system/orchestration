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
    v-model="show"
    max-width="290"
    @click:outside="show = false"
  >
    <v-card>
      <v-card-title class="headline">
        Delete action
      </v-card-title>
      <v-card-text>
        Do you really want to delete the action?
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="show = false"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          color="error"
          text
          @click="onDeleteButtonClick"
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A dialog component to confirm the deletion of an action.
 *
 * @augments Vue
 */
@Component
export default class ActionDeleteDialog extends Vue {
  /**
   * A boolean indication whether the dialog is shown or not
   */
  @Prop({
    default: false,
    type: Boolean,
    required: true
  })
  readonly value!: boolean

  get show (): boolean {
    return this.value
  }

  set show (value: boolean) {
    /**
     * is triggered when the dialog is closed
     *
     * @event input
     * @property {boolean} value
     */
    this.$emit('input', value)
  }

  onDeleteButtonClick () {
    /**
     * is triggered when the user clicks the delete button
     *
     * @event delete-dialog-button-click
     */
    this.$emit('delete-dialog-button-click')
  }
}
</script>
