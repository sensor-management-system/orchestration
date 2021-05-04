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
        v-if="isLoggedIn && !(isAddActionPage)"
        color="primary"
        small
        :disabled="isEditActionPage"
        :to="'/devices/' + deviceId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
    <template v-if="isAddActionPage">
      <NuxtChild />
    </template>
    <template v-else>
      <v-timeline dense>
        <v-timeline-item
          v-for="action in actions"
          :key="action.id"
          :color="getActionColor(action)"
          class="mb-4"
          small
        >
          <template v-if="action.isGenericDeviceAction">
            <v-card>
              <v-card-subtitle class="pb-0">
                {{ action.beginDate | toUtcDate }} - {{ action.endDate | toUtcDate }}
              </v-card-subtitle>
              <v-card-title class="py-0">
                <v-row
                  no-gutters
                >
                  <v-col
                    cols="11"
                  >
                    {{ action.actionTypeName }}
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
              </v-card-title>
              <v-expand-transition>
                <div
                  v-show="isActionItemShown(action.id)"
                >
                  <v-card-subtitle
                    class="pt-0"
                  >
                    {{ action.contact.toString() }}
                  </v-card-subtitle>
                  <v-card-text
                    class="grey lighten-5 text--primary pt-2"
                  >
                    <label>Description</label>
                    {{ action.description }}
                  </v-card-text>
                </div>
              </v-expand-transition>
            </v-card>
          </template>
          <template v-if="action.isUpdateAction">
            <v-card>
              <v-card-subtitle class="pb-0">
                {{ action.updateDate | toUtcDate }}
              </v-card-subtitle>
              <v-card-title class="pt-0">
                {{ action.softwareTypeName }} update
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
                  <v-row dense>
                    <v-col cols="12" md="4">
                      <label>
                        Version
                      </label>
                      {{ action.version }}
                    </v-col>
                    <v-col cols="12" md="4">
                      <label>
                        Repository
                      </label>
                      {{ action.repositoryUrl }}
                    </v-col>
                  </v-row>
                  <v-row dense>
                    <v-col>
                      <label>Description</label>
                      {{ action.description }}
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-expand-transition>
            </v-card>
          </template>
          <template v-if="action.isDeviceCalibrationAction">
            <v-card>
              <v-card-subtitle class="pb-0">
                {{ action.currentCalibrationDate | toUtcDate }}
              </v-card-subtitle>
              <v-card-title class="pt-0">
                Device calibration
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
                  <v-row dense>
                    <v-col cols="12" md="4">
                      <label>Formula</label> {{ action.formula }}
                    </v-col>
                    <v-col cols="12" md="4">
                      <label>value</label> {{ action.value }}
                    </v-col>
                    <v-col cols="12" md="4">
                      <label>
                        Next calibration date
                      </label>
                      {{ action.nextCalibrationDate | toUtcDate }}
                    </v-col>
                  </v-row>
                  <label>Measured quantities</label>
                  <ul>
                    <li v-for="deviceProperty in action.deviceProperties" :key="deviceProperty.id">
                      {{ deviceProperty.label }}
                    </li>
                  </ul>
                  <label>Description</label>
                  {{ action.description }}
                </v-card-text>
              </v-expand-transition>
            </v-card>
          </template>
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
    </template>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IAction } from '@/models/Action'
import { GenericDeviceAction } from '@/models/GenericDeviceAction'

const toUtcDate = (dt: DateTime) => {
  return dt.toUTC().toFormat('yyyy-MM-dd TT')
}

class DeviceSoftwareUpdateAction implements IAction {
  private id: string
  private softwareTypeName: string
  private softwareTypeUri: string
  private updateDate: DateTime
  private version: string
  private repositoryUrl: string
  private description: string
  private contact: Contact
  constructor (
    id: string,
    softwareTypeName: string,
    softwareTypeUri: string,
    updateDate: DateTime,
    version: string,
    repositoryUrl: string,
    description: string,
    contact: Contact
  ) {
    this.id = id
    this.softwareTypeName = softwareTypeName
    this.softwareTypeUri = softwareTypeUri
    this.updateDate = updateDate
    this.version = version
    this.repositoryUrl = repositoryUrl
    this.description = description
    this.contact = contact
  }

  getId (): string {
    return 'software-' + this.id
  }

  get isUpdateAction (): boolean {
    return true
  }
}

class DeviceCalibrationAction implements IAction {
  private id: string
  private description: string
  private currentCalibrationDate: DateTime
  private nextCalibrationDate: DateTime
  private formula: string
  private value: string
  private deviceProperties: DeviceProperty[]
  private contact: Contact
  constructor (
    id: string,
    description: string,
    currentCalibrationDate: DateTime,
    nextCalibrationDate: DateTime,
    formula: string,
    value: string,
    deviceProperties: DeviceProperty[],
    contact: Contact
  ) {
    this.id = id
    this.description = description
    this.currentCalibrationDate = currentCalibrationDate
    this.nextCalibrationDate = nextCalibrationDate
    this.formula = formula
    this.value = value
    this.deviceProperties = deviceProperties
    this.contact = contact
  }

