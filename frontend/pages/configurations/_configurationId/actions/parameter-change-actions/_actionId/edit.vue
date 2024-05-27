<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    ParameterChangeActionForm,
    SaveAndCancelButtons
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('configurations', ['configurationParameterChangeAction', 'configurationParameters']),
  methods: {
    ...mapActions('configurations', ['loadConfigurationParameterChangeAction', 'loadAllConfigurationActions', 'loadConfigurationParameters', 'updateConfigurationParameterChangeAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationParameterChangeActionEditPage extends mixins(CheckEditAccess) {
  private action: ParameterChangeAction = new ParameterChangeAction()

  // vuex definition for typescript check
  configurationParameterChangeAction!: ConfigurationsState['configurationParameterChangeAction']
  configurationParameters!: ConfigurationsState['configurationParameters']
  loadConfigurationParameterChangeAction!: LoadConfigurationParameterChangeActionAction
  loadConfigurationParameters!: LoadConfigurationParametersAction
  updateConfigurationParameterChangeAction!: UpdateConfigurationParameterChangeActionAction
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction
  setLoading!: SetLoadingAction

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
      this.setLoading(true)
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
      this.setLoading(false)
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
      this.setLoading(true)
      await this.updateConfigurationParameterChangeAction({
        parameterId: this.action.parameter.id,
        action: this.action
      })
      this.loadAllConfigurationActions(this.configurationId)
      this.$router.push('/configurations/' + this.configurationId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
