<<template>
  <div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addSoftwareUpdateAction"
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
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addSoftwareUpdateAction"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import NewSoftwareUpdateActions from '@/pages/platforms/_platformId/actions/new/software-update-actions.vue'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
import { mapActions, mapState } from 'vuex'
@Component({
  components: { ActionButtonTray, SoftwareUpdateActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: mapActions('devices', ['addDeviceSoftwareUpdateAction', 'loadAllDeviceActions'])
})
export default class NewDeviceSoftwareUpdateActions extends Vue
{
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async addSoftwareUpdateAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      await this.addDeviceSoftwareUpdateAction({
        deviceId: this.deviceId,
        softwareUpdateAction: this.softwareUpdateAction
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
