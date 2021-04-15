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
    <v-card class="pa-2 mb-3">
      <v-row>
        <v-col>
          <v-select
            v-model="chosenKindOfAction"
            :items="kindOfActionChoices"
            :item-value="(x) => x.id"
            :item-text="(x) => x.label"
            clearable
            label="Kind of action"
          />
        </v-col>
      </v-row>
    </v-card>
    <v-card v-if="deviceCalibrationChosen" class="pa-2">
      <v-row>
        <v-col md="6">
          <v-text-field label="formula" />
        </v-col>
        <v-col>
          <v-text-field label="value" />
        </v-col>
      </v-row>
      <v-form
        ref="datesForm"
        v-model="datesAreValid"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12" md="3">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getStartDate()"
                  :rules="[rules.startDate]"
                  v-bind="attrs"
                  label="Current calibration date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setStartDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getStartDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setStartDateAndValidate"
              />
            </v-menu>
          </v-col>
          <v-col cols="12" md="3">
            <v-menu
              v-model="endDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getEndDate()"
                  :rules="[rules.endDate]"
                  v-bind="attrs"
                  label="Next calibration date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setEndDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getEndDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setEndDateAndValidate"
              />
            </v-menu>
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Affacted measured quantities</p>
            <v-checkbox
              v-for="ms in measuredQuantities"
              :key="ms.id"
              :label="ms.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-select :items="contacts" label="Contact" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            label="Description"
            rows="3"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Attachments</p>
            <v-checkbox
              v-for="attachment in attachments"
              :key="attachment.id"
              :label="attachment.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            ref="cancelButton"
            text
            small
            :to="'/devices/' + deviceId + '/actions'"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="green"
            small
          >
            Add
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else-if="softwareUpdateChosen" class="pa-2">
      <v-row>
        <v-col md="6">
          <v-select :items="softwareTypes" :item-text="(x) => x.name" label="Software type" />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="3">
          <v-text-field label="Version" placeholder="1.2.3" />
        </v-col>
        <v-col md="9">
          <v-text-field label="Repository URL" placeholder="https://github.com/" />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-select :items="contacts" label="Contact" />
        </v-col>
      </v-row>
      <v-form
        ref="datesForm"
        v-model="datesAreValid"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12" md="3">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getStartDate()"
                  :rules="[rules.startDate]"
                  v-bind="attrs"
                  label="Date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setStartDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getStartDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setStartDateAndValidate"
              />
            </v-menu>
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            label="Description"
            rows="3"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Attachments</p>
            <v-checkbox
              v-for="attachment in attachments"
              :key="attachment.id"
              :label="attachment.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            ref="cancelButton"
            text
            small
            :to="'/devices/' + deviceId + '/actions'"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="green"
            small
          >
            Add
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else-if="mountChosen" class="pa-2">
      <v-row>
        <v-col md="9">
          <v-select :items="configurations" :item-text="(x) => x.label" label="Configuration" />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="9">
          <v-select :items="platforms" :item-text="(x) => x.shortName" label="Parent platform" />
        </v-col>
      </v-row>
      <v-row>
        <v-col
          cols="12"
          md="2"
        >
          <v-text-field
            label="Offset (x)"
            type="number"
            @wheel.prevent
          />
        </v-col>
        <v-col
          cols="12"
          md="2"
        >
          <v-text-field
            label="Offset (y)"
            type="number"
            @wheel.prevent
          />
        </v-col>
        <v-col
          cols="12"
          md="2"
        >
          <v-text-field
            label="Offset (z)"
            type="number"
            @wheel.prevent
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-select :items="contacts" label="Contact" />
        </v-col>
      </v-row>
      <v-form
        ref="datesForm"
        v-model="datesAreValid"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12" md="3">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getStartDate()"
                  :rules="[rules.startDate]"
                  v-bind="attrs"
                  label="Start date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setStartDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getStartDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setStartDateAndValidate"
              />
            </v-menu>
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            label="Description"
            rows="3"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Attachments</p>
            <v-checkbox
              v-for="attachment in attachments"
              :key="attachment.id"
              :label="attachment.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            ref="cancelButton"
            text
            small
            :to="'/devices/' + deviceId + '/actions'"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="green"
            small
          >
            Add
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else-if="unmountChosen" class="pa-2">
      <v-row>
        <v-col md="9">
          <v-select :items="configurations" :item-text="(x) => x.label" label="Configuration" />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-select :items="contacts" label="Contact" />
        </v-col>
      </v-row>
      <v-form
        ref="datesForm"
        v-model="datesAreValid"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12" md="3">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getEndDate()"
                  :rules="[rules.startDate]"
                  v-bind="attrs"
                  label="End date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setEndDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getEndDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setStartDateAndValidate"
              />
            </v-menu>
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            label="Description"
            rows="3"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Attachments</p>
            <v-checkbox
              v-for="attachment in attachments"
              :key="attachment.id"
              :label="attachment.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            ref="cancelButton"
            text
            small
            :to="'/devices/' + deviceId + '/actions'"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="green"
            small
          >
            Add
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else-if="otherChosen" class="pa-2">
      <v-row>
        <v-col md="6">
          <v-select :items="deviceActionTypes" :item-text="(x) => x.name" label="Action type" />
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-select :items="contacts" label="Contact" />
        </v-col>
      </v-row>
      <v-form
        ref="datesForm"
        v-model="datesAreValid"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12" md="3">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getStartDate()"
                  :rules="[rules.startDate]"
                  v-bind="attrs"
                  label="Start date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setStartDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getStartDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setStartDateAndValidate"
              />
            </v-menu>
          </v-col>
          <v-col cols="12" md="3">
            <v-menu
              v-model="endDateMenu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="getEndDate()"
                  :rules="[rules.endDate]"
                  v-bind="attrs"
                  label="End date"
                  clearable
                  prepend-icon="mdi-calendar-range"
                  readonly
                  v-on="on"
                  @click:clear="setEndDateAndValidate(null)"
                />
              </template>
              <v-date-picker
                :value="getEndDate()"
                first-day-of-week="1"
                :show-week="true"
                @input="setEndDateAndValidate"
              />
            </v-menu>
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            label="Description"
            rows="3"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <div v-if="attachments.length > 0">
            <p>Attachments</p>
            <v-checkbox
              v-for="attachment in attachments"
              :key="attachment.id"
              :label="attachment.label"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            ref="cancelButton"
            text
            small
            :to="'/devices/' + deviceId + '/actions'"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="green"
            small
          >
            Add
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-else class="pa-2" flat>
      <v-card-text style="text--grey text--center">
        <i><small>Please choose the kind of action.</small></i>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Configuration } from '@/models/Configuration'
