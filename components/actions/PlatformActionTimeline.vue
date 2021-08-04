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
  <v-timeline dense>
    <v-timeline-item
      v-for="(action, index) in value"
      :key="getActionTypeIterationKey(action)"
      :color="action | getActionColor"
      class="mb-4"
      small
    >
      <GenericActionCard
        v-if="action.isGenericAction"
        :value="value[index]"
        :delete-callback="getActionApiDispatcherDeleteMethod(action)"
        @delete-success="removeActionFromModel"
        @showdelete="$emit('showdelete', $event)"
      >
        <template #actions>
          <v-btn
            v-if="isLoggedIn"
            :to="'/platforms/' + platformId + '/actions/generic-platform-actions/' + action.id + '/edit'"
            color="primary"
            text
            @click.stop.prevent
          >
            Edit
          </v-btn>
        </template>
      </GenericActionCard>

      <SoftwareUpdateActionCard
        v-if="action.isSoftwareUpdateAction"
        :value="value[index]"
        target="Platform"
        :delete-callback="getActionApiDispatcherDeleteMethod(action)"
        @delete-success="removeActionFromModel"
        @showdelete="$emit('showdelete', $event)"
      >
        <template #actions>
          <v-btn
            v-if="isLoggedIn"
            :to="'/platforms/' + platformId + '/actions/software-update-actions/' + action.id + '/edit'"
            color="primary"
            text
            @click.stop.prevent
          >
            Edit
          </v-btn>
        </template>
      </SoftwareUpdateActionCard>

      <PlatformMountActionCard
        v-if="action.isPlatformMountAction"
        v-model="action.inner"
      />

      <PlatformUnmountActionCard
        v-if="action.isPlatformUnmountAction"
        v-model="action.inner"
      />
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import GenericActionCard from '@/components/actions/GenericActionCard.vue'
import SoftwareUpdateActionCard from '@/components/actions/SoftwareUpdateActionCard.vue'
import PlatformMountActionCard from '@/components/actions/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/actions/PlatformUnmountActionCard.vue'

import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import {
  getActionColor,
  IActionApiDispatcher,
  ActionApiDeleteMethod
} from '@/modelUtils/actionHelpers'

/**
 * A component to display Platform related actions in a timeline
 *
 * The component offers the following properties:
 *
 * * value - an Array of actions
 * * deviceId - the id of the platform the actions belong to
 * * actionApiDispatcher - an object that returns the methods that are required
 * to modifiy the actions (for example via an Api)
 *
 * The component triggers the following events:
 *
 * * input - the Array of actions was altered (for example because of an action
 * that was deleted)
 *
 * @augments Vue
 */
@Component({
  components: {
    GenericActionCard,
    PlatformMountActionCard,
    PlatformUnmountActionCard,
    SoftwareUpdateActionCard
  },
  filters: {
    getActionColor
  }
})
export default class PlatformActionTimeline extends Vue {
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly value!: IActionCommonDetails[]

  @Prop({
    type: String,
    required: true
  })
  readonly platformId!: string

  /**
   * an object that dispatches Api methods to handle actions
   */
  @Prop({
    default: null,
    required: false,
    type: Object
  })
  // @ts-ignore
  readonly actionApiDispatcher!: IActionApiDispatcher | null

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  getActionTypeIterationKey (action: IActionCommonDetails): string {
    return this.getActionType(action) + '-' + action.id
  }

  getActionType (action: IActionCommonDetails): string {
    switch (true) {
      case 'isGenericAction' in action:
        return 'generic-action'
      case 'isSoftwareUpdateAction' in action:
        return 'software-update-action'
      case 'isPlatformMountAction' in action:
        return 'platform-mount-action'
      case 'isPlatformUnmountAction' in action:
        return 'platform-unmount-action'
      default:
        return 'unknown-action'
    }
  }

  /**
   * removes the action from the model and triggers the input event with the
   * updated model
   *
   * @param {IActionCommonDetails} action - the action to remove
   * @fires PlatformActionTimeline#input
   */
  removeActionFromModel (action: IActionCommonDetails) {
    const actions: IActionCommonDetails[] = [...this.value]
    const actionIndex: number = actions.findIndex(someAction => someAction === action)
    if (actionIndex > -1) {
      actions.splice(actionIndex, 1)
    }
    /**
     * fires an input event
     * @event PlatformActionTimeline#input
     * @type {IActionCommonDetails[]}
     */
    this.$emit('input', actions)
  }

  /**
   * returns the Api method to delete the specific action, if available
   *
   * @param {IActionCommonDetails} action - the action to get the delete method for
   * @return {ActionApiDeleteMethod | undefined} an Api method to delete the action
   */
  getActionApiDispatcherDeleteMethod (action: IActionCommonDetails): ActionApiDeleteMethod | undefined {
    if (!this.actionApiDispatcher) {
      return
    }
    return this.actionApiDispatcher.getDeleteMethod(action)
  }
}
</script>
