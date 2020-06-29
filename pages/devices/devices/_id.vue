<template>
  <div>
    <v-form>
      <v-card
        outlined
      >
        <v-tabs-items
          v-model="activeTab"
        >
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.persistentIdentifier"
                      label="Persistent identifier (PID)"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="device.shortName"
                      label="Short name"
                      required
                      class="required"
                      :rules="[rules.required]"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="device.longName"
                      label="Long name"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="deviceStatusName"
                      :items="statusNames"
                      label="Status"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-combobox
                      v-model="deviceTypeName"
                      :items="deviceTypeNames"
                      label="Type"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-combobox
                      v-model="deviceManufacturerName"
                      :items="manufacturerNames"
                      label="Manufacturer"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.model"
                      label="Model"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="9">
                    <v-textarea
                      v-model="device.description"
                      label="Description"
                      rows="3"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="9">
                    <v-text-field
                      v-if="readonly"
                      v-model="device.website"
                      label="Website"
                      placeholder="https://"
                      type="url"
                      :readonly="true"
                      :disabled="true"
                    >
                      <template slot="append">
                        <a v-if="device.website.length > 0" :href="device.website" target="_blank">
                          <v-icon>
                            mdi-open-in-new
                          </v-icon>
                        </a>
                      </template>
                    </v-text-field>
                    <v-text-field
                      v-else
                      v-model="device.website"
                      label="Website"
                      placeholder="https://"
                      type="url"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.serialNumber"
                      label="Serial number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.inventoryNumber"
                      label="Inventory number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-checkbox
                      v-model="device.dualUse"
                      label="Dual use"
                      hint="can be used for military aims"
                      :persistent-hint="true"
                      color="red darken-3"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <ContactSelect :selected-contacts.sync="device.contacts" :readonly="readonly" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <DevicePropertyExpansionPanels v-model="device.properties" :readonly="readonly" />
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <CustomFieldCards v-model="device.customFields" :readonly="readonly" :rules="rules" />
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <v-timeline dense clipped>
                  <v-timeline-item
                    class="mb-4"
                    small
                  >
                    <v-row justify="space-between">
                      <v-col cols="2">
                        2020-04-28 10:15
                      </v-col>
                      <v-col cols="10">
                        <strong>attached to platform XY</strong>
                        <div>Max M.</div>
                      </v-col>
                    </v-row>
                  </v-timeline-item>
                  <v-timeline-item
                    class="mb-4"
                    color="grey"
                    icon-color="grey lighten-2"
                    small
                  >
                    <v-row justify="space-between">
                      <v-col cols="2">
                        2020-04-28 09:15
                      </v-col>
                      <v-col cols="10">
                        <strong>edited description</strong>
                        <div>Max M.</div>
                      </v-col>
                    </v-row>
                  </v-timeline-item>
                  <v-timeline-item
                    class="mb-4"
                    color="grey"
                    icon-color="grey lighten-2"
                    small
                  >
                    <v-row justify="space-between">
                      <v-col cols="2">
                        2020-04-20 08:05
                      </v-col>
                      <v-col cols="10">
                        <strong>device created</strong>
                        <div>Hans H.</div>
                      </v-col>
                    </v-row>
                  </v-timeline-item>
                </v-timeline>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-btn
          v-if="!isInEditMode"
          fab
          fixed
          bottom
          right
          color="secondary"
          @click="toggleEditMode"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<style lang="scss">
@import "~/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import Device from '../../../models/Device'

import CVService from '../../../services/CVService'
import SmsService from '../../../services/SmsService'

import DeviceType from '../../../models/DeviceType'
import Manufacturer from '../../../models/Manufacturer'
import Status from '../../../models/Status'

// @ts-ignore
import ContactSelect from '../../../components/ContactSelect.vue'
// @ts-ignore
import DevicePropertyExpansionPanels from '../../../components/DevicePropertyExpansionPanels.vue'
// @ts-ignore
import CustomFieldCards from '../../../components/CustomFieldCards.vue'
// @ts-ignore
import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'

// @ts-ignore
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Basic Data',
      'Persons',
      'Properties',
      'Custom Fields',
      'Events'
    ]
  }
}

@Component({
  components: {
    ContactSelect,
    DevicePropertyExpansionPanels,
    CustomFieldCards
  }
})
// @ts-ignore
export default class DeviceIdPage extends Vue {
  private numberOfTabs: number = 5
  private activeTab: number = 0

  private device: Device = new Device()

  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private deviceTypes: DeviceType[] = []

