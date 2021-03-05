<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
    <v-card-text>
      <DeviceBasicDataForm
        v-model="deviceCopy"
      />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'

import { Device } from '@/models/Device'

@Component({
  components: {
    DeviceBasicDataForm
  }
})
export default class DeviceEditBasicPage extends Vue {
  // we need to initialize the instance variable with an empty Device instance
  // here, otherwise the form is not reactive
  private deviceCopy: Device = new Device()

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  created () {
    this.deviceCopy = Device.createFromObject(this.value)
  }

  onSaveButtonClicked () {
    this.save().then((device) => {
      this.$emit('input', device)
      this.$router.push('/devices/' + this.deviceId + '/basic')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  save (): Promise<Device> {
    return new Promise((resolve, reject) => {
      this.$api.devices.save(this.deviceCopy).then((savedDevice) => {
        resolve(savedDevice)
      }).catch((_error) => {
        reject(_error)
      })
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
