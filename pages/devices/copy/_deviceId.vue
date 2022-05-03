<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyMeasuredQuantities" label="Measured quantities" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyCustomFields" label="Custom fields" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            Please note: Actions will not be copied.
          </v-col>
        </v-row>
      </v-alert>
      <DeviceBasicDataForm
        ref="basicForm"
        v-model="deviceToCopy"
        :persistent-identifier-placeholder="persistentIdentifierPlaceholder"
        :serial-number-placeholder="serialNumberPlaceholder"
        :inventory-number-placeholder="inventoryNumberPlaceholder"
      />
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
        class="mt-2"
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyMeasuredQuantities" label="Measured quantities" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyCustomFields" label="Custom fields" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            Please note: Actions will not be copied.
          </v-col>
        </v-row>
      </v-alert>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('devices', ['device']),
  methods: {
    ...mapActions('devices', ['copyDevice', 'loadDevice']),
    ...mapActions('appbar', ['setDefaults', 'initDeviceCopyAppBar'])
  }
})
// @ts-ignore
export default class DeviceCopyPage extends Vue {
  private deviceToCopy: Device = new Device()
  private isSaving = false
  private isLoading = false

  private copyContacts: boolean = true
  private copyMeasuredQuantities: boolean = true
  private copyCustomFields: boolean = false
  private copyAttachments: boolean = false

  private persistentIdentifierPlaceholder: string | null = null
  private serialNumberPlaceholder: string | null = null
  private inventoryNumberPlaceholder: string | null = null

  // vuex definition for typescript check
  device!: Device
  initDeviceCopyAppBar!: (id: string) => void
  setDefaults!: () => void
  copyDevice!: ({ device, copyContacts, copyAttachments, copyMeasuredQuantities, copyCustomFields }:
    {device: Device, copyContacts: boolean, copyAttachments: boolean, copyMeasuredQuantities: boolean, copyCustomFields: boolean}) => string

  loadDevice!: ({
    deviceId,
    includeContacts,
    includeCustomFields,
    includeDeviceProperties,
    includeDeviceAttachments
  }:
    { deviceId: string, includeContacts: boolean, includeCustomFields: boolean, includeDeviceProperties: boolean, includeDeviceAttachments: boolean }) => void

  async created () {
    this.initDeviceCopyAppBar(this.deviceId)
    try {
      this.isLoading = true
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: true,
        includeCustomFields: true,
        includeDeviceProperties: true,
        includeDeviceAttachments: true
      })
      this.deviceToCopy = this.getPreparedDeviceForCopy()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading device failed')
    } finally {
      this.isLoading = false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  getPreparedDeviceForCopy (): any {
    const deviceToEdit = Device.createFromObject(this.device)
    deviceToEdit.id = null
    if (deviceToEdit.persistentIdentifier) {
      this.persistentIdentifierPlaceholder = deviceToEdit.persistentIdentifier
    }
    deviceToEdit.persistentIdentifier = ''
    if (deviceToEdit.serialNumber) {
      this.serialNumberPlaceholder = deviceToEdit.serialNumber
    }
    deviceToEdit.serialNumber = ''
    if (deviceToEdit.inventoryNumber) {
      this.inventoryNumberPlaceholder = deviceToEdit.inventoryNumber
    }
    deviceToEdit.inventoryNumber = ''
    return deviceToEdit
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isSaving = true
      const savedDeviceId = await this.copyDevice({
        device: this.deviceToCopy,
        copyContacts: this.copyContacts,
        copyAttachments: this.copyAttachments,
        copyMeasuredQuantities: this.copyMeasuredQuantities,
        copyCustomFields: this.copyCustomFields
      })
      this.$store.commit('snackbar/setSuccess', 'Device copied')
      this.$router.push('/devices/' + savedDeviceId)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Copy failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
