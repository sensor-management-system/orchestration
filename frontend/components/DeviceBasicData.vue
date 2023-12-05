<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-row>
      <v-col cols="12">
        <label>Visibility / Permissions</label>
        <VisibilityChip
          v-model="value.visibility"
        />
        <PermissionGroupChips
          v-model="value.permissionGroups"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>URN</label>
        {{ deviceURN }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Persistent identifier (PID)</label>
        <pid-tooltip
          :value="value.persistentIdentifier"
          show-button
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>Short name</label>
        {{ value.shortName | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Long name</label>
        {{ value.longName | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Device type</label>
        {{ deviceTypeName | orDefault }}
        <v-tooltip v-if="deviceTypeDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ deviceTypeDefinition }}</span>
        </v-tooltip>
      </v-col>
      <v-col cols="12" md="3">
        <label>Manufacturer</label>
        {{ deviceManufacturerName | orDefault }}
        <v-tooltip v-if="deviceManufacturerDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ deviceManufacturerDefinition }}</span>
        </v-tooltip>
      </v-col>
      <v-col cols="12" md="3">
        <label>Model</label>
        {{ value.model | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Country of origin</label>
        {{ value.country | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Status</label>
        {{ deviceStatusName | orDefault }}
        <v-tooltip v-if="deviceStatusDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ deviceStatusDefinition }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row>
      <v-col cols="12" md="9">
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Website</label>
        {{ value.website | orDefault }}
        <a v-if="value.website.length > 0" :href="value.website" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row>
      <v-col cols="12" md="3">
        <label>Serial number</label>
        {{ value.serialNumber | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Inventory number</label>
        {{ value.inventoryNumber | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="value.keywords">
      <v-col>
        <label>Keywords</label>
        <v-chip-group v-if="value.keywords.length">
          <v-chip v-for="keyword, idx in value.keywords" :key="idx" small>
            {{ keyword }}
          </v-chip>
        </v-chip-group>
        <span v-else>
          {{ '' | orDefault }}
        </span>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Dual use</label>
        {{ value.dualUse ? 'yes' : 'no' }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import QrCodeDialog from '@/components/QrCodeDialog.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'

import { createDeviceUrn } from '@/modelUtils/urnBuilders'

@Component({
  components: {
    PermissionGroupChips,
    PidTooltip,
    QrCodeDialog,
    VisibilityChip
  }
})
export default class DeviceBasicData extends Vue {
  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private deviceTypes: DeviceType[] = []

  @Prop({
    default: () => new Device(),
    required: true,
    type: Device
  })
  readonly value!: Device

  mounted () {
    this.$api.states.findAllPaginated().then((foundStates) => {
      this.states = foundStates
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of states failed')
    })
    this.$api.manufacturer.findAllPaginated().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    })
    this.$api.deviceTypes.findAllPaginated().then((foundDeviceTypes) => {
      this.deviceTypes = foundDeviceTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of device types failed')
    })
  }

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get statusNames (): string[] {
    return this.states.map(s => s.name)
  }

  get deviceTypeNames (): string[] {
    return this.deviceTypes.map(t => t.name)
  }

  get deviceManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get deviceManufacturerDefinition (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].definition
    }
    return ''
  }

  get deviceStatusName (): string {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.value.statusName
  }

  get deviceStatusDefinition (): string {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].definition
    }
    return ''
  }

  get deviceTypeName (): string {
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.uri === this.value.deviceTypeUri)
    if (deviceTypeIndex > -1) {
      return this.deviceTypes[deviceTypeIndex].name
    }
    return this.value.deviceTypeName
  }

  get deviceTypeDefinition (): string {
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.uri === this.value.deviceTypeUri)
    if (deviceTypeIndex > -1) {
      return this.deviceTypes[deviceTypeIndex].definition
    }
    return ''
  }

  get deviceURN () {
    return createDeviceUrn(this.value, this.manufacturers)
  }

  /**
   * copies the PID-URL to the clipboard and changes the tooltip's text and color
   *
   * @returns {void}
   */
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
