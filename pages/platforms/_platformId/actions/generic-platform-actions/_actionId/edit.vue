<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-card-actions>
      <v-spacer />
      <ActionButtonTray
        v-if="$auth.loggedIn"
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
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <ActionButtonTray
        v-if="$auth.loggedIn"
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :is-saving="isSaving"
        @apply="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { GenericAction } from '@/models/GenericAction'
import { Attachment } from '@/models/Attachment'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'

@Component({
  components: {
    ActionButtonTray,
    GenericActionForm
  },
  scrollToTop: true
})
export default class EditPlatformAction extends Vue {
  private action: GenericAction = new GenericAction()
  private attachments: Attachment[] = []
  private _isLoading: boolean = false
  private _isSaving: boolean = false

  async fetch (): Promise<any> {
    this.isLoading = true
    await Promise.all([
      this.fetchAttachments(),
      this.fetchAction()
    ])
    this.isLoading = false
  }

  async fetchAction (): Promise<any> {
    try {
      this.action = await this.$api.genericPlatformActions.findById(this.actionId)
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    }
  }

  async fetchAttachments (): Promise<any> {
    try {
      this.attachments = await this.$api.platforms.findRelatedPlatformAttachments(this.platformId)
    } catch (_) {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isLoading (): boolean {
    return this.$data._isLoading
  }

  set isLoading (value: boolean) {
    this.$data._isLoading = value
    this.$emit('showload', value)
  }

  get isSaving (): boolean {
    return this.$data._isSaving
  }

  set isSaving (value: boolean) {
    this.$data._isSaving = value
    this.$emit('showsave', value)
  }

  save (): void {
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.genericPlatformActions.update(this.platformId, this.action).then((action: GenericAction) => {
      this.$store.commit('snackbar/setSuccess', `Action: ${this.action.actionTypeName} updated`)
      this.$router.push('/platforms/' + this.platformId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }
}
</script>
