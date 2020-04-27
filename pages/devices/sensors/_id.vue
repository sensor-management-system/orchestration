<template>
  <div>
    <v-breadcrumbs :items="navigation" />
    <h1>Add Sensor</h1>
    <v-form>
      <v-tabs
        v-model="activeTab"
      >
        <v-tab>Basic Data</v-tab>
        <v-tab>Persons</v-tab>
        <v-tab>Properties</v-tab>
        <v-tab>Custom Fields</v-tab>
        <v-tab>Events</v-tab>
        <v-tab-item>
          <v-row>
            <v-col cols="12" md="6">
              <span>Sensor URN: [MANUFACTURER_MODEL_TYPE_SERIALNUMBER]</span>
            </v-col>
          </v-row>
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
                chips
              >
                <template v-slot:selection="{ item }">
                  <v-chip v-if="item.value == 2" color="green"><span>{{ item.text }}</span></v-chip>
                  <v-chip v-else-if="item.value == 3" color="red"><span>{{ item.text }}</span></v-chip>
                  <v-chip v-else><span>{{ item.text }}</span></v-chip>
                </template>
              </v-select>
            </v-col>
          </v-row>
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
          <v-row>
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
            <v-col cols="12" md="3">
              <v-select
                :items="sensorTypes"
                label="type"
              />
            </v-col>
          </v-row>
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
          <v-row>
            <v-col cols="12" md="3">
              <v-btn
                outlined
                right
                @click="nextTab(1)"
              >
                next
              </v-btn>
            </v-col>
          </v-row>
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
    </v-form>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class Sensors extends Vue {
  activeTab: number = 0

  nextTab (tabNr:number) {
    this.activeTab = tabNr
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
}
</script>
