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
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn && !(isAddActionPage || isEditActionPage)"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
    <template
      v-if="isAddActionPage"
    >
      <NuxtChild
        @input="$fetch"
        @showsave="showsave"
      />
    </template>
    <template
      v-else-if="isEditActionPage"
    >
      <NuxtChild
        @input="$fetch"
        @showload="showload"
        @showsave="showsave"
      />
    </template>
    <template v-else>
      <div v-if="actions.length == 0">
        <v-card flat>
          <v-card-text>
            <p class="text-center">
              There are no actions for this device.
            </p>
          </v-card-text>
        </v-card>
      </div>
      <v-timeline
        v-else
        dense
      >
        <v-timeline-item
          v-for="(action, index) in actions"
          :key="getActionTypeIterationKey(action)"
          :color="action.getColor()"
          class="mb-4"
          small
        >
          <GenericActionCard
            v-if="action.isGenericAction"
            v-model="actions[index]"
          >
            <template
              v-if="isLoggedIn"
              #menu
            >
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-item
                    :disabled="!isLoggedIn"
                    dense
                    @click="showDeleteDialog(action)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isLoggedIn ? 'red--text' : 'grey--text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isLoggedIn ? 'red' : 'grey'"
                        >
                          mdi-delete
                        </v-icon>
                        Delete
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
            <template #actions>
              <v-btn
                v-if="isLoggedIn"
                :to="'/devices/' + deviceId + '/actions/generic-device-actions/' + action.id + '/edit'"
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
            v-model="actions[index]"
          >
            <template
              v-if="isLoggedIn"
              #menu
            >
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-item
                    :disabled="!isLoggedIn"
                    dense
                    @click="showDeleteDialog(action)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isLoggedIn ? 'red--text' : 'grey--text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isLoggedIn ? 'red' : 'grey'"
                        >
                          mdi-delete
                        </v-icon>
                        Delete
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
            <template #actions>
              <v-btn
                v-if="isLoggedIn"
                :to="'/devices/' + deviceId + '/actions/software-update-actions/' + action.id + '/edit'"
                color="primary"
                text
                @click.stop.prevent
              >
                Edit
              </v-btn>
            </template>
          </SoftwareUpdateActionCard>

          <DeviceCalibrationActionCard
            v-if="action.isDeviceCalibrationAction"
            v-model="actions[index]"
          >
            <template
              v-if="isLoggedIn"
              #menu
            >
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-item
                    :disabled="!isLoggedIn"
                    dense
                    @click="showDeleteDialog(action)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isLoggedIn ? 'red--text' : 'grey--text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isLoggedIn ? 'red' : 'grey'"
                        >
                          mdi-delete
                        </v-icon>
                        Delete
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
            <template #actions>
              <v-btn
                v-if="isLoggedIn"
                :to="'/devices/' + deviceId + '/actions/device-calibration-actions/' + action.id + '/edit'"
                color="primary"
                text
                @click.stop.prevent
              >
                Edit
              </v-btn>
            </template>
          </DeviceCalibrationActionCard>
          <DeviceMountActionCard
            v-if="action.isDeviceMountAction"
            v-model="action.inner"
          />
          <DeviceUnmountActionCard
            v-if="action.isDeviceUnmountAction"
            v-model="action.inner"
          />
        </v-timeline-item>
      </v-timeline>
      <v-dialog
        v-model="hasActionToDelete"
        max-width="290"
        @click:outside="hideDeleteDialog"
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
              @click="hideDeleteDialog()"
            >
              No
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              @click="deleteAction()"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import DeviceCalibrationActionCard from '@/components/DeviceCalibrationActionCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import GenericActionCard from '@/components/GenericActionCard.vue'
import SoftwareUpdateActionCard from '@/components/SoftwareUpdateActionCard.vue'
import DeviceMountActionCard from '@/components/DeviceMountActionCard.vue'
import DeviceUnmountActionCard from '@/components/DeviceUnmountActionCard.vue'

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/views/devices/actions/DeviceUnmountAction'

import { DateComparator, isDateCompareable } from '@/modelUtils/Compareables'

