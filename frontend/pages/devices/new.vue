<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
        :country-names="countryNames"
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
    <serial-number-warning-dialog v-model="showSerialNumberWarning" entity="device" @confirm="saveWithoutSerialNumber" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { CreatePidAction, SaveDeviceAction } from '@/store/devices'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import SerialNumberWarningDialog from '@/components/shared/SerialNumberWarningDialog.vue'

import { Device } from '@/models/Device'
import { LoadCountriesAction } from '@/store/vocabulary'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    NonModelOptionsForm,
    SerialNumberWarningDialog
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['countryNames'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadCountries']),
    ...mapActions('devices', ['saveDevice', 'createPid']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class DeviceNewPage extends Vue {
  private device: Device = new Device()

  private showSerialNumberWarning = false
  private wantsToSaveWithoutSerialNumber = false
  private createOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  saveDevice!: SaveDeviceAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  loadCountries!: LoadCountriesAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    this.initializeAppBar()
    try {
      await this.loadCountries()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load countries')
    }
  }

  saveWithoutSerialNumber () {
    this.wantsToSaveWithoutSerialNumber = true
    this.save()
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    if (this.device.serialNumber === '') {
      if (!this.wantsToSaveWithoutSerialNumber) {
        this.showSerialNumberWarning = true
        return
      }
    }

    try {
      this.setLoading(true)
      const savedDevice = await this.saveDevice(this.device)
      this.$store.commit('snackbar/setSuccess', 'Device created')

      if (this.createOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedDevice.persistentIdentifier = await this.createPid(savedDevice.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      this.$store.commit('snackbar/setSuccess', 'Device created')
      this.$router.push('/devices/' + savedDevice.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Creation of device failed')
    } finally {
      this.setLoading(false)
    }
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
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
        name: 'Parameters',
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
