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
    <v-card
      flat
    >
      <!-- button-tray -->
      <v-card-actions
        v-if="isLoggedIn"
      >
        <v-spacer />
        <v-btn
          ref="cancelButton"
          text
          small
          :to="'/devices/' + deviceId + '/actions'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="deviceCalibrationChosen"
          color="green"
          small
          @click="addDeviceCalibrationAction"
        >
          Add
        </v-btn>
        <v-btn
          v-else-if="softwareUpdateChosen"
          color="green"
          small
          @click="addDeviceSoftwareUpdateAction"
        >
          Add
        </v-btn>
        <v-btn
          v-else-if="otherChosen"
          color="green"
          small
          @click="addGenericDeviceAction"
        >
          Add
        </v-btn>
      </v-card-actions>
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="optionsForActionType"
          :item-text="(x) => x.name"
          :item-value="(x) => x"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
        />
      </v-card-text>
      <!-- deviceCalibration -->
      <v-card-text
        v-if="deviceCalibrationChosen"
      >
        <v-form
          ref="datesForm"
          v-model="datesAreValid"
          @submit.prevent
        >
          <v-row>
            <v-col cols="12" md="6">
              <DatePicker
                v-model="startDate"
                label="Current calibration date"
                :rules="[rules.startDate, rules.currentCalibrationDateNotNull]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <DatePicker
                v-model="endDate"
                label="Next calibration date"
                :rules="[rules.endDate]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col md="6">
              <v-text-field label="Formula" />
            </v-col>
            <v-col>
              <v-text-field label="Value" />
            </v-col>
          </v-row>
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
        </v-form>
      </v-card-text>
      <!-- softwareUpdate -->
      <v-card-text
        v-if="softwareUpdateChosen"
      >
        <v-form
          ref="datesForm"
          v-model="datesAreValid"
          @submit.prevent
        >
          <v-row>
            <v-col cols="12" md="6">
              <DatePicker
                v-model="startDate"
                label="Date"
                :rules="[rules.startDate, rules.updateDateNotNull]"
              />
            </v-col>
          </v-row>
        </v-form>
        <v-form
          ref="softwareTypeForm"
          v-model="softwareTypeIsValid"
          @submit.prevent
        >
          <v-row>
            <v-col cols="12" md="6">
              <v-select :items="softwareTypes" clearable :item-text="(x) => x.name" label="Software type" :rules="[rules.softwareTypeNotNull]" />
            </v-col>
          </v-row>
        </v-form>
        <v-row>
          <v-col cols="12" md="3">
            <v-text-field label="Version" placeholder="1.2.3" />
          </v-col>
          <v-col cols="12" md="9">
            <v-text-field label="Repository URL" placeholder="https://github.com/" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-text
        v-if="otherChosen"
      >
        <v-form
          ref="datesForm"
          v-model="datesAreValid"
          @submit.prevent
        >
          <v-row>
            <v-col cols="12" md="6">
              <DatePicker
                v-model="startDate"
                label="Start date"
                :rules="[rules.startDate, rules.startDateNotNull]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <DatePicker
                v-model="endDate"
                label="End date"
                :rules="[rules.endDate]"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <!-- action type independent -->
      <v-card-text
        v-if="chosenKindOfAction"
      >
        <v-row>
          <v-col cols="12" md="12">
            <v-textarea
              label="Description"
              rows="3"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-form
              ref="contactForm"
              v-model="contactIsValid"
              @submit.prevent
            >
              <v-autocomplete
                v-model="selectedContact"
                :items="contacts"
                label="Contact"
                clearable
                required
                :item-text="(x) => x.toString()"
                :rules="[rules.contactNotNull]"
              />
            </v-form>
          </v-col>
          <v-col cols="12" md="1">
            <v-btn v-if="isLoggedIn" small @click="selectCurrentUserAsContact">
              {{ labelForSelectMeButton }}
            </v-btn>
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
      </v-card-text>
      <!-- button-tray -->
      <v-card-actions
        v-if="isLoggedIn"
      >
        <v-spacer />
        <v-btn
          ref="cancelButton"
          text
          small
          :to="'/devices/' + deviceId + '/actions'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="deviceCalibrationChosen"
          color="green"
          small
          @click="addDeviceCalibrationAction"
        >
          Add
        </v-btn>
        <v-btn
          v-else-if="softwareUpdateChosen"
          color="green"
          small
          @click="addDeviceSoftwareUpdateAction"
        >
          Add
        </v-btn>
        <v-btn
          v-else-if="otherChosen"
          color="green"
          small
          @click="addGenericDeviceAction"
        >
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { DeviceProperty } from '@/models/DeviceProperty'

import { dateToString, stringToDate } from '@/utils/dateHelper'

import DatePicker from '@/components/DatePicker.vue'

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

@Component({
  components: {
    DatePicker
  }
})
export default class ActionAddPage extends Vue {
  private rules: Object = {
    startDate: this.validateInputForStartDate,
    endDate: this.validateInputForEndDate,
    contactNotNull: this.mustBeProvided('Contact'),
    currentCalibrationDateNotNull: this.mustBeProvided('Current calibration date'),
    updateDateNotNull: this.mustBeProvided('Update date'),
    startDateNotNull: this.mustBeProvided('Start date'),
    softwareTypeNotNull: this.mustBeProvided('Software type')
  }

  private datesAreValid = true
  private contactIsValid = true
  private softwareTypeIsValid = true

  private optionsForActionType: IOptionsForActionType[] = [
    { id: 'device-calibration', kind: 'device_calibration', name: 'Device calibration' },
    { id: 'software-update', kind: 'software_update', name: 'Software update' },
    { id: 'generic-action-1', kind: 'generic_device_action', /* uri: 'actionTypes/device_visit', */ name: 'Device visit' },
    { id: 'generic-action-2', kind: 'generic_device_action', /* uri: 'actionTypes/device_maintainance', */ name: 'Device maintainance' }
  ]

  private contacts: Contact[] = []
  private selectedContact: Contact | null = null
  private readonly labelForSelectMeButton = 'Add current user'

  private attachments: Attachment[] = []

  private measuredQuantities: DeviceProperty[] = []

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
    this.$api.devices.findRelatedDeviceAttachments(this.deviceId).then((foundAttachments) => {
      this.attachments = foundAttachments
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    })
    this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundMeasuredQuantities) => {
      this.measuredQuantities = foundMeasuredQuantities
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
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

  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    const innerFunc: (v: any) => boolean | string = function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
    return innerFunc
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  addDeviceCalibrationAction () {
    if (!(this.$refs.datesForm as Vue & { validate: () => boolean }).validate()) {
      return
    }
    if (!(this.$refs.contactForm as Vue & { validate: () => boolean}).validate()) {
      return
    }

    this.$store.commit('snackbar/setError', 'Not implemented yet')
  }

  addDeviceSoftwareUpdateAction () {
    if (!(this.$refs.datesForm as Vue & { validate: () => boolean }).validate()) {
      return
    }
    if (!(this.$refs.softwareTypeForm as Vue & { validate: () => boolean }).validate()) {
      return
    }
    if (!(this.$refs.contactForm as Vue & { validate: () => boolean}).validate()) {
      return
    }
    this.$store.commit('snackbar/setError', 'Not implemented yet')
  }

  addGenericDeviceAction () {
    if (!(this.$refs.datesForm as Vue & { validate: () => boolean }).validate()) {
      return
    }
    if (!(this.$refs.contactForm as Vue & { validate: () => boolean}).validate()) {
      return
    }
    this.$store.commit('snackbar/setError', 'Not implemented yet')
  }
}

</script>