  getId (): string {
    return 'calibration-' + this.id
  }

  get isDeviceCalibrationAction (): boolean {
    return true
  }
}

class DeviceMountAction {
  private id: string
  private configurationName: string
  private parentPlatformName: string
  private offsetX: number
  private offsetY: number
  private offsetZ: number
  private beginDate: DateTime
  private contact: Contact
  constructor (
    id: string,
    configurationName: string,
    parentPlatformName: string,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    beginDate: DateTime,
    contact: Contact
  ) {
    this.id = id
    this.configurationName = configurationName
    this.parentPlatformName = parentPlatformName
    this.offsetX = offsetX
    this.offsetY = offsetY
    this.offsetZ = offsetZ
    this.beginDate = beginDate
    this.contact = contact
  }

  getId (): string {
    return 'mount-' + this.id
  }

  get isDeviceMountAction (): boolean {
    return true
  }
}

class DeviceUnmountAction implements IAction {
  private id: string
  private configurationName: string
  private endDate: DateTime
  private contact: Contact
  constructor (
    id: string,
    configurationName: string,
    endDate: DateTime,
    contact: Contact
  ) {
    this.id = id
    this.configurationName = configurationName
    this.endDate = endDate
    this.contact = contact
  }

  getId (): string {
    return 'unmount-' + this.id
  }

  get isDeviceUnmountAction (): boolean {
    return true
  }
}

@Component({
  components: {
    ProgressIndicator
  },
  filters: {
    toUtcDate
  }
})
export default class DeviceActionsPage extends Vue {
  private isLoading: boolean = false
  private isSaving: boolean = false

  private actions: IAction[] = []
  private searchResultItemsShown: { [id: string]: boolean } = {}

  async fetch () {
    const contact1 = Contact.createFromObject({
      id: '1',
      givenName: 'Tech',
      familyName: 'Niker',
      email: 'tech.niker@gfz-potsdam.de',
      website: ''
    })
    const contact2 = Contact.createFromObject({
      id: '2',
      givenName: 'Cam',
      familyName: 'Paign',
      email: 'cam.paign@gfz-potsdam.de',
      website: ''
    })
    const deviceSoftwareUpdateAction = new DeviceSoftwareUpdateAction(
      '2',
      'Firmware',
      'softwaretypes/firmware',
      DateTime.fromISO('2021-03-30T08:10:00Z'),
      '1.0.34',
      'git.gfz-potsdam.de/sensor-management-system/firmware',
      'The 1.0.34 firmware version for the device',
      contact1
    )
    const devProp1 = new DeviceProperty()
    devProp1.label = 'Wind direction'
    const devProp2 = new DeviceProperty()
    devProp2.label = 'Wind speed'
    const deviceCalibrationAction1 = new DeviceCalibrationAction(
      '3',
      'Calibration of the device for usage on the campaign',
      DateTime.fromISO('2021-03-30T08:12:00Z'),
      DateTime.fromISO('2021-04-30T12:00:00Z'),
      'f(x) = x',
      '100',
      [devProp1, devProp2],
      contact2
    )
    const deviceMountAction1 = new DeviceMountAction(
      '4',
      'Measurement ABC',
      'Station ABC',
      0,
      0,
      2,
      DateTime.fromISO('2021-03-30T12:00:00Z'),
      contact1
    )
    const deviceUnmountAction1 = new DeviceUnmountAction(
      '5',
      'Measurement ABC',
      DateTime.fromISO('2022-03-30T12:00:00Z'),
      contact1
    )
    this.actions = [
      deviceSoftwareUpdateAction,
      deviceCalibrationAction1,
      deviceMountAction1,
      deviceUnmountAction1
    ]
    await Promise.all([this.fetchGenericDeviceActions()])
  }

  async fetchGenericDeviceActions (): Promise<void> {
    const actions: GenericDeviceAction[] = await this.$api.devices.findRelatedGenericDeviceActions(this.deviceId)
    actions.forEach((action: GenericDeviceAction) => this.actions.push(action))
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
    const editUrl = '^\/devices\/' + this.deviceId + '\/actions\/([0-9]+)\/edit$'
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

  getActionColor (action: IAction) {
    switch (true) {
      case action instanceof GenericDeviceAction:
        return 'blue'
      case action instanceof DeviceSoftwareUpdateAction:
        return 'yellow'
      case action instanceof DeviceCalibrationAction:
        return 'brown'
      case action instanceof DeviceMountAction:
        return 'green'
      case action instanceof DeviceUnmountAction:
        return 'red'
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
