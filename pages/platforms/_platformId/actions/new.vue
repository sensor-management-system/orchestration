<template>
  <div>
    <v-card>
      <v-card-actions>
        <v-spacer />
        <platform-action-cancel-add-buttons
          :cancel-url="'/platforms/' + platformId + '/actions'"
          :is-saving="isSaving"
          :show-apply="genericActionChosen"
          @apply="addGenericAction"
        />
      </v-card-actions>
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="genericActionTypes"
          :item-text="(x) => x.name"
          :item-value="(x) => x"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
        />
      </v-card-text>

      <v-card-text
        v-if="genericActionChosen"
      >
        <GenericActionForm
          ref="genericPlatformActionForm"
          v-model="genericPlatformAction"
          :attachments="attachments"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <platform-action-cancel-add-buttons
          :cancel-url="'/platforms/' + platformId + '/actions'"
          :is-saving="isSaving"
          :show-apply="genericActionChosen"
          @apply="addGenericAction"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import GenericActionForm from '@/components/GenericActionForm.vue'
import { ActionType } from '@/models/ActionType'
import { ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'
import { GenericAction } from '@/models/GenericAction'
import { Attachment } from '@/models/Attachment'
import PlatformActionCancelAddButtons from '@/components/platform/actions/PlatformActionCancelAddButtons.vue'

@Component({
  components: {
    PlatformActionCancelAddButtons,
    GenericActionForm
  }
})
export default class NewPlatformAction extends Vue {
  private genericActionTypes: ActionType[] = []
  private chosenKindOfAction: ActionType | null = null
  private genericPlatformAction: GenericAction = new GenericAction()
  private attachments: Attachment[] = []
  private isSaving: boolean = false

  async fetch () {
    await Promise.all([
      this.fetchGenericActionTypes()
    ])
  }

  async fetchGenericActionTypes (): Promise<any> {
    this.genericActionTypes = await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_PLATFORM).build().findMatchingAsList()
  }

  get genericActionChosen (): boolean {
    return !!this.chosenKindOfAction
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  addGenericAction () {
    if (!this.isLoggedIn) {
      return
    }
    if (!this.genericActionChosen) {
      return
    }
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfAction?.uri || ''

    this.isSaving = true
    this.$api.genericPlatformActions.add(this.platformId, this.genericPlatformAction).then((action: GenericAction) => {
      this.$store.commit('snackbar/setSuccess', `Action: ${this.genericPlatformAction.actionTypeName} created`)
      this.$router.push('/platforms/' + this.platformId + '/actions', () => this.$emit('input', action))
      // this.$router.push('/platforms/' + this.platformId + '/actions') TODO: Automatisches neuladen der Daten in der action.vue
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }
}
</script>

<style scoped>

</style>
