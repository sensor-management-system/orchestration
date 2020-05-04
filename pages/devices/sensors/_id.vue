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
                      label="label"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      :items="states"
                      label="state"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      :items="sensorTypes"
                      label="type"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="manufacturer"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="model"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="6">
                    <v-textarea label="Description" rows="3" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="Website"
                      placeholder="https://"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="Serial Number"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      label="Inventar Number"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-checkbox label="Dual Use" hint="can be used for military aims" :persistent-hint="true" color="red darken-3" />
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
                    <v-autocomplete
                      label="add a person"
                    />
                    <v-chip
                      class="ma-2"
                      color="indigo"
                      text-color="white"
                      :close="true"
                    >
                      <v-avatar left>
                        <v-icon>mdi-account-circle</v-icon>
                      </v-avatar>
                      Mister Marple
                    </v-chip>
                    <v-chip
                      class="ma-2"
                      color="indigo"
                      text-color="white"
                      :close="true"
                    >
                      <v-avatar left>
                        <v-icon>mdi-account-circle</v-icon>
                      </v-avatar>
                      Hans Hamster
                    </v-chip>
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
                <br /><br />
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
                <br /><br />
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
                      color="secondary"
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
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class Sensors extends Vue {
  numberOfTabs: number = 5
  activeTab: number = 0

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
}
</script>
