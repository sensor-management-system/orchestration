<template>
  <div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :show-apply="true"
        @apply="addSoftwareUpdateAction"
      />
    </v-card-actions>
    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="softwareUpdateAction"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :show-apply="true"
        @apply="addSoftwareUpdateAction"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import { mapActions, mapState } from 'vuex'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

@Component({
  components: {
    ActionButtonTray,
    SoftwareUpdateActionForm
  },
  computed: mapState('platforms', ['platformAttachments', 'chosenKindOfPlatformAction']),
  methods: mapActions('platforms', ['addPlatformSoftwareUpdateAction', 'loadAllPlatformActions'])
})
export default class NewSoftwareUpdateActions extends Vue {

  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()

  get platformId (): string {
    return this.$route.params.platformId
  }

  async addSoftwareUpdateAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    await this.addPlatformSoftwareUpdateAction(
      {
        platformId: this.platformId,
        softwareUpdateAction: this.softwareUpdateAction
      })
    this.loadAllPlatformActions(this.platformId)
    this.$router.push('/platforms/' + this.platformId + '/actions')
    this.$store.commit('snackbar/setError', 'Failed to save the action')

  }
}
</script>

<style scoped>

</style>
