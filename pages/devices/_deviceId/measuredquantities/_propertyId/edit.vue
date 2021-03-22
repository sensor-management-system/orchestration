<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          ref="label"
          v-model="valueCopy.label"
          label="Label"
        />
      </v-col>
    </v-row>
    <v-row>
      <col>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click.prevent.stop="save"
      >
        Save
      </v-btn>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'

@Component({

})
export default class DevicePropertyEditPage extends Vue {
  private valueCopy: DeviceProperty = new DeviceProperty()
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: DeviceProperty

  created () {
    this.valueCopy = DeviceProperty.createFromObject(this.value)
  }

  save () {
    this.$api.deviceProperties.update(this.deviceId, this.valueCopy).then((newProperty: DeviceProperty) => {
      this.$emit('input', newProperty)
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save property')
    })
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
