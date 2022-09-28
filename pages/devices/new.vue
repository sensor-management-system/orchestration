<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <DeviceBasicDataForm
        ref="basicForm"
        v-model="device"
      />
      <NonModelOptionsForm
        v-model="createOptions"
        :entity="device"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import { SetTitleAction, SetTabsAction } from '@/store/appbar'
import { CreatePidAction, SaveDeviceAction } from '@/store/devices'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    ProgressIndicator,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('devices', ['saveDevice', 'createPid']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])
  }
})
// @ts-ignore
export default class DeviceNewPage extends Vue {
  private device: Device = new Device()
  private isLoading: boolean = false
  private createOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  saveDevice!: SaveDeviceAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  createPid!: CreatePidAction

  created () {
    this.initializeAppBar()
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      const savedDevice = await this.saveDevice(this.device)
      if (this.createOptions.persistentIdentifierShouldBeCreated) {
        savedDevice.persistentIdentifier = await this.createPid(savedDevice.id)
      }
      this.$store.commit('snackbar/setSuccess', 'Device created')
      this.$router.push('/devices/' + savedDevice.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }

  initializeAppBar () {
    this.setTabs([
      {
        to: '/devices/new/',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Measured Quantities',
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
        name: 'Actions',
        disabled: true
      }
    ])
    this.setTitle('New Device')
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
