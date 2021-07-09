<template>
  <div>
    <v-card-actions>
      <v-spacer/>
      <platform-action-cancel-add-buttons
        v-if="isLoggedIn"
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :is-saving="isSaving"
        @apply="save"
      />
    </v-card-actions>

    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="action.actionTypeName"
      :items="[action.actionTypeName]"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <GenericActionForm
      ref="genericPlatformActionForm"
      v-model="action"
      :attachments="attachments"
    />

    <v-card-actions>
      <v-spacer/>
      <platform-action-cancel-add-buttons
        v-if="isLoggedIn"
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :is-saving="isSaving"
        @apply="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "nuxt-property-decorator";
import GenericActionForm from "@/components/GenericActionForm.vue";
import { GenericAction } from '@/models/GenericAction'
import {Attachment} from "@/models/Attachment";
import PlatformActionCancelAddButtons from "@/components/platform/actions/PlatformActionCancelAddButtons.vue";

@Component({
  components: {
    PlatformActionCancelAddButtons,
    GenericActionForm
  }
})
export default class EditPlatformAction extends Vue {
  private action: GenericAction = new GenericAction()
  private attachments: Attachment[] = []

  async fetch(): Promise<any> {
    this.isLoading = true
    await Promise.all([
      this.fetchAttachments(),
      this.fetchAction()
    ])
    this.isLoading = false
  }

  async fetchAction(): Promise<any> {
    try {
      this.action = await this.$api.genericPlatformActions.findById(this.actionId)
    } catch (error) {
      console.log(error)
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    }
  }

  async fetchAttachments(): Promise<any> {
    try {
      this.attachments = await this.$api.platforms.findRelatedPlatformAttachments(this.platformId)
    } catch (_) {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    }
  }

  get platformId(): string {
    return this.$route.params.platformId
  }

  get actionId(): string {
    return this.$route.params.actionId
  }

  get isLoggedIn(): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isLoading(): boolean {
    return this.$data._isLoading
  }

  set isLoading(value: boolean) {
    this.$data._isLoading = value
    this.$emit('showload', value)
  }

  get isSaving(): boolean {
    return this.$data._isSaving
  }

  set isSaving(value: boolean) {
    this.$data._isSaving = value
    this.$emit('showsave', value)
  }

  save(): void {
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.genericPlatformActions.update(this.platformId, this.action).then((action: GenericAction) => {
      this.$router.push('/platforms/' + this.platformId + '/actions', () => this.$emit('input', action))
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
