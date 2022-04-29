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
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
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
import { GenericAction } from '@/models/GenericAction'
import { mapActions, mapState } from 'vuex'
import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, SaveAndCancelButtons, GenericActionForm },
  computed:mapState('platforms',['platformAttachments','chosenKindOfPlatformAction']),
  methods:mapActions('platforms',['addPlatformGenericAction','loadAllPlatformActions'])
})
export default class NewGenericPlatformAction extends Vue {

  private genericPlatformAction: GenericAction = new GenericAction()
  private isSaving: boolean = false

  created(){
    if(this.chosenKindOfPlatformAction === null){
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
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfPlatformAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfPlatformAction?.uri || ''

    try {
      this.isSaving=true
      await this.addPlatformGenericAction({platformId:this.platformId,genericPlatformAction: this.genericPlatformAction})
      this.loadAllPlatformActions(this.platformId)
      let successMessage = this.genericPlatformAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
      this.$router.push('/platforms/' + this.platformId + '/actions')
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
