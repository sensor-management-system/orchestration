<template>
  <div>
    <v-row>
      <v-col>
        <v-btn v-if="isLoggedIn" nuxt :to="'/devices/show/' + deviceId + '/basic/edit'">
          Edit
        </v-btn>
      </v-col>
    </v-row>
    <DeviceBasicDataForm v-model="device" :readonly="true" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    DeviceBasicDataForm
  }
})
export default class DeviceShowBasicPage extends Vue {
  private device: Device = new Device()

  mounted () {
    this.$api.devices.findById(this.deviceId).then((device) => {
      this.device = device
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading device failed')
    })
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
