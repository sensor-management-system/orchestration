<template>
  <div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addGenericAction"
      />
    </v-card-actions>
    <GenericActionForm
      ref="genericDeviceActionForm"
      v-model="genericDeviceAction"
      :attachments="deviceAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        :show-apply="true"
        @apply="addGenericAction"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { GenericAction } from '@/models/GenericAction'
import { mapActions, mapState } from 'vuex'
import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'

@Component({
  middleware:['auth'],
  components: { ActionButtonTray, GenericActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: mapActions('devices',['addDeviceGenericAction','loadAllDeviceActions'])
})
export default class NewGenericDeviceAction extends Vue {
  private genericDeviceAction: GenericAction = new GenericAction()

  get deviceId (): string {
    return this.$route.params.deviceId
  }


  addGenericAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericDeviceAction.actionTypeName = this.chosenKindOfDeviceAction?.name || ''
    this.genericDeviceAction.actionTypeUrl = this.chosenKindOfDeviceAction?.uri || ''

    try {
      this.addDeviceGenericAction({
        deviceId: this.deviceId,
        genericDeviceAction: this.genericDeviceAction
      });
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
