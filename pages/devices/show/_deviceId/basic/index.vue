<template>
  <DeviceBasicDataForm
    v-model="value"
    :readonly="true"
  >
    <template v-slot:actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/show/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </template>
  </DeviceBasicDataForm>
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
export default class DeviceShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