const toUtcDate = (dt: DateTime) => {
  return dt.toUTC().toFormat('yyyy-MM-dd TT')
}

interface IColoredAction {
  getColor (): string
}

class DeviceMountActionWrapper {
  inner: DeviceMountAction

  constructor (inner: DeviceMountAction) {
    this.inner = inner
  }

  get id (): string {
    return this.inner.basicData.id
  }

  get description (): string {
    return this.inner.basicData.description
  }

  get contact (): Contact {
    return Contact.createFromObject(this.inner.contact)
  }

  get attachments (): Attachment[] {
    return []
  }

  get isDeviceMountAction (): boolean {
    return true
  }

  getColor (): string {
    return 'green'
  }
}

class DeviceUnmountActionWrapper implements IActionCommonDetails, IColoredAction {
  inner: DeviceUnmountAction

  constructor (inner: DeviceUnmountAction) {
    this.inner = inner
  }

  get id (): string {
    return this.inner.basicData.id
  }

  get description (): string {
    return this.inner.basicData.description
  }

  get contact (): Contact {
    return Contact.createFromObject(this.inner.contact)
  }

  get attachments (): Attachment[] {
    return []
  }

  get isDeviceUnmountAction (): boolean {
    return true
  }

  getColor (): string {
    return 'red'
  }
}

/**
 * extend the original interfaces by adding the getColor() method
 */
declare module '@/models/GenericAction' {
  interface GenericAction extends IColoredAction {
  }
}
GenericAction.prototype.getColor = (): string => 'blue'

declare module '@/models/SoftwareUpdateAction' {
  interface SoftwareUpdateAction extends IColoredAction {
  }
}
SoftwareUpdateAction.prototype.getColor = (): string => 'yellow'

declare module '@/models/DeviceCalibrationAction' {
  interface DeviceCalibrationAction extends IColoredAction {
  }
}
DeviceCalibrationAction.prototype.getColor = (): string => 'brown'

type ActionDeleteMethod = (id: string) => Promise<void>

@Component({
  components: {
    DeviceCalibrationActionCard,
    ProgressIndicator,
    GenericActionCard,
    SoftwareUpdateActionCard,
    DeviceMountActionCard,
    DeviceUnmountActionCard
  },
  filters: {
    toUtcDate
  }
})
export default class DeviceActionsPage extends Vue {
  private isLoading: boolean = false
  private isSaving: boolean = false

  private actions: IActionCommonDetails[] = []
  private searchResultItemsShown: { [id: string]: boolean } = {}

  private actionToDelete: IActionCommonDetails | null = null

  async fetch () {
    this.actions = []
    await Promise.all([
      this.fetchGenericActions(),
      this.fetchSoftwareUpdateActions(),
      this.fetchDeviceCalibrationActions(),
      this.fetchMountActions(),
      this.fetchUnmountActions()
    ])

    // sort the actions
    const comparator = new DateComparator()
    this.actions.sort((i: IActionCommonDetails, j: IActionCommonDetails): number => {
      if (isDateCompareable(i) && isDateCompareable(j)) {
        // multiply result with -1 to get descending order
        return comparator.compare(i, j) * -1
      }
      if (isDateCompareable(i)) {
        return -1
      }
      if (isDateCompareable(j)) {
        return 1
      }
      return 0
    })
  }

  async fetchGenericActions (): Promise<void> {
    const actions: GenericAction[] = await this.$api.devices.findRelatedGenericActions(this.deviceId)
    actions.forEach((action: GenericAction) => this.actions.push(action))
  }

  async fetchSoftwareUpdateActions (): Promise<void> {
    const actions: SoftwareUpdateAction[] = await this.$api.devices.findRelatedSoftwareUpdateActions(this.deviceId)
    actions.forEach((action: SoftwareUpdateAction) => this.actions.push(action))
  }

  async fetchMountActions (): Promise<void> {
    const actions: DeviceMountAction[] = await this.$api.devices.findRelatedMountActions(this.deviceId)
    actions.forEach((action: DeviceMountAction) => this.actions.push(new DeviceMountActionWrapper(action)))
  }

