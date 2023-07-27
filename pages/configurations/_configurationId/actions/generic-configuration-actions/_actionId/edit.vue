<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="action.actionTypeName"
      :items="[action.actionTypeName]"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/configurations/' + configurationId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <GenericActionForm
      ref="genericConfigurationActionForm"
      v-model="action"
      :attachments="configurationAttachments"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/configurations/' + configurationId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  LoadConfigurationGenericActionAction,
  LoadAllConfigurationActionsAction,
  LoadConfigurationAttachmentsAction,
  UpdateConfigurationGenericActionAction,
  ConfigurationsState
} from '@/store/configurations'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    ProgressIndicator,
    GenericActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('configurations', ['configurationGenericAction', 'configurationAttachments']),
  methods: mapActions('configurations', ['loadConfigurationGenericAction', 'loadAllConfigurationActions', 'loadConfigurationAttachments', 'updateConfigurationGenericAction'])
})
export default class GenericConfigurationActionEditPage extends mixins(CheckEditAccess) {
  private action: GenericAction = new GenericAction()
  private isSaving = false
  private isLoading = false

  // vuex definition for typescript check
  configurationGenericAction!: ConfigurationsState['configurationGenericAction']
  configurationAttachments!: ConfigurationsState['configurationAttachments']
  loadConfigurationGenericAction!: LoadConfigurationGenericActionAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  updateConfigurationGenericAction!: UpdateConfigurationGenericActionAction
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/actions'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await Promise.all([
        this.loadConfigurationGenericAction(this.actionId),
        this.loadConfigurationAttachments(this.configurationId)
      ])
      if (this.configurationGenericAction) {
        this.action = GenericAction.createFromObject(this.configurationGenericAction)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.isLoading = false
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    if (!(this.$refs.genericConfigurationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      this.isSaving = true
      await this.updateConfigurationGenericAction({
        configurationId: this.configurationId,
        genericAction: this.action
      })
      this.loadAllConfigurationActions(this.configurationId)
      this.$store.commit('snackbar/setSuccess', `${this.action.actionTypeName} updated`)
      this.$router.push('/configurations/' + this.configurationId + '/actions')
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
      this.$router.replace('/configurations/' + this.configurationId + '/actions', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }
}
</script>
