<template>
  <div>
    <h1>Edit Device</h1>
    <v-tabs
      v-model="activeTab"
    >
      <v-tab nuxt :to="'/devices/show/' + deviceId + '/basic'">
        Basic
      </v-tab>
      <v-tab nuxt :to="'/devices/show/' + deviceId + '/contacts'">
        Contacts
      </v-tab>
    </v-tabs>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component({

})
export default class DeviceShowPage extends Vue {
  private numberOfTabs: number = 5
  private activeTab: number = 1

  created () {
    if (this.isBasePath()) {
      this.$router.push('/devices/show/' + this.deviceId + '/basic')
    }
  }

  isBasePath () {
    return this.$route.path === '/devices/show/' + this.deviceId || this.$route.path === '/devices/show/' + this.deviceId + '/'
  }

  get deviceId () {
    return this.$route.params.deviceId
  }
}
</script>
