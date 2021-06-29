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
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/actions'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        :disabled="isSaving"
        @click="save"
      >
        apply
      </v-btn>
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
      ref="genericDeviceActionForm"
      v-model="action"
      :attachments="attachments"
    />

    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/actions'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        :disabled="isSaving"
        @click="save"
      >
        apply
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/GenericActionForm.vue'

@Component({
  components: {
    GenericActionForm
  },
  scrollToTop: true
})
export default class GenericDeviceActionEditPage extends Vue {
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
      this.action = await this.$api.genericDeviceActions.findById(this.actionId)
    } catch (_) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    }
  }

  async fetchAttachments (): Promise<any> {
    try {
      this.attachments = await this.$api.devices.findRelatedDeviceAttachments(this.deviceId)
    } catch (_) {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
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
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.genericDeviceActions.update(this.deviceId, this.action).then((action: GenericAction) => {
      this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }
}
</script>
