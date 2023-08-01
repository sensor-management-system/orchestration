<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
      v-model="isLoading"
      dark
    />
    <v-select
      value="Parameter Value Change"
      :items="['Parameter Value Change']"
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

    <ParameterChangeActionForm
      ref="configurationParameterChangeActionForm"
      v-model="action"
      :parameters="configurationParameters"
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
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  LoadConfigurationParameterChangeActionAction,
  LoadAllConfigurationActionsAction,
  LoadConfigurationParametersAction,
  UpdateConfigurationParameterChangeActionAction,
  ConfigurationsState
} from '@/store/configurations'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import ParameterChangeActionForm from '@/components/actions/ParameterChangeActionForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    ParameterChangeActionForm,
    ProgressIndicator,
    SaveAndCancelButtons
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('configurations', ['configurationParameterChangeAction', 'configurationParameters']),
  methods: mapActions('configurations', ['loadConfigurationParameterChangeAction', 'loadAllConfigurationActions', 'loadConfigurationParameters', 'updateConfigurationParameterChangeAction'])
})
export default class ConfigurationParameterChangeActionEditPage extends mixins(CheckEditAccess) {
  private action: ParameterChangeAction = new ParameterChangeAction()
  private isLoading = false

  // vuex definition for typescript check
  configurationParameterChangeAction!: ConfigurationsState['configurationParameterChangeAction']
  configurationParameters!: ConfigurationsState['configurationParameters']
  loadConfigurationParameterChangeAction!: LoadConfigurationParameterChangeActionAction
  loadConfigurationParameters!: LoadConfigurationParametersAction
  updateConfigurationParameterChangeAction!: UpdateConfigurationParameterChangeActionAction
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
        this.loadConfigurationParameterChangeAction(this.actionId),
        this.loadConfigurationParameters(this.configurationId)
      ])
      if (this.configurationParameterChangeAction) {
        this.action = ParameterChangeAction.createFromObject(this.configurationParameterChangeAction)
      }
    } catch {
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

  async save () {
    if (!(this.$refs.configurationParameterChangeActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    if (!this.action.parameter || this.action.parameter.id === null) {
      this.$store.commit('snackbar/setError', 'Please select a parameter')
      return
    }

    try {
      this.isLoading = true
      await this.updateConfigurationParameterChangeAction({
        parameterId: this.action.parameter.id,
        action: this.action
      })
      this.loadAllConfigurationActions(this.configurationId)
      this.$router.push('/configurations/' + this.configurationId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isLoading = false
    }
  }
}
</script>
