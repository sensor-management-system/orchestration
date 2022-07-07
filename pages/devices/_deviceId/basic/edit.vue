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
import { Component, InjectReactive, Vue, Watch } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'

import { mapActions, mapState } from 'vuex'

import { DevicesState, LoadDeviceAction, SaveDeviceAction } from '@/store/devices'

import { Device } from '@/models/Device'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    ProgressIndicator,
    NavigationGuardDialog
  },
  middleware: ['auth'],
  computed: mapState('devices', ['device']),
  methods: mapActions('devices', ['saveDevice', 'loadDevice'])
})
export default class DeviceEditBasicPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private deviceCopy: Device = new Device()
  private isSaving: boolean = false
  private hasSaved: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null

  // vuex definition for typescript check
  device!: DevicesState['device']
  saveDevice!: SaveDeviceAction
  loadDevice!: LoadDeviceAction

  created () {
    if (this.device) {
      this.deviceCopy = Device.createFromObject(this.device)
    }
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
      this.hasSaved = true
      this.$store.commit('snackbar/setSuccess', 'Device updated')
      this.$router.push('/devices/' + this.deviceId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isSaving = false
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

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/devices/' + this.deviceId + '/basic', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this device.')
      })
    }
  }
}
</script>
