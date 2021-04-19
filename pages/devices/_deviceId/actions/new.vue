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
            :items="optionsForActionType"
            :item-text="(x) => x.name"
            :item-value="(x) => x"
            clearable
            label="Action Type"
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
          <v-select
            multiple
            clearable
            label="Affected measured quantities"
            :items="measuredQuantities"
            :item-text="(x) => x.label"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col md="5">
          <v-autocomplete v-model="selectedContact" :items="contacts" label="Contact" clearable :item-text="(x) => x.toString()" />
        </v-col>
        <v-col md="1">
          <v-btn v-if="isLoggedIn" @click="selectCurrentUserAsContact">
            {{ labelForSelectMeButton }}
          </v-btn>
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
          <v-select
            v-if="attachments.length > 0"
            multiple
            clearable
            label="Attachments"
            :items="attachments"
            :item-text="(x) => x.label"
          />
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
        <v-col md="5">
          <v-autocomplete v-model="selectedContact" :items="contacts" label="Contact" clearable :item-text="(x) => x.toString()" />
        </v-col>
        <v-col md="1">
          <v-btn v-if="isLoggedIn" @click="selectCurrentUserAsContact">
            {{ labelForSelectMeButton }}
          </v-btn>
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
          <v-select
            v-if="attachments.length > 0"
            multiple
            clearable
            label="Attachments"
            :items="attachments"
            :item-text="(x) => x.label"
          />
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
        <v-col md="5">
          <v-autocomplete v-model="selectedContact" :items="contacts" label="Contact" clearable :item-text="(x) => x.toString()" />
        </v-col>
        <v-col md="1">
          <v-btn v-if="isLoggedIn" @click="selectCurrentUserAsContact">
            {{ labelForSelectMeButton }}
          </v-btn>
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
          <v-select
            v-if="attachments.length > 0"
            multiple
            clearable
            label="Attachments"
            :items="attachments"
            :item-text="(x) => x.label"
          />
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
        <i><small>Please choose the action type.</small></i>
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

type KindOfActionType = 'device_calibration' | 'software_update' | 'generic_device_action'

interface IGenericActionType {
  id: string
  uri: string
  name: string
}

interface IOptionsForActionType {
  id: string
  kind: KindOfActionType
  name: string
}

@Component
export default class ActionAddPage extends Vue {
  private rules: Object = {
    startDate: this.validateInputForStartDate,
    endDate: this.validateInputForEndDate
  }

  private datesAreValid = true

  private optionsForActionType: IOptionsForActionType[] = [
    { id: 'device-calibration', kind: 'device_calibration', name: 'Device calibration' },
    { id: 'software-update', kind: 'software_update', name: 'Software update' },
    { id: 'generic-action-1', kind: 'generic_device_action', /* uri: 'actionTypes/device_visit', */ name: 'Device visit' },
    { id: 'generic-action-2', kind: 'generic_device_action', /* uri: 'actionTypes/device_maintainance', */ name: 'Device maintainance' }
  ]

  private contacts: Contact[] = []
  private selectedContact: Contact | null = null
  private readonly labelForSelectMeButton = 'Select me'

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

  private softwareTypes = [
    { id: '1', uri: 'softwareTypes/firmware', name: 'Firmware' },
    { id: '2', uri: 'softwareTypes/software', name: 'Software' }
  ]

  private _chosenKindOfAction: IOptionsForActionType | null = null
  private startDateMenu = false
  private endDateMenu = false

  private startDate: DateTime | null = null
  private endDate: DateTime | null = null

  mounted () {
    this.$api.contacts.findAll().then((foundContacts) => {
      this.contacts = foundContacts
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    })
  }

  selectCurrentUserAsContact () {
    const currentUserMail = this.$store.getters['oidc/userEmail']
    if (currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === currentUserMail)
      if (userIndex > -1) {
        this.selectedContact = this.contacts[userIndex]
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  get chosenKindOfAction () {
    return this.$data._chosenKindOfAction
  }

  set chosenKindOfAction (newValue: IOptionsForActionType | null) {
    if (this.$data._chosenKindOfAction !== newValue) {
      this.$data._chosenKindOfAction = newValue
      if (this.$data._chosenKindOfAction?.kind !== newValue?.kind) {
        this.resetAllActionSpecificInputs()
      }
    }
  }

  resetAllActionSpecificInputs () {
    this.startDate = null
    this.endDate = null
    this.startDateMenu = false
    this.endDateMenu = false
    this.selectedContact = null
    // TODO: Once their value is tracked in a slot of this component
  }

  get deviceCalibrationChosen () {
    return this.$data._chosenKindOfAction?.kind === 'device_calibration'
  }

  get softwareUpdateChosen () {
    return this.$data._chosenKindOfAction?.kind === 'software_update'
  }

  get otherChosen () {
    return this.$data._chosenKindOfAction?.kind === 'generic_device_action'
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
