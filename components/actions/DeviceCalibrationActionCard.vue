<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
  <v-card>
    <v-card-subtitle class="pb-0">
      <v-row no-gutters>
        <v-col>
          {{ value.currentCalibrationDate | toUtcDate }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <ActionCardMenu
            v-if="isLoggedIn"
            :value="value"
            @delete-menu-item-click="showDeleteDialog = true"
          />
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-title class="pt-0">
      Device calibration
    </v-card-title>
    <v-card-subtitle class="pb-1">
      <v-row
        no-gutters
      >
        <v-col>
          {{ value.contact.toString() }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="actions" />
          <v-btn
            icon
            @click.stop.prevent="toggleVisibility()"
          >
            <v-icon>{{ isVisible() ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-expand-transition>
      <div v-show="isVisible(value.id)">
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <v-row dense>
            <v-col cols="12" md="4">
              <label>
                Formula
              </label>
              {{ value.formula }}
            </v-col>
            <v-col cols="12" md="4">
              <label>
                Value
              </label>
              {{ value.value }}
            </v-col>
            <v-col v-if="value.nextCalibrationDate != null" cols="12" md="4">
              <label>
                Next calibration date
              </label>
              {{ value.nextCalibrationDate | toUtcDate }}
            </v-col>
          </v-row>
          <div v-if="value.measuredQuantities && value.measuredQuantities.length > 0">
            <label>Measured quantities</label>
            <ul>
              <li v-for="measuredQuantity in value.measuredQuantities" :key="measuredQuantity.id">
                {{ measuredQuantity.label }}
              </li>
            </ul>
          </div>
          <div v-if="value.description">
            <label>Description</label>
            {{ value.description }}
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
    <ActionDeleteDialog
      v-model="showDeleteDialog"
      @delete-dialog-button-click="deleteActionAndCloseDialog"
    />
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a device calibration action card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { dateToDateTimeString } from '@/utils/dateHelper'

import ActionCardMenu from '@/components/actions/ActionCardMenu.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'

@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  },
  components: {
    ActionCardMenu,
    ActionDeleteDialog
  }
})
export default class DeviceCalibrationActionCard extends Vue {
  private showDetails: boolean = false
  private isShowDeleteDialog: boolean = false
  private _isDeleting: boolean = false

  @Prop({
    default: () => new DeviceCalibrationAction(),
    required: true,
    type: Object
  })
  readonly value!: DeviceCalibrationAction

  /**
   * a function reference that deletes the action
   */
  @Prop({
    default: () => null,
    required: false,
    type: Function
  })
  // @ts-ignore
  readonly deleteCallback!: (id: string) => Promise<void>

  isVisible (): boolean {
    return this.showDetails
  }

  toggleVisibility (): void {
    this.showDetails = !this.showDetails
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get showDeleteDialog (): boolean {
    return this.isShowDeleteDialog
  }

  set showDeleteDialog (value: boolean) {
    this.isShowDeleteDialog = value
  }

  get isDeleting (): boolean {
    return this.$data._isDeleting
  }

  set isDeleting (value: boolean) {
    this.$data._isDeleting = value
    this.$emit('showdelete', value)
  }

  /**
   * deletes the action and closes the delete dialog
   *
   * @fires DeviceCalibrationActionCard#delete-success
   */
  deleteActionAndCloseDialog (): void {
    if (!this.value.id) {
      return
    }
    if (!this.deleteCallback) {
      return
    }
    this.isDeleting = true
    this.deleteCallback(this.value.id).then(() => {
      this.isDeleting = false
      /**
       * fires an delete-success event
       * @event DeviceCalibrationActionCard#delete-success
       * @type {IActionCommonDetails}
       */
      this.$emit('delete-success', this.value)
      this.$store.commit('snackbar/setSuccess', 'Action deleted')
    }).catch((_error) => {
      this.isDeleting = false
      this.$store.commit('snackbar/setError', 'Action could not be deleted')
    }).finally(() => {
      this.showDeleteDialog = false
    })
  }
}
</script>
