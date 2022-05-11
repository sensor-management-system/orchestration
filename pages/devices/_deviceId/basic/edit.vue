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
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <DeviceBasicDataForm
      ref="basicForm"
      v-model="deviceCopy"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <!-- <v-alert
      :value="showNavigationWarning"
      color="warning"
      dark
      icon="mdi-alert"
      transition="scale-transition"
    >
      <v-row>
        You are about to discard your changes. Are you sure?
      </v-row>
      <v-row>
        <v-btn @click="closeDialog">
          No, stay here
        </v-btn>
        <v-btn @click="saveChanges">
          Save and move on
        </v-btn>
        <v-btn @click="discardChanges">
          Yes, continue
        </v-btn>
      </v-row>
    </v-alert> -->

    <v-dialog
      v-model="showNavigationWarning"
      width="500"
      @click:outside="closeDialog"
    >
      <v-card class="">
        <v-card-title class="text-h5">
          <!-- <v-icon>mdi-alert</v-icon> -->
           Unsaved changes
        </v-card-title>

        <v-card-text>
          You have unsaved changes. Are you sure you want to leave the page?
        </v-card-text>

        <v-card-actions>
          <v-spacer />

          <v-btn
            color=""
            text
            @click.stop="closeDialog"
          >
            close
          </v-btn>


          <v-btn
            color="secondary"
            text
            @click="discardChanges"
          >
            Discard changes
          </v-btn>
          <v-btn
            color="primary"

            @click="saveChanges"
          >
            Save changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'

import { mapActions, mapState } from 'vuex'
import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('devices', ['device']),
  methods: mapActions('devices', ['saveDevice', 'loadDevice'])
})
export default class DeviceEditBasicPage extends Vue {
  private deviceCopy: Device = new Device()
  private isSaving: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null

  // private continueToDifferentPage = () => {
  //   this.showNavigationWarning = false
  //   this.$router.push(this.to)
  // }

  // private stayOnPage = () => {
  //   this.showNavigationWarning = false
  //   this.to = null
  // }

  closeDialog () {
    this.showNavigationWarning = false
    this.to = null
  }

  async saveChanges () {
    // add code to save changes here
    await this.save()
    this.showNavigationWarning = false
    console.log('save and goto', this.to)
    this.$router.push(this.to.path)
  }

  discardChanges () {
    this.showNavigationWarning = false
    console.log('discard and goto', this.to)
    this.$router.push(this.to.path)
  }

  // vuex definition for typescript check
  device!: Device
  saveDevice!: (device: Device) => Promise<Device>
  loadDevice!: ({
    deviceId,
    includeContacts,
    includeCustomFields,
    includeDeviceProperties,
    includeDeviceAttachments
  }:
    { deviceId: string, includeContacts: boolean, includeCustomFields: boolean, includeDeviceProperties: boolean, includeDeviceAttachments: boolean }) => void

  created () {
    this.deviceCopy = Device.createFromObject(this.device)
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get deviceHasBeenEdited () {
    return (JSON.stringify(this.device) !== JSON.stringify(this.deviceCopy))
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.isSaving = true
      await this.saveDevice(this.deviceCopy)
      this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false
      }) // Todo eventuell gibt es eine besser möglichkeit die Änderungen nachzuladen/eventuell das gespeicherte Device als das device im store setzen
      this.$store.commit('snackbar/setSuccess', 'Device updated')
      this.$router.push('/devices/' + this.deviceId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isSaving = false
    }
  }

  beforeRouteLeave (to, from, next) {
    // called when the route that renders this component is about to
    // be navigated away from.
    // has access to `this` component instance.
    if (this.deviceHasBeenEdited) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }
}
</script>
