<template>
  <div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :show-apply="true"
        @apply="addGenericAction"
      />
    </v-card-actions>

    <GenericActionForm
      ref="genericPlatformActionForm"
      v-model="genericPlatformAction"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButtonTray
        :cancel-url="'/platforms/' + platformId + '/actions'"
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
  components: { ActionButtonTray, GenericActionForm },
  computed:mapState('platforms',['platformAttachments','chosenKindOfPlatformAction']),
  methods:mapActions('platforms',['addPlatformGenericAction','loadAllPlatformActions'])
})
export default class NewGenericPlatformAction extends Vue {

  private genericPlatformAction: GenericAction = new GenericAction()

  get platformId (): string {
    return this.$route.params.platformId
  }


  async addGenericAction () {

    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfPlatformAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfPlatformAction?.uri || ''

    try {
      await this.addPlatformGenericAction({platformId:this.platformId,genericPlatformAction: this.genericPlatformAction})
      this.loadAllPlatformActions(this.platformId)
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      console.log('e',e);
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }
  }
}
</script>

<style scoped>

</style>
