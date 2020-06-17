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
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
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
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <SensorPropertyExpansionPanels v-model="sensor.properties" :readonly="readonly" />
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>Sensor URN: {{ sensorURN }}</v-card-title>
              <v-card-text>
                <CustomFieldCards v-model="sensor.customFields" :readonly="readonly" />
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
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

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import Sensor from '../../../models/Sensor'

// @ts-ignore
import PersonSelect from '../../../components/PersonSelect.vue'
// @ts-ignore
import SensorPropertyExpansionPanels from '../../../components/SensorPropertyExpansionPanels.vue'
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
  private editMode: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.toggleEditMode()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      if (this.sensor && this.sensor.id) {
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

  mounted () {
    this.loadSensor()

    // make sure that all components (especially the dynamically passed ones) are rendered
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

  get isInEditMode (): boolean {
    return this.editMode
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

  get sensorURN () {
    return this.sensor.urn
  }

  get readonly () {
    return !this.isInEditMode
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
    if (val.id) {
      this.$nuxt.$emit('AppBarContent:title', 'Device ' + val.label)
    }
  }
}
</script>
