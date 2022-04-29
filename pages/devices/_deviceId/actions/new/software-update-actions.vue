<<template>
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
    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="softwareUpdateAction"
      :attachments="deviceAttachments"
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
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { mapActions, mapState } from 'vuex'

@Component({
  middleware:['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons,  SoftwareUpdateActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: mapActions('devices', ['addDeviceSoftwareUpdateAction', 'loadAllDeviceActions'])
})
export default class NewDeviceSoftwareUpdateActions extends Vue
{
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()
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
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving=true
      await this.addDeviceSoftwareUpdateAction({
        deviceId: this.deviceId,
        softwareUpdateAction: this.softwareUpdateAction
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New Software Update Action added')
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }finally {
      this.isSaving=false
    }
  }
}
</script>

<style scoped>

</style>
