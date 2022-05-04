<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/devices"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
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
        v-model="device"
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
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/devices"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Attachment } from '@/models/Attachment'
import { ContactRole } from '@/models/ContactRole'
import { CustomTextField } from '@/models/CustomTextField'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    DeviceBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth']
})
// @ts-ignore
export default class DeviceCopyPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private device: Device = new Device()
  private existingDevice: Device = new Device()
  private isLoading: boolean = true

  private copyContacts: boolean = true
  private copyMeasuredQuantities: boolean = true
  private copyCustomFields: boolean = false
  private copyAttachments: boolean = false

  private persistentIdentifierPlaceholder: string | null = null
  private serialNumberPlaceholder: string | null = null
  private inventoryNumberPlaceholder: string | null = null

  mounted () {
    this.initializeAppBar()
  }

  async fetch () {
    // We also load the contacts and the measured quantities as those
    // are the ones that we will also copy.
    try {
      const device = await this.$api.devices.findById(this.deviceId, {
        includeContacts: false,
        includeCustomFields: true,
        includeDeviceProperties: true,
        includeDeviceAttachments: true
      })
      this.existingDevice = device
      const deviceToEdit = Device.createFromObject(this.existingDevice)
      // Unset the fields that are very device specific
      // (we need other PIDs, serial numbers and inventory numbers)
      // For the moment we just unset them completely, but there may be
      // some more logic in those numbers.
      // For example the serial numbers could just be something like 'XXXX-1'
      // and for the next device 'XXXX-2'.
      // For the inventory numbers the same.
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

      this.device = deviceToEdit
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading device failed')
    } finally {
      this.isLoading = false
    }
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  async onSaveButtonClicked () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    if (!this.$auth.loggedIn) {
      this.$store.commit('snackbar/setError', 'You need to be logged in to save the device')
      return
    }
    this.isLoading = true
    const measuredQuantities = this.device.properties.map(DeviceProperty.createFromObject)
    const customFields = this.device.customFields.map(CustomTextField.createFromObject)
    const attachments = this.device.attachments.map(Attachment.createFromObject)
    try {
      // most importantly: Save the device itself
      const savedDevice = await this.$api.devices.save(this.device)
      const savedDeviceId = savedDevice.id!

      const related: Promise<any>[] = []

      if (this.copyContacts) {
        // Then we can deal about the contacts
        // The contacts have the special issue, that our system will add the contact who
        // add/edit the device automatically.
        // We we should check who we added this way already.
        const sourceContactRoles = await this.$api.devices.findRelatedContactRoles(this.deviceId)
        const freshCreatedContactRoles = await this.$api.devices.findRelatedContactRoles(savedDeviceId)
        // And then only add those remaining
        const contactRolesToSave = sourceContactRoles.filter(c => freshCreatedContactRoles.findIndex((ec: ContactRole) => { return ec.contact!.id === c.contact!.id && ec.roleName === c.roleName }) === -1)

        for (const contactRole of contactRolesToSave) {
          const contactRoleToSave = ContactRole.createFromObject(contactRole)
          // we don't have a reference to the device here, but we have an id
          // that we should remove before we save it
          contactRoleToSave.id = null
          related.push(this.$api.devices.addContact(savedDeviceId, contactRoleToSave))
        }
      }
      if (this.copyMeasuredQuantities) {
        // For the measured quantities it is simpler.
        // But the existing entries have already an id - so we have to unset those
        // in order to save them (otherwise we would get Unique Constraint Violations)
        for (const measuredQuantity of measuredQuantities) {
          measuredQuantity.id = null
          related.push(this.$api.deviceProperties.add(savedDeviceId, measuredQuantity))
        }
      }
      if (this.copyCustomFields) {
        for (const customField of customFields) {
          customField.id = null
          related.push(this.$api.customfields.add(savedDeviceId, customField))
        }
      }
      if (this.copyAttachments) {
        for (const attachment of attachments) {
          attachment.id = null
          related.push(this.$api.deviceAttachments.add(savedDeviceId, attachment))
        }
      }
      await Promise.all(related)

      this.isLoading = false
      this.$store.commit('snackbar/setSuccess', 'Device copied')
      this.$router.push('/devices/' + savedDevice.id + '')
    } catch (_error) {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Copy failed')
    }
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/devices/copy/' + this.deviceId,
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
      ],
      title: 'Copy Device'
    })
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  @Watch('existingDevice', { immediate: true, deep: true })
  // @ts-ignore
  onDeviceChanged (val: Device) {
    if (val.id) {
      this.$store.commit('appbar/setTitle', 'Copy ' + (val?.shortName || 'Device'))
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
