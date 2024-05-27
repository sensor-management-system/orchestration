<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/configurations/' + configurationId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <ParameterChangeActionForm
      ref="parameterChangeActionForm"
      v-model="parameterChangeAction"
      :parameters="configurationParameters"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
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
  AddConfigurationParameterChangeActionAction,
  LoadAllConfigurationActionsAction,
  ConfigurationsState
} from '@/store/configurations'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { SetLoadingAction } from '@/store/progressindicator'
import ParameterChangeActionForm from '@/components/actions/ParameterChangeActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    ParameterChangeActionForm
  },
  computed: mapState('configurations', ['chosenKindOfConfigurationAction', 'configurationParameters', 'configurationPresetParameter']),
  methods: {
    ...mapActions('configurations', ['addConfigurationParameterChangeAction', 'loadAllConfigurationActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewParameterChangeAction extends mixins(CheckEditAccess) {
  private parameterChangeAction: ParameterChangeAction = new ParameterChangeAction()

  // vuex definition for typescript check
  configurationParameters!: ConfigurationsState['configurationParameters']
  chosenKindOfConfigurationAction!: ConfigurationsState['chosenKindOfConfigurationAction']
  configurationPresetParameter!: ConfigurationsState['configurationPresetParameter']
  addConfigurationParameterChangeAction!: AddConfigurationParameterChangeActionAction
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

  created () {
    if (this.chosenKindOfConfigurationAction === null) {
      this.$router.push('/configurations/' + this.configurationId + '/actions')
      return
    }

    if (this.configurationPresetParameter) {
      this.parameterChangeAction.parameter = this.configurationPresetParameter
    } else if (this.configurationParameters.length === 1) {
      this.parameterChangeAction.parameter = this.configurationParameters[0]
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async save () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.parameterChangeActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    if (!this.parameterChangeAction.parameter || this.parameterChangeAction.parameter.id === null) {
      this.$store.commit('snackbar/setError', 'Please select a parameter')
      return
    }

    try {
      this.setLoading(true)
      await this.addConfigurationParameterChangeAction({
        parameterId: this.parameterChangeAction.parameter.id,
        action: this.parameterChangeAction
      })
      this.loadAllConfigurationActions(this.configurationId)
      this.$router.push('/configurations/' + this.configurationId + '/actions')
      this.$store.commit('snackbar/setSuccess', 'New Parameter Change Action added')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
