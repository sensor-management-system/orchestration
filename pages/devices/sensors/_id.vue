<template>
  <div>
    <v-breadcrumbs :items="navigation" />
    <h1>Add Sensor</h1>
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
              <v-card-title>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="persistent identifier (PID)"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="sensor.label"
                      label="label"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="sensor.state"
                      :items="states"
                      label="state"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="sensor.type"
                      :items="sensorTypes"
                      label="type"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.manufacturer"
                      label="manufacturer"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.model"
                      label="model"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="6">
                    <v-textarea
                      v-model="sensor.description"
                      label="Description"
                      rows="3"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.urlWebsite"
                      label="Website"
                      placeholder="https://"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.serialNumber"
                      label="Serial Number"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.inventoryNumber"
                      label="Inventar Number"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-checkbox
                      v-model="sensor.dualUse"
                      label="Dual Use"
                      hint="can be used for military aims"
                      :persistent-hint="true"
                      color="red darken-3"
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
              <v-card-title>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <PersonSelect :selected-persons.sync="sensor.responsiblePersons" />
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
              <v-card-title>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</v-card-title>
              <v-card-text>
                <v-btn
                  small
                  color="primary"
                >
                  add Property
                </v-btn>
                <br><br>
                <v-expansion-panels
                  v-model="propertyStates"
                  multiple
                >
                  <v-expansion-panel
                    v-for="(item, index) in [0, 1]"
                    :key="index"
                  >
                    <v-expansion-panel-header>
                      <v-row no-gutters>
                        <v-col cols="11">
                          Property {{ index+1 }}
                        </v-col>
                        <v-col cols="1">
                          <v-menu
                            right
                          >
                            <template v-slot:activator="{ on }">
                              <v-btn
                                icon
                                v-on="on"
                              >
                                <v-icon>mdi-dots-vertical</v-icon>
                              </v-btn>
                            </template>

                            <v-list>
                              <v-list-item>
                                <v-list-item-title>Copy</v-list-item-title>
                              </v-list-item>
                              <v-list-item>
                                <v-list-item-title>Delete</v-list-item-title>
                              </v-list-item>
                            </v-list>
                          </v-menu>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-select
                            label="compartment"
                          />
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-select
                            label="unit"
                          />
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            label="accuracy"
                          />
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-select
                            label="sampling media"
                          />
                        </v-col>
                        <v-col cols="12" md="1">
                          <v-text-field
                            label="measuring range min"
                          />
                        </v-col>
                        <v-col cols="12" md="1">
                          <v-text-field
                            label="measuring range min"
                          />
                        </v-col>
                        <v-col cols="12" md="3" offset="1">
                          <v-text-field
                            label="label"
                          />
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-select
                            label="variable"
                          />
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            label="failure value"
                          />
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
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
              <v-card-title>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</v-card-title>
              <v-card-text>
                <v-btn
                  small
                  color="primary"
                >
                  add Custom Field
                </v-btn>
                <br><br>
                <v-row
                  v-for="(item, index) in [0, 1]"
                  :key="index"
                >
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="key"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="value"
                    />
                  </v-col>
                  <v-col cols="1">
                    <v-btn
                      color="error"
                      small
                      outlined
                    >
                      delete
                    </v-btn>
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
              <v-card-title>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</v-card-title>
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
                        <strong>sensor created</strong>
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
          fab
          fixed
          bottom
          right
          color="primary"
        >
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import Sensor from '../../../models/Sensor'
import { SensorProperty } from '../../../models/SensorProperty'
import CustomTextField from '../../../models/CustomTextField'

// @ts-ignore
import PersonSelect from '../../../components/PersonSelect.vue'

@Component({
  components: { PersonSelect }
})
// @ts-ignore
export default class SensorIdPage extends Vue {
  private numberOfTabs: number = 5
  private activeTab: number = 0

  private sensor: Sensor = new Sensor()

  previousTab () {
    this.activeTab = this.activeTab === 0 ? this.numberOfTabs - 1 : this.activeTab - 1
  }

  nextTab () {
    this.activeTab = this.activeTab === this.numberOfTabs - 1 ? 0 : this.activeTab + 1
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
        text: 'Add Sensor'
      }
    ]
  }

  get sensorTypes () {
    return [
      {
        text: 'Einzelsensor',
        value: '1'
      },
      {
        text: 'Multiparameter Sonde',
        value: '2'
      }
    ]
  }

  get states () {
    return [
      {
        text: 'in warehouse',
        value: '1'
      },
      {
        text: 'in use',
        value: '2'
      },
      {
        text: 'under construction',
        value: '3'
      },
      {
        text: 'blocked',
        value: '4'
      },
      {
        text: 'scrapped',
        value: '5'
      }
    ]
  }

  get propertyStates () {
    return [
      0,
      1
    ]
  }

  @Watch('sensor', { immediate: true, deep: true })
  // @ts-ignore
  onSensorChanged (val: Sensor, oldVal: Sensor) {
    console.log('something changed', val.responsiblePersons)
  }
}
</script>
