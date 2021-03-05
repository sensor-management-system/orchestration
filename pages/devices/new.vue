<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
  <v-card
    flat
  >
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        to="/search/devices"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        create
      </v-btn>
    </v-card-actions>
    <DeviceBasicDataForm
      ref="basicForm"
      v-model="device"
    />
  </v-card>
</template>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'

@Component({
  components: {
    DeviceBasicDataForm
  }
})
// @ts-ignore
export default class DeviceNewPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private device: Device = new Device()

  mounted () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  onSaveButtonClicked (): void {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    this.$api.devices.save(this.device).then((savedDevice) => {
      if (this.isLoggedIn) {
        this.$store.commit('snackbar/setSuccess', 'Device created')
        this.$router.push('/devices/' + savedDevice.id + '')
      } else {
        throw new Error('You need to be logged in to save the device')
      }
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/devices/new',
          name: 'Basic Data'
        },
        {
          name: 'Contacts',
          disabled: true
        },
        {
          name: 'Properties',
          disabled: true
        },
        {
          name: 'Custom Fields',
          disabled: true
        },
        {
          name: 'Attachments',
          disabled: true
        },
        {
          name: 'Events',
          disabled: true
        }
      ],
      title: 'Add Device'
    })
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
