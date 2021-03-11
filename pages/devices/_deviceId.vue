<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-card flat>
      <NuxtChild
        v-model="device"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class DevicePage extends Vue {
  private device: Device = new Device()
  private isLoading: boolean = true

  created () {
    if (this.isBasePath()) {
      this.$router.push('/devices/' + this.deviceId + '/basic')
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

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/devices/' + this.deviceId + '/basic',
          name: 'Basic Data'
        },
        {
          to: '/devices/' + this.deviceId + '/contacts',
          name: 'Contacts'
        },
        {
          to: '/devices/' + this.deviceId + '/properties',
          name: 'Properties'
        },
        {
          to: '/devices/' + this.deviceId + '/customfields',
          name: 'Custom Fields'
        }
      ],
      title: 'Devices'
    })
  }

  isBasePath () {
    return this.$route.path === '/devices/' + this.deviceId || this.$route.path === '/devices/' + this.deviceId + '/'
  }

  get deviceId () {
    return this.$route.params.deviceId
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
