<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <GenericActionForm
      ref="genericDeviceActionForm"
      v-model="genericDeviceAction"
      :attachments="deviceAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
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

import { mapActions, mapState } from 'vuex'
import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { GenericAction } from '@/models/GenericAction'
@Component({
  middleware: ['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons, GenericActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: mapActions('devices', ['addDeviceGenericAction', 'loadAllDeviceActions'])
})
export default class NewGenericDeviceAction extends Vue {
  private genericDeviceAction: GenericAction = new GenericAction()
  private isSaving: boolean = false

  created () {
    if (this.chosenKindOfDeviceAction === null) {
      this.$router.push('/devices/' + this.deviceId + '/actions')
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save () {
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericDeviceAction.actionTypeName = this.chosenKindOfDeviceAction?.name || ''
    this.genericDeviceAction.actionTypeUrl = this.chosenKindOfDeviceAction?.uri || ''

    try {
      this.isSaving = true
      await this.addDeviceGenericAction({
        deviceId: this.deviceId,
        genericDeviceAction: this.genericDeviceAction
      })
      this.loadAllDeviceActions(this.deviceId)
      const successMessage = this.genericDeviceAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
      this.$router.push('/devices/' + this.deviceId + '/actions')
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
