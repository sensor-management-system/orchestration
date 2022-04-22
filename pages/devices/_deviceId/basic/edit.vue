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
      v-model="isLoading"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
    <DeviceBasicDataForm
      ref="basicForm"
      v-model="deviceCopy"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
  </div>
</template>




<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Device } from '@/models/Device'
import { mapActions, mapState } from 'vuex'

@Component({
  components: {
    DeviceBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('devices',['device']),
  methods: mapActions('devices',['saveDevice','loadDevice'])
})
export default class DeviceEditBasicPage extends Vue {

  private deviceCopy: Device = new Device()
  private isLoading: boolean = false

  created () {
    this.deviceCopy = Device.createFromObject(this.device)
  }

  async onSaveButtonClicked () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.isLoading = true
      await this.saveDevice(this.deviceCopy)
      this.loadDevice({
        deviceId:this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false
      }) // Todo eventuell gibt es eine besser möglichkeit die Änderungen nachzuladen/eventuell das gespeicherte Device als das device im store setzen
      this.$router.push('/devices/' + this.deviceId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }
}
</script>
