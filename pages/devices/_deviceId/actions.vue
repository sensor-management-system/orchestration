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
      <v-timeline dense>
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
          <template v-if="action.isDeviceMountAction">
            <v-card>
              <v-card-subtitle class="pb-0">
                {{ action.beginDate | toUtcDate }}
              </v-card-subtitle>
              <v-card-title class="pt-0">
                Mounted on {{ action.configurationName }}
              </v-card-title>
              <v-card-subtitle>
                <v-row
                  no-gutters
                >
                  <v-col
                    cols="11"
                  >
                    {{ action.contact.toString() }}
                  </v-col>
                  <v-col
                    align-self="end"
                    class="text-right"
                  >
                    <v-btn
                      icon
                      @click.stop.prevent="showActionItem(action.id)"
                    >
                      <v-icon>{{ isActionItemShown(action.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-subtitle>
              <v-expand-transition>
                <v-card-text
                  v-show="isActionItemShown(action.id)"
                  class="text--primary"
                >
                  <label>Parent platform</label>{{ action.parentPlatformName }}
                  <v-row dense>
                    <v-col cols="12" md="4">
                      <label>Offset x</label>{{ action.offsetX }} m
                    </v-col>
                    <v-col cols="12" md="4">
                      <label>Offset y</label>{{ action.offsetY }} m
                    </v-col>
                    <v-col cols="12" md="4">
                      <label>Offset z</label>{{ action.offsetZ }} m
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-expand-transition>
            </v-card>
          </template>
          <template v-if="action.isDeviceUnmountAction">
            <v-card>
              <v-card-subtitle class="pb-0">
                {{ action.endDate | toUtcDate }}
              </v-card-subtitle>
              <v-card-title class="pt-0">
                Unmounted on {{ action.configurationName }}
              </v-card-title>
              <v-card-subtitle>
                <v-row
                  no-gutters
                >
                  <v-col
                    cols="11"
                  >
                    {{ action.contact.toString() }}
                  </v-col>
                  <v-col
                    align-self="end"
                    class="text-right"
                  >
                    <v-btn
                      icon
                      @click.stop.prevent="showActionItem(action.id)"
                    >
                      <v-icon>{{ isActionItemShown(action.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-subtitle>
              <v-expand-transition>
                <v-card-text
                  v-show="isActionItemShown(action.id)"
                  class="text--primary"
                />
              </v-expand-transition>
            </v-card>
          </template>
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

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DateComparator, isDateCompareable } from '@/modelUtils/Compareables'

const toUtcDate = (dt: DateTime) => {
  return dt.toUTC().toFormat('yyyy-MM-dd TT')
}

interface IColoredAction {
  getColor (): string
}

class DeviceMountAction {
  public id: string
  public configurationName: string
  public parentPlatformName: string
  public offsetX: number
  public offsetY: number
  public offsetZ: number
  public beginDate: DateTime
  public description: string
  public contact: Contact
  public attachments: Attachment[]
  constructor (
    id: string,
    configurationName: string,
    parentPlatformName: string,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    beginDate: DateTime,
    description: string,
    contact: Contact,
    attachments: Attachment[]
  ) {
    this.id = id
    this.configurationName = configurationName
    this.parentPlatformName = parentPlatformName
    this.offsetX = offsetX
    this.offsetY = offsetY
    this.offsetZ = offsetZ
    this.beginDate = beginDate
    this.description = description
    this.contact = contact
    this.attachments = attachments
  }

  getId (): string {
    return 'mount-' + this.id
  }

  get isDeviceMountAction (): boolean {
    return true
  }

  getColor (): string {
    return 'green'
  }
}

class DeviceUnmountAction implements IActionCommonDetails, IColoredAction {
  public id: string
  public configurationName: string
  public endDate: DateTime
  public description: string
  public contact: Contact
  public attachments: Attachment[]
  constructor (
    id: string,
    configurationName: string,
    endDate: DateTime,
    description: string,
    contact: Contact,
    attachments: Attachment[]
  ) {
    this.id = id
    this.configurationName = configurationName
    this.endDate = endDate
    this.description = description
    this.contact = contact
    this.attachments = attachments
  }

  getId (): string {
    return 'unmount-' + this.id
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
    SoftwareUpdateActionCard
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
    const contact1 = Contact.createFromObject({
      id: 'X1',
      givenName: 'Tech',
      familyName: 'Niker',
      email: 'tech.niker@gfz-potsdam.de',
      website: ''
    })
    const devProp1 = new DeviceProperty()
    devProp1.label = 'Wind direction'
    const devProp2 = new DeviceProperty()
    devProp2.label = 'Wind speed'
    const deviceMountAction1 = new DeviceMountAction(
      'X4',
      'Measurement ABC',
      'Station ABC',
      0,
      0,
      2,
      DateTime.fromISO('2021-03-30T12:00:00Z'),
      'Mounted Measurement ABC',
      contact1,
      []
    )
    const deviceUnmountAction1 = new DeviceUnmountAction(
      'X5',
      'Measurement ABC',
      DateTime.fromISO('2022-03-30T12:00:00Z'),
      'Unmounted Measurement ABC',
      contact1,
      []
    )
    this.actions = [
      deviceMountAction1,
      deviceUnmountAction1
    ]
    await Promise.all([
      this.fetchGenericActions(),
      this.fetchSoftwareUpdateActions(),
      this.fetchDeviceCalibrationActions()
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
