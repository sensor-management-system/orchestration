<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <DeviceBasicDataForm
      ref="basicForm"
      v-model="deviceCopy"
    />
    <NonModelOptionsForm
      v-model="editOptions"
      :entity="deviceCopy"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/basic'"
        @save="save"
      />
    </v-card-actions>

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="deviceHasBeenEdited"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'

import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { CreatePidAction, DevicesState, LoadDeviceAction, SaveDeviceAction } from '@/store/devices'

import { Device } from '@/models/Device'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    NavigationGuardDialog,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  computed: mapState('devices', ['device']),
  methods: {
    ...mapActions('devices', ['saveDevice', 'loadDevice', 'createPid']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceEditBasicPage extends mixins(CheckEditAccess) {
  private deviceCopy: Device | null = null

  private hasSaved: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private editOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  device!: DevicesState['device']
  saveDevice!: SaveDeviceAction
  loadDevice!: LoadDeviceAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/basic'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
  }

  created () {
    if (this.device) {
      this.deviceCopy = Device.createFromObject(this.device)
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get deviceHasBeenEdited () {
    if (!this.deviceCopy) {
      return false
    }
    return (JSON.stringify(this.device) !== JSON.stringify(this.deviceCopy))
  }

  async save () {
    if (!this.deviceCopy) {
      return
    }
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const savedDevice = await this.saveDevice(this.deviceCopy)
      if (this.editOptions.persistentIdentifierShouldBeCreated) {
        savedDevice.persistentIdentifier = await this.createPid(savedDevice.id)
      }
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false
      })
      this.hasSaved = true
      this.$store.commit('snackbar/setSuccess', 'Device updated')
      this.$router.push('/devices/' + this.deviceId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (this.deviceHasBeenEdited && !this.hasSaved) {
      if (this.to && this.to) {
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
