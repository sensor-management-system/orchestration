<template>
  <div>
    <v-progress-circular
      v-if="isLoading"
      class="center-absolute"
      indeterminate
    />
    <v-card flat>
      <v-card-title>Device URN: {{ deviceURN }}</v-card-title>
      <NuxtChild
        v-model="device"
      />
    </v-card>
  </div>
</template>

<style>
  .center-absolute {
    position: fixed;
    top: 50%;
    left: 50%;
    margin-top: -16px;
    margin-left: -16px;
  }
</style>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'
import { Manufacturer } from '@/models/Manufacturer'

@Component
export default class DevicePage extends Vue {
  private device: Device = new Device()
  private isLoading: boolean = true

  private manufacturers: Manufacturer[] = []

  created () {
    if (this.isBasePath()) {
      this.$router.push('/devices/show/' + this.deviceId + '/basic')
    }
  }

  mounted () {
    this.initializeAppBar()

    this.$api.manufacturer.findAllPaginated().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    })

    this.$api.devices.findById(this.deviceId).then((device) => {
      this.device = device
      this.isLoading = false
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading device failed')
      this.isLoading = false
    })
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/devices/show/' + this.deviceId + '/basic',
          name: 'Basic Data'
        },
        {
          to: '/devices/show/' + this.deviceId + '/contacts',
          name: 'Contacts'
        }
      ],
      title: 'Devices'
    })
  }

  isBasePath () {
    return this.$route.path === '/devices/show/' + this.deviceId || this.$route.path === '/devices/show/' + this.deviceId + '/'
  }

  get deviceId () {
    return this.$route.params.deviceId
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

  @Watch('device', { immediate: true, deep: true })
  // @ts-ignore
  onDeviceChanged (val: Device) {
    if (val.id) {
      this.$store.commit('appbar/setTitle', val?.shortName || 'Add Device')
    }
  }
}
</script>
