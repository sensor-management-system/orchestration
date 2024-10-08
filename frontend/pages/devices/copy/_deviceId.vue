<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :disabled="!canModifyEntity(deviceToCopy)"
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
            <v-checkbox v-model="copyParameters" label="Parameters" />
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
        :country-names="countryNames"
      />
      <NonModelOptionsForm
        v-model="copyOptions"
        :entity="deviceToCopy"
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
            <v-checkbox v-model="copyParameters" label="Parameters" />
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
          :disabled="!canModifyEntity(deviceToCopy)"
          :to="'/devices'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanModifyEntityGetter, UserGroupsGetter } from '@/store/permissions'
import { LoadDeviceAction, CopyDeviceAction, DevicesState, CreatePidAction, LoadDeviceAttachmentsAction } from '@/store/devices'

import { Device } from '@/models/Device'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import { LoadCountriesAction } from '@/store/vocabulary'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'userGroups']),
    ...mapState('devices', ['device']),
    ...mapGetters('vocabulary', ['countryNames'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadCountries']),
    ...mapActions('devices', ['copyDevice', 'loadDevice', 'createPid', 'loadDeviceAttachments']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class DeviceCopyPage extends Vue {
  private deviceToCopy: Device = new Device()
  private copyOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  private copyContacts: boolean = true
  private copyMeasuredQuantities: boolean = true
  private copyParameters: boolean = true
  private copyCustomFields: boolean = false
  private copyAttachments: boolean = false

  private persistentIdentifierPlaceholder: string | null = null
  private serialNumberPlaceholder: string | null = null
  private inventoryNumberPlaceholder: string | null = null

  // vuex definition for typescript check
  device!: DevicesState['device']
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  userGroups!: UserGroupsGetter
  loadDevice!: LoadDeviceAction
  copyDevice!: CopyDeviceAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  loadCountries!: LoadCountriesAction
  setShowBackButton!: SetShowBackButtonAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction

  async created () {
    this.initializeAppBar()
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDevice({
          deviceId: this.deviceId,
          includeContacts: true,
          includeCustomFields: true,
          includeDeviceProperties: true,
          includeDeviceAttachments: true,
          includeImages: true,
          includeDeviceParameters: true
        }),
        this.loadCountries(),
        this.loadDeviceAttachments(this.deviceId)
      ])

      if (!this.device || !this.canAccessEntity(this.device)) {
        this.$router.replace('/devices/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to copy this device.')
        return
      }

      const deviceCopy = this.getPreparedDeviceForCopy()
      if (deviceCopy) {
        this.deviceToCopy = deviceCopy
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading device failed')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  getPreparedDeviceForCopy (): Device | null {
    if (!this.device) {
      return null
    }
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
    deviceToEdit.permissionGroups = this.userGroups.filter(userGroup => this.device?.permissionGroups.filter(group => userGroup.equals(group)).length)
    return deviceToEdit
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const savedDeviceId = await this.copyDevice({
        device: this.deviceToCopy,
        copyContacts: this.copyContacts,
        copyAttachments: this.copyAttachments,
        copyMeasuredQuantities: this.copyMeasuredQuantities,
        copyParameters: this.copyParameters,
        copyCustomFields: this.copyCustomFields,
        originalDeviceId: this.deviceId
      })
      if (this.copyOptions.persistentIdentifierShouldBeCreated) {
        try {
          this.deviceToCopy.persistentIdentifier = await this.createPid(savedDeviceId)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      this.$store.commit('snackbar/setSuccess', 'Device copied')
      this.$router.push('/devices/' + savedDeviceId)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Copy failed')
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
        name: 'Export Control',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      }
    ])
    this.setTitle('Copy Device')
  }

  @Watch('device', { immediate: true, deep: true })
  onDeviceChanged (val: DevicesState['device']) {
    if (val && val.id) {
      this.setTitle('Copy ' + val.shortName)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
