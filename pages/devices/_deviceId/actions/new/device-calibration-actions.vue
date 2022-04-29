<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer></v-spacer>
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
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
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import DeviceCalibrationActionForm from '@/components/actions/DeviceCalibrationActionForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { mapActions, mapState } from 'vuex'
@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    ProgressIndicator,
    DeviceCalibrationActionForm
  },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction', 'deviceMeasuredQuantities']),
  methods: mapActions('devices', ['addDeviceCalibrationAction', 'loadAllDeviceActions'])
})
export default class NewDeviceCalibrationAction extends Vue {
  private deviceCalibrationAction: DeviceCalibrationAction = new DeviceCalibrationAction()
  private isSaving: boolean = false

  created(){
    if(this.chosenKindOfDeviceAction === null){
      this.$router.push('/devices/' + this.deviceId + '/actions')
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.deviceCalibrationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.addDeviceCalibrationAction({
        deviceId: this.deviceId,
        calibrationDeviceAction: this.deviceCalibrationAction
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
      this.$store.commit('snackbar/setSuccess', 'New Calibration Action added')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }

}
</script>

<style scoped>

</style>
