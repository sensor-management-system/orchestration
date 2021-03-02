<template>
  <div>
    <v-progress-circular
      v-if="isLoading"
      class="center-absolute"
      indeterminate
    />
    <NuxtChild
      :value="device"
    />
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
import { Component, Vue } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'

@Component
export default class DevicePage extends Vue {
  private device: Device = new Device()
  private isLoading: boolean = true

  created () {
    if (this.isBasePath()) {
      this.$router.push('/devices/show/' + this.deviceId + '/basic')
    }
  }

  mounted () {
    this.initializeAppBar()
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
}
</script>
