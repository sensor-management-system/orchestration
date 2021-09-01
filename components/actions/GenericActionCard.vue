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
          {{ actionDate }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <ActionCardMenu
            v-if="isUserAuthenticated"
            :value="value"
            @delete-menu-item-click="showDeleteDialog = true"
          />
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-title class="pt-0">
      {{ value.actionTypeName }}
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
      <div
        v-show="isVisible(value.id)"
      >
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <label>Description</label>
          {{ value.description }}
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
 * @file provides a component for a Generic Device Actions card
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { GenericAction } from '@/models/GenericAction'

import ActionCardMenu from '@/components/actions/ActionCardMenu.vue'
import ActionDeleteDialog from '@/components/actions/ActionDeleteDialog.vue'

/**
 * A class component for Generic Device Action card
 * @extends Vue
 */
@Component({
  components: {
    ActionCardMenu,
    ActionDeleteDialog
  }
})
// @ts-ignore
export default class GenericActionCard extends Vue {
  private showDetails: boolean = false
  private isShowDeleteDialog: boolean = false
  private _isDeleting: boolean = false

  /**
   * a GenericAction
   */
  @Prop({
    default: () => new GenericAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: GenericAction

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

  @Prop({
    type: Boolean,
    required: true
  })
  readonly isUserAuthenticated!: boolean

  /**
   * whether the card expansion is shown or not
   *
   * @return {boolean} whether the card expansion is shown or not
   */
  isVisible (): boolean {
    return this.showDetails
  }

  /**
   * toggles the shown state of the card expansion
   *
   */
  toggleVisibility (): void {
    this.showDetails = !this.showDetails
  }

  get actionDate ():string {
    let actionDate = dateToDateTimeString(this.value.beginDate)
    if (this.value.endDate) {
      actionDate += ' - ' + dateToDateTimeString(this.value.endDate)
    }
    return actionDate
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
   * @fires GenericActionCard#delete-success
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
       * @event GenericActionCard#delete-success
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
