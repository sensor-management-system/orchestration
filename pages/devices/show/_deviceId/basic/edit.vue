<template>
  <div>
    <div v-if="isLoading">
      <v-progress-circular indeterminate />
    </div>
    <div v-else>
      <DeviceBasicDataForm
        v-model="value"
        :readonly="false"
      >
        <template v-slot:actions>
          <v-spacer />
          <v-btn
            v-if="isLoggedIn"
            small
            text
            nuxt
            :to="'/devices/show/' + deviceId + '/basic'"
          >
            cancel
          </v-btn>
          <v-btn
            v-if="isLoggedIn"
            color="primary"
            small
            @click="onSaveButtonClicked"
          >
            apply
          </v-btn>
        </template>
      </DeviceBasicDataForm>
    </div>
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
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  onSaveButtonClicked () {
    this.save().then(() => {
      this.$router.push('/devices/show/' + this.deviceId + '/basic')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  save (): Promise<Device> {
    return new Promise((resolve, reject) => {
      this.$api.devices.save(this.device).then((savedDevice) => {
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
