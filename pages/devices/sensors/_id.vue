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
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="persistent identifier (PID)"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="sensor.label"
                      label="label"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="sensor.state"
                      :items="states"
                      label="state"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="sensor.type"
                      :items="sensorTypes"
                      label="type"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.manufacturer"
                      label="manufacturer"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.model"
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
                      v-model="sensor.description"
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
                      v-model="sensor.urlWebsite"
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
                      v-model="sensor.serialNumber"
                      label="Serial Number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="sensor.inventoryNumber"
                      label="Inventar Number"
                      :readonly="readonly"
                      :disabled="readonly"
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
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <PersonSelect :selected-persons.sync="sensor.responsiblePersons" :readonly="readonly" />
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
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <SensorPropertyExpansionPanels v-model="sensor.properties" :readonly="readonly" />
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
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <CustomFieldCards v-model="sensor.customFields" :readonly="readonly" />
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
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
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
          @click="toggleEditMode"
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

// @ts-ignore
import PersonSelect from '../../../components/PersonSelect.vue'
// @ts-ignore
import SensorPropertyExpansionPanels from '../../../components/SensorPropertyExpansionPanels.vue'
// @ts-ignore
import CustomFieldCards from '../../../components/CustomFieldCards.vue'

@Component({
  components: {
    PersonSelect,
    SensorPropertyExpansionPanels,
    CustomFieldCards
  }
})
// @ts-ignore
export default class SensorIdPage extends Vue {
  private numberOfTabs: number = 5
  private activeTab: number = 0

  private sensor: Sensor = new Sensor()
  private isInEditMode: boolean = false

  mounted () {
    this.loadSensor()
  }

  loadSensor () {
    const sensorId = this.$route.params.id
    if (sensorId) {
      this.isInEditMode = false
      // @TODO
    } else {
      this.isInEditMode = true
      // @TODO
    }
  }

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  get sensorURN () {
    return this.sensor.urn
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

  @Watch('sensor', { immediate: true, deep: true })
  // @ts-ignore
  onSensorChanged (val: Sensor) {
    // @TODO: remove!
    // eslint-disable-next-line
    console.log('something changed in the sensor', val)
  }
}
</script>
