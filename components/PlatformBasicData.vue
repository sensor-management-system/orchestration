<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <label>URN</label>
        {{ platformURN }}
      </v-col>
      <v-col cols="12" md="3">
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

<style lang="scss">
@import '~vuetify/src/styles/settings/variables';
@import '~vuetify/src/styles/settings/colors';

label {
  /* TODO: move to its own file */
  display: block;
  font-size: map-deep-get($headings, 'caption', 'size');
  font-weight: map-deep-get($headings, 'caption', 'weight');
  letter-spacing: map-deep-get($headings, 'caption', 'letter-spacing');
  line-height: map-deep-get($headings, 'caption', 'line-height');
  font-family: map-deep-get($headings, 'caption', 'font-family');
  color: map-get($grey, 'darken-1');
}
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

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
    let partType = '[type]'
    let partShortName = '[short_name]'

    if (this.value.platformTypeUri !== '') {
      const manIndex = this.platformTypes.findIndex(m => m.uri === this.value.platformTypeUri)
      if (manIndex > -1) {
        partType = this.platformTypes[manIndex].name
      } else if (this.value.platformTypeName !== '') {
        partType = this.value.platformTypeName
      }
    } else if (this.value.platformTypeName !== '') {
      partType = this.value.platformTypeName
    }

    if (this.value.shortName !== '') {
      partShortName = this.value.shortName
    }

    return [partType, partShortName].join('_').replace(
      ' ', '_'
    )
  }
}
</script>
