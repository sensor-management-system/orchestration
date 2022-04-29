<template>
  <div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addCalibrationAction"
      />
    </v-card-actions>
    <DeviceCalibrationActionForm
      ref="deviceCalibrationActionForm"
      v-model="deviceCalibrationAction"
      :attachments="deviceAttachments"
      :measured-quantities="deviceMeasuredQuantities"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addCalibrationAction"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { mapActions, mapState } from 'vuex'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
@Component({
  middleware:['auth'],
  components: { ActionButtonTray, DeviceCalibrationActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction','deviceMeasuredQuantities'],),
  methods: mapActions('devices',['addDeviceCalibrationAction','loadAllDeviceActions'])
})
export default class NewDeviceCalibrationAction extends Vue {
  private deviceCalibrationAction: DeviceCalibrationAction = new DeviceCalibrationAction()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  addCalibrationAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.addDeviceCalibrationAction({
        deviceId: this.deviceId,
        calibrationDeviceAction: this.deviceCalibrationAction
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }
  }

}
</script>

<style scoped>

</style>
