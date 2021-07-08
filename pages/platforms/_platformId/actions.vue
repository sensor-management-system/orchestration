<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />

    <platform-new-action-button :platform-id="platformId"/>

    <template v-if="isAddActionPage">
      <NuxtChild
        @input="$fetch"
        @showsave="showsave"
      />
    </template>

    <template v-else-if="isEditActionPage">
      <NuxtChild
        @input="$fetch"
        @showload="showload"
        @showsave="showsave"
      />
    </template>

    <template v-else>
      <platform-action-timeline
        :actions="actions"
        :platform-id="platformId"
      />
      <platform-action-delete-dialog :platform-id="platformId" @update="fetchActions"/>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import PlatformActionTimeline from '@/components/platform/actions/PlatformActionTimeline'
import PlatformNewActionButton from '@/components/platform/actions/PlatformNewActionButton'
import ProgressIndicator from '@/components/ProgressIndicator'
import PlatformActionDeleteDialog from '@/components/platform/actions/PlatformActionDeleteDialog'
import { GenericAction } from '@/models/GenericAction'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'

@Component({
  components: {
    PlatformActionTimeline,
    PlatformNewActionButton,
    ProgressIndicator,
    PlatformActionDeleteDialog
  }
})
export default class PlatformActionsPage extends Vue {
  private isSaving: boolean = false
  private isLoading: boolean = false
  private actions: IActionCommonDetails[] = []

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get isAddActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/platforms\/' + this.platformId + '\/actions\/new$'
    return !!this.$route.path.match(addUrl)
  }

  get isEditActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/platforms\/' + this.platformId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  showsave (isSaving: boolean) {
    this.isSaving = isSaving
  }

  showload (isLoading: boolean) {
    this.isLoading = isLoading
  }

  async fetchGenericActions (): Promise<void> {
    const actions: GenericAction[] = await this.$api.platforms.findRelatedGenericActions(this.platformId)
    actions.forEach((action: GenericAction) => this.actions.push(action))
  }

  async fetchActions (): Promise<void> {
    this.actions = []
    await this.fetchGenericActions()
  }

  async fetch () {
    await this.fetchActions()
  }
}
</script>

<style scoped>

</style>
