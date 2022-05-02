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
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="softwareUpdateAction"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    ProgressIndicator,
    SoftwareUpdateActionForm
  },
  computed: mapState('platforms', ['platformAttachments', 'chosenKindOfPlatformAction']),
  methods: mapActions('platforms', ['addPlatformSoftwareUpdateAction', 'loadAllPlatformActions'])
})
export default class NewPlatformSoftwareUpdateActions extends Vue {
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()
  private isSaving: boolean = false

  created () {
    if (this.chosenKindOfPlatformAction === null) {
      this.$router.push('/platforms/' + this.platformId + '/actions')
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  async save () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      this.isSaving = true
      await this.addPlatformSoftwareUpdateAction(
        {
          platformId: this.platformId,
          softwareUpdateAction: this.softwareUpdateAction
        })
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'New Software Update Action added')
      this.$router.push('/platforms/' + this.platformId + '/actions')
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
