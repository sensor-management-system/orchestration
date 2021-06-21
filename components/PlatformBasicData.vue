<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
      <v-col cols="12" md="6">
        <label>URN</label>
        {{ platformURN }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Persistent identifier (PID)</label>
        {{ value.persistentIdentifier | orDefault }}
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
        <label>Status</label>
        {{ platformStatusName | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Platform type</label>
        {{ platformTypeName | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Manufacturer</label>
        {{ platformManufacturerName | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Model</label>
        {{ value.model | orDefault }}
      </v-col>
    </v-row>
    <v-divider />
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
          <v-icon>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-divider />
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
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

import { createPlatformUrn } from '@/modelUtils/urnBuilders'

@Component
export default class PlatformBasicData extends Vue {
  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private platformTypes: PlatformType[] = []

  @Prop({
    default: () => new Platform(),
    required: true,
    type: Platform
  })
  readonly value!: Platform

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
    this.$api.platformTypes.findAllPaginated().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of platform types failed')
    })
  }

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get statusNames (): string[] {
    return this.states.map(s => s.name)
  }

  get platformTypeNames (): string[] {
    return this.platformTypes.map(t => t.name)
  }

  get platformManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get platformStatusName () {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.value.statusName
  }

  get platformTypeName () {
    const platformTypeIndex = this.platformTypes.findIndex(t => t.uri === this.value.platformTypeUri)
    if (platformTypeIndex > -1) {
      return this.platformTypes[platformTypeIndex].name
    }
    return this.value.platformTypeName
  }

  get platformURN () {
    return createPlatformUrn(this.value, this.platformTypes)
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