import { Platform } from '@/models/Platform'

import { dateToString, stringToDate } from '@/utils/dateHelper'

const ID_DEVICE_CALIBRATION = 1
const ID_SOFTWARE_UPDATE = 2
const ID_MOUNT_DEVICE = 3
const ID_UNMOUNT_DEVICE = 4
const ID_OTHER = 5

interface IDeviceActionType {
  id: string,
  uri: string
  name: string
}

@Component
export default class ActionAddPage extends Vue {
  private rules: Object = {
    startDate: this.validateInputForStartDate,
    endDate: this.validateInputForEndDate
  }

  private datesAreValid = true

  private kindOfActionChoices = [
    { id: ID_DEVICE_CALIBRATION, label: 'Device calibration' },
    { id: ID_SOFTWARE_UPDATE, label: 'Software update' },
    { id: ID_MOUNT_DEVICE, label: 'Mount' },
    { id: ID_UNMOUNT_DEVICE, label: 'Unmount' },
    { id: ID_OTHER, label: 'Other...' }
  ]

  private contacts = [
    Contact.createWithIdEMailAndNames('1', 'max.mustermann@mail.com', 'Max', 'Mustermann', ''),
    Contact.createWithIdEMailAndNames('1', 'mix.mustermann@mail.com', 'Mix', 'Mustermann', ''),
    Contact.createWithIdEMailAndNames('1', 'mox.mustermann@mail.com', 'Mox', 'Mustermann', '')
  ]

  private attachments = [
    Attachment.createFromObject({
      id: '1', url: 'http://www.gfz-potsdam.de', label: 'GFZ Homepage'
    }),
    Attachment.createFromObject({
      id: '2', url: 'http://www.ufz.de', label: 'UFZ Homepage'
    })
  ]

