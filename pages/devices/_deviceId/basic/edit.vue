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

@Component({
  components: {
    DeviceBasicDataForm,
    ProgressIndicator
  }
})
export default class DeviceEditBasicPage extends Vue {
  // we need to initialize the instance variable with an empty Device instance
  // here, otherwise the form is not reactive
  private deviceCopy: Device = new Device()

  private isLoading: boolean = false

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  created () {
    this.deviceCopy = Device.createFromObject(this.value)
  }

  onSaveButtonClicked () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    this.isLoading = true
    this.save().then((device) => {
      this.isLoading = false
      this.$emit('input', device)
      this.$router.push('/devices/' + this.deviceId + '/basic')
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  save (): Promise<Device> {
    return new Promise((resolve, reject) => {
      this.$api.devices.save(this.deviceCopy).then((savedDevice) => {
        resolve(savedDevice)
      }).catch((_error) => {
        reject(_error)
      })
    })
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onDeviceChanged (val: Device) {
    this.deviceCopy = Device.createFromObject(val)
  }
}
</script>