  private editMode: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      if (this.device && this.device.id) {
        this.toggleEditMode()
      } else {
        this.$router.push('/devices')
      }
    })

    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  private rules: Object = {
    required: (v: string) => !!v || 'Required'
  }

  mounted () {
    CVService.findAllStates().then((foundStates) => {
      // TODO: Replace with real Status[] as we want to fill the uri & name
      this.states = foundStates
    })
    CVService.findAllManufacturers().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    })
    CVService.findAllDeviceTypes().then((foundDeviceTypes) => {
      this.deviceTypes = foundDeviceTypes
    })
    this.loadDevice()
    this.$nextTick(() => {
      if (!this.$route.params.id) {
        this.$nuxt.$emit('AppBarContent:title', 'Add Device')
      }
      this.$nuxt.$emit('AppBarContent:save-button-hidden', !this.editMode)
      this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !this.editMode)
    })
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarContent:save-button-click')
    this.$nuxt.$off('AppBarContent:cancel-button-click')
    this.$nuxt.$off('AppBarExtension:change')
  }

  loadDevice () {
    const deviceId = this.$route.params.id
    if (deviceId) {
      this.isInEditMode = false
      SmsService.findDeviceById(deviceId).then((foundDevice) => {
        this.device = foundDevice
      })
    } else {
      this.isInEditMode = true
    }
  }

  get isInEditMode (): boolean {
    return this.editMode
  }

  save () {
    SmsService.saveDevice(this.device).then((savedDevice) => {
      this.device = savedDevice
      this.toggleEditMode()
    })
  }

  get deviceURN () {
    let partManufacturer = '[manufacturer]'
    let partModel = '[model]'
    let partSerialNumber = '[serial_number]'

    if (this.device.manufacturerUri !== '') {
      const manIndex = this.manufacturers.findIndex(m => m.uri === this.device.manufacturerUri)
      if (manIndex > -1) {
        partManufacturer = this.manufacturers[manIndex].name
      } else if (this.device.manufacturerName !== '') {
        partManufacturer = this.device.manufacturerName
      }
    } else if (this.device.manufacturerName !== '') {
      partManufacturer = this.device.manufacturerName
    }

    if (this.device.model !== '') {
      partModel = this.device.model
    }

    if (this.device.serialNumber !== '') {
      partSerialNumber = this.device.serialNumber
    }

    return [partManufacturer, partModel, partSerialNumber].join('_').replace(
      ' ', '_'
    )
  }

  set isInEditMode (editMode: boolean) {
    this.editMode = editMode
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$nuxt.$emit('AppBarContent:save-button-hidden', !editMode)
    this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !editMode)
  }

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  get readonly () {
    return !this.isInEditMode
  }

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get deviceManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.device.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.device.manufacturerName
  }

  set deviceManufacturerName (newName: string) {
    this.device.manufacturerName = newName
    const manufacturerIndex = this.manufacturers.findIndex(m => m.name === newName)
    if (manufacturerIndex > -1) {
      this.device.manufacturerUri = this.manufacturers[manufacturerIndex].uri
    } else {
      this.device.manufacturerUri = newName
    }
  }

  get statusNames (): string[] {
    return this.states.map(s => s.name)
  }

  get deviceTypeNames (): string[] {
    return this.deviceTypes.map(t => t.name)
  }

  get deviceStatusName () {
    const statusIndex = this.states.findIndex(s => s.uri === this.device.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.device.statusName
  }

  set deviceStatusName (newName: string) {
    this.device.statusName = newName
    const statusIndex = this.states.findIndex(s => s.name === newName)
    if (statusIndex > -1) {
      this.device.statusUri = this.states[statusIndex].uri
    } else {
      this.device.statusUri = ''
    }
  }

  get deviceTypeName () {
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.uri === this.device.deviceTypeUri)
    if (deviceTypeIndex > -1) {
      return this.deviceTypes[deviceTypeIndex].name
    }
    return this.device.deviceTypeName
  }

  set deviceTypeName (newName: string) {
    this.device.deviceTypeName = newName
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.name === newName)
    if (deviceTypeIndex > -1) {
      this.device.deviceTypeUri = this.deviceTypes[deviceTypeIndex].uri
    } else {
      this.device.deviceTypeUri = ''
    }
  }

  @Watch('device', { immediate: true, deep: true })
  // @ts-ignore
  onDeviceChanged (val: Device) {
    if (val.id) {
      this.$nuxt.$emit('AppBarContent:title', 'Device ' + val.shortName)
    }
  }
}
</script>