  createDeviceProperty (id: string, label: string) {
    const result = new DeviceProperty()
    result.id = id
    result.label = label
    return result
  }

  createConfiguration (id: string, label: string) {
    const result = new Configuration()
    result.id = id
    result.label = label
    return result
  }

  createPlatform (id: string, shortName: string) {
    const result = new Platform()
    result.id = id
    result.shortName = shortName
    return result
  }

  private measuredQuantities = [
    this.createDeviceProperty('1', 'Air temperature'),
    this.createDeviceProperty('2', 'Wind speed'),
    this.createDeviceProperty('3', 'Wind direction')
  ]

  private platforms = [
    this.createPlatform('1', 'Platform A'),
    this.createPlatform('2', 'Platform B'),
    this.createPlatform('3', 'Platform C')
  ]

  private configurations = [
    this.createConfiguration('1', 'Configuration A'),
    this.createConfiguration('2', 'Configuration B'),
    this.createConfiguration('3', 'Configuration C')
  ]

  private deviceActionTypes = [
    { id: '1', uri: 'actionTypes/device_visit', name: 'Device visit' },
    { id: '2', uri: 'actionTypes/device_maintainance', name: 'Device maintainance' }
  ]

  private softwareTypes = [
    { id: '1', uri: 'softwareTypes/firmware', name: 'Firmware' },
    { id: '2', uri: 'softwareTypes/software', name: 'Software' }
  ]

  private _chosenKindOfAction: number | null = null
  private startDateMenu = false
  private endDateMenu = false

  private startDate: DateTime | null = null
  private endDate: DateTime | null = null

  get chosenKindOfAction () {
    return this.$data._chosenKindOfAction
  }

  set chosenKindOfAction (newValue: number | null) {
    if (this.$data._chosenKindOfAction !== newValue) {
      this.$data._chosenKindOfAction = newValue
      this.resetAllActionSpecificInputs()
    }
  }

  resetAllActionSpecificInputs () {
    this.startDate = null
    this.endDate = null
    this.startDateMenu = false
    this.endDateMenu = false
    // TODO: Once their value is tracked in a slot of this component
    // actionType
    // contact
  }

  get deviceCalibrationChosen () {
    return this.chosenKindOfAction === ID_DEVICE_CALIBRATION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfAction === ID_SOFTWARE_UPDATE
  }

  get mountChosen () {
    return this.chosenKindOfAction === ID_MOUNT_DEVICE
  }

  get unmountChosen () {
    return this.chosenKindOfAction === ID_UNMOUNT_DEVICE
  }

  get otherChosen () {
    return this.chosenKindOfAction === ID_OTHER
  }

  getStartDate (): string {
    return dateToString(this.startDate)
  }

  setStartDate (aDate: string | null) {
    this.startDate = aDate !== null ? stringToDate(aDate) : null
  }

  getEndDate (): string {
    return dateToString(this.endDate)
  }

  setEndDate (aDate: string | null) {
    this.endDate = aDate !== null ? stringToDate(aDate) : null
  }

  setStartDateAndValidate (aDate: string) {
    this.setStartDate(aDate)
    this.startDateMenu = false
    if (this.endDate !== null) {
      this.checkValidationOfDates()
    }
  }

  setEndDateAndValidate (aDate: string | null) {
    this.setEndDate(aDate)
    this.endDateMenu = false
    if (this.startDate !== null) {
      this.checkValidationOfDates()
    }
  }

  checkValidationOfDates () {
    (this.$refs.datesForm as Vue & { validate: () => boolean }).validate()
  }

  validateInputForStartDate (v: string): boolean | string {
    if (v === null || v === '') {
      return true
    }
    if (!this.endDate) {
      return true
    }
    if (stringToDate(v) <= this.endDate) {
      return true
    }
    return 'Start date must not be after end date'
  }

  validateInputForEndDate (v: string): boolean | string {
    if (v === null || v === '') {
      return true
    }
    if (!this.startDate) {
      return true
    }
    if (stringToDate(v) >= this.startDate) {
      return true
    }
    return 'End date must not be before start date'
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }
}
</script>
