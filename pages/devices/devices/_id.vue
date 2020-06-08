<template>
  <div>
    <v-breadcrumbs :items="navigation" />
    <h1>Add Device</h1>
    <v-form>
      <v-card
        outlined
      >
        <v-tabs
          v-model="activeTab"
          background-color="grey lighten-3"
        >
          <v-tab>Basic Data</v-tab>
          <v-tab>Persons</v-tab>
          <v-tab>Properties</v-tab>
          <v-tab>Custom Fields</v-tab>
          <v-tab>Events</v-tab>
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.persistentIdentifier"
                      label="persistent identifier (PID)"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="device.label"
                      label="label"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="device.statusName"
                      :items="states"
                      label="status"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="device.manufacturerUri"
                      :items="manufacturers"
                      :item-value="(x) => x.uri"
                      label="manufacturer"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.model"
                      label="model"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="6">
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
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.website"
                      label="Website"
                      placeholder="https://"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.serialNumber"
                      label="Serial Number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="device.inventoryNumber"
                      label="Inventar Number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-checkbox
                      v-model="device.dualUse"
                      label="Dual Use"
                      hint="can be used for military aims"
                      :persistent-hint="true"
                      color="red darken-3"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="nextTab(1)"
                >
                  next ❯
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <ContactSelect :selected-contacts.sync="device.contacts" :readonly="readonly" />
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="previousTab"
                >
                  ❮ previous
                </v-btn>
                <v-btn
                  text
                  @click="nextTab"
                >
                  next ❯
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <DevicePropertyExpansionPanels v-model="device.properties" :readonly="readonly" />
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="previousTab"
                >
                  ❮ previous
                </v-btn>
                <v-btn
                  text
                  @click="nextTab"
                >
                  next ❯
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>device URN: {{ deviceURN }}</v-card-title>
              <v-card-text>
                <CustomFieldCards v-model="device.customFields" :readonly="readonly" />
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="previousTab"
                >
                  ❮ previous
                </v-btn>
                <v-btn
                  text
                  @click="nextTab"
                >
                  next ❯
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>device URN: {{ deviceURN }}</v-card-title>
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
              <v-card-actions>
                <v-btn
                  text
                  @click="previousTab"
                >
                  ❮ previous
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
        </v-tabs>
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
        <v-btn
          v-if="isInEditMode"
          fab
          fixed
          bottom
          right
          color="primary"
          @click="save"
        >
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import Device from '../../../models/Device'

// @ts-ignore
import ContactSelect from '../../../components/ContactSelect.vue'
// @ts-ignore
import DevicePropertyExpansionPanels from '../../../components/DevicePropertyExpansionPanels.vue'
// @ts-ignore
import CustomFieldCards from '../../../components/CustomFieldCards.vue'

import VCService from '../../../services/VCService'
import SmsService from '../../../services/SmsService'
import Manufacturer from '../../../models/Manufacturer'

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

  private states: string[] = []
  private manufacturers: Manufacturer[] = []

  private isInEditMode: boolean = false

  mounted () {
    VCService.findAllStates().then((foundStates) => {
      // TODO: Replace with real Status[] as we want to fill the uri & name
      this.states = foundStates.map(x => x.name)
    })
    VCService.findAllManufacturers().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    })
    this.loadDevice()
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

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  save () {
    SmsService.saveDevice(this.device).then((savedDevice) => {
      this.device = savedDevice
    })
  }

  get deviceURN () {
    return this.device.urn
  }

  previousTab () {
    this.activeTab = this.activeTab === 0 ? this.numberOfTabs - 1 : this.activeTab - 1
  }

  nextTab () {
    this.activeTab = this.activeTab === this.numberOfTabs - 1 ? 0 : this.activeTab + 1
  }

  get readonly () {
    return !this.isInEditMode
  }

  get navigation () {
    return [
      {
        disabled: false,
        exact: true,
        to: '/',
        text: 'Home'
      },
      {
        disabled: false,
        exact: true,
        to: '/devices',
        text: 'Devices'
      },
      {
        disabled: true,
        text: 'Add Device'
      }
    ]
  }

  @Watch('device', { immediate: true, deep: true })
  // @ts-ignore
  onDeviceChanged (val: device) {
    // @TODO: remove!
    // eslint-disable-next-line
    console.log('something changed in the device', val)
  }
}
</script>