  async fetchUnmountActions (): Promise<void> {
    const actions: DeviceUnmountAction[] = await this.$api.devices.findRelatedUnmountActions(this.deviceId)
    actions.forEach((action: DeviceUnmountAction) => this.actions.push(new DeviceUnmountActionWrapper(action)))
  }

  async fetchDeviceCalibrationActions (): Promise<void> {
    const actions: DeviceCalibrationAction[] = await this.$api.devices.findRelatedCalibrationActions(this.deviceId)
    actions.forEach((action: DeviceCalibrationAction) => this.actions.push(action))
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  showActionItem (id: string) {
    const show = !!this.searchResultItemsShown[id]
    Vue.set(this.searchResultItemsShown, id, !show)
  }

  isActionItemShown (id: string): boolean {
    return this.searchResultItemsShown[id]
  }

  unsetActionItemsShown (): void {
    this.searchResultItemsShown = {}
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isAddActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/devices\/' + this.deviceId + '\/actions\/new$'
    return !!this.$route.path.match(addUrl)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string | undefined {
    return this.$route.params.actionId
  }

  get hasActionToDelete (): boolean {
    return this.actionToDelete !== null
  }

  showsave (isSaving: boolean) {
    this.isSaving = isSaving
  }

  showload (isLoading: boolean) {
    this.isLoading = isLoading
  }

  showDeleteDialog (action: IActionCommonDetails) {
    this.actionToDelete = action
  }

  hideDeleteDialog (): void {
    this.actionToDelete = null
  }

  /**
   * deletes the action and closes the delete dialog
   *
   * calls {@link DeviceActionsPage#deleteActionAndCloseDialog} with the appropriate API method
   *
   * @throws {TypeError} - throws an Error if the type of action is not supported
   */
  deleteAction (): void {
    if (!this.actionToDelete) {
      return
    }
    if (!this.actionToDelete.id) {
      return
    }
    switch (true) {
      case 'isGenericAction' in this.actionToDelete:
        this.deleteActionAndCloseDialog(this.actionToDelete.id, this.$api.genericDeviceActions.deleteById.bind(this.$api.genericDeviceActions))
        break
      case 'isSoftwareUpdateAction' in this.actionToDelete:
        this.deleteActionAndCloseDialog(this.actionToDelete.id, this.$api.deviceSoftwareUpdateActions.deleteById.bind(this.$api.deviceSoftwareUpdateActions))
        break
      case 'isDeviceCalibrationAction' in this.actionToDelete:
        this.deleteActionAndCloseDialog(this.actionToDelete.id, this.$api.deviceCalibrationActions.deleteById.bind(this.$api.deviceCalibrationActions))
        break
      default:
        throw new TypeError('deleting the action type is not supported.')
    }
  }

  /**
   * deletes the action and closes the delete dialog
   *
   * @param {string} id - the id of the action to delete
   * @param {ActionDeleteMethod} actionDeleteMethod - an API method to delete an action
   */
  deleteActionAndCloseDialog (id: string, actionDeleteMethod: ActionDeleteMethod): void {
    this.isSaving = true
    actionDeleteMethod(id).then(() => {
      this.$fetch()
      this.$store.commit('snackbar/setSuccess', 'Action deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Action could not be deleted')
    }).finally(() => {
      this.hideDeleteDialog()
      this.isSaving = false
    })
  }

  getActionType (action: IActionCommonDetails): string {
    switch (true) {
      case 'isGenericAction' in action:
        return 'generic-action'
      case 'isSoftwareUpdateAction' in action:
        return 'software-update-action'
      case 'isDeviceCalibrationAction' in action:
        return 'device-calibration-action'
      case 'isDeviceMountAction' in action:
        return 'device-mount-action'
      case 'isDeviceUnmountAction' in action:
        return 'device-unmount-action'
      default:
        return 'unknown-action'
    }
  }

  getActionTypeIterationKey (action: IActionCommonDetails): string {
    return this.getActionType(action) + '-' + action.id
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
