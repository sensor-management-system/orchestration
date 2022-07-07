<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-select
      value="Software Update"
      :items="['Software Update']"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="action"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import {
  PlatformsState,
  LoadPlatformSoftwareUpdateActionAction,
  LoadAllPlatformActionsAction,
  LoadPlatformAttachmentsAction,
  UpdatePlatformSoftwareUpdateActionAction
} from '@/store/platforms'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator,
    SaveAndCancelButtons,
    SoftwareUpdateActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('platforms', ['platformSoftwareUpdateAction', 'platformAttachments']),
  methods: mapActions('platforms', ['loadPlatformSoftwareUpdateAction', 'loadAllPlatformActions', 'loadPlatformAttachments', 'updatePlatformSoftwareUpdateAction'])
})
export default class PlatformSoftwareUpdateActionEditPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private action: SoftwareUpdateAction = new SoftwareUpdateAction()
  private isSaving = false
  private isLoading = false

  // vuex definition for typescript check
  platformSoftwareUpdateAction!: PlatformsState['platformSoftwareUpdateAction']
  platformAttachments!: PlatformsState['platformAttachments']
  loadPlatformSoftwareUpdateAction!: LoadPlatformSoftwareUpdateActionAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  updatePlatformSoftwareUpdateAction!: UpdatePlatformSoftwareUpdateActionAction
  loadAllPlatformActions!: LoadAllPlatformActionsAction

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await Promise.all([
        this.loadPlatformSoftwareUpdateAction(this.actionId),
        this.loadPlatformAttachments(this.platformId)
      ])
      if (this.platformSoftwareUpdateAction) {
        this.action = SoftwareUpdateAction.createFromObject(this.platformSoftwareUpdateAction)
      }
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.isLoading = false
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.updatePlatformSoftwareUpdateAction({
        platformId: this.platformId,
        softwareUpdateAction: this.action
      })
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software Update Action updated')
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/platforms/' + this.platformId + '/actions', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this platform.')
      })
    }
  }
}
</script>
