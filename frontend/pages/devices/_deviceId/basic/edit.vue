<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
      :country-names="countryNames"
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

import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { CreatePidAction, DevicesState, LoadDeviceAction, SaveDeviceAction, LoadDeviceAttachmentsAction, SaveDeviceImagesAction } from '@/store/devices'

import { Device } from '@/models/Device'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import { LoadCountriesAction } from '@/store/vocabulary'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    NavigationGuardDialog,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['device', 'deviceAttachments']),
    ...mapGetters('vocabulary', ['countryNames'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadCountries']),
    ...mapActions('devices', ['loadDeviceAttachments', 'saveDevice', 'loadDevice', 'createPid', 'saveDeviceImages']),
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
  deviceAttachments!: DevicesState['deviceAttachments']
  saveDevice!: SaveDeviceAction
  loadDevice!: LoadDeviceAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  loadCountries!: LoadCountriesAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  saveDeviceImages!: SaveDeviceImagesAction
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

  async created () {
    if (this.device) {
      this.deviceCopy = Device.createFromObject(this.device)
      try {
        this.setLoading(true)
        await this.loadDeviceAttachments(this.deviceId)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      } finally {
        this.setLoading(false)
      }
    }
    await this.loadCountries()
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

    // handle images first
    try {
      this.setLoading(true)
      const savedImagesWithIds = await this.saveDeviceImages({ deviceId: this.deviceId, deviceImages: this.device!.images, deviceCopyImages: this.deviceCopy.images })
      this.deviceCopy.images = savedImagesWithIds
    } catch (e) {
      this.$store.commit('snackbar/setWarning', 'Save of images failed')
    }

    try {
      this.setLoading(true)
      const savedDevice = await this.saveDevice(this.deviceCopy)
      if (this.editOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedDevice.persistentIdentifier = await this.createPid(savedDevice.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }

      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false,
        includeImages: true
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
