<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
    <DeviceBasicData
      v-model="device"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DeviceBasicData from '@/components/DeviceBasicData.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    DeviceBasicData
  }
})
export default class DeviceShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  get device (): Device {
    return this.value
  }

  set device (value: Device) {
    this.$emit('input', value)
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
