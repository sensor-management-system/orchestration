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
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <ParameterChangeActionForm
      ref="parameterChangeActionForm"
      v-model="parameterChangeAction"
      :parameters="platformParameters"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/platforms/' + platformId + '/actions'"
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
  AddPlatformParameterChangeActionAction,
  LoadAllPlatformActionsAction,
  PlatformsState
} from '@/store/platforms'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import ParameterChangeActionForm from '@/components/actions/ParameterChangeActionForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  middleware: ['auth'],
  components: {
    SaveAndCancelButtons,
    ParameterChangeActionForm
  },
  computed: mapState('platforms', ['chosenKindOfPlatformAction', 'platformParameters', 'platformPresetParameter']),
  methods: {
    ...mapActions('platforms', ['addPlatformParameterChangeAction', 'loadAllPlatformActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewParameterChangeAction extends mixins(CheckEditAccess) {
  private parameterChangeAction: ParameterChangeAction = new ParameterChangeAction()

  // vuex definition for typescript check
  platformParameters!: PlatformsState['platformParameters']
  chosenKindOfPlatformAction!: PlatformsState['chosenKindOfPlatformAction']
  platformPresetParameter!: PlatformsState['platformPresetParameter']
  addPlatformParameterChangeAction!: AddPlatformParameterChangeActionAction
  loadAllPlatformActions!: LoadAllPlatformActionsAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/actions'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  created () {
    if (this.chosenKindOfPlatformAction === null) {
      this.$router.push('/platforms/' + this.platformId + '/actions')
      return
    }

    if (this.platformPresetParameter) {
      this.parameterChangeAction.parameter = this.platformPresetParameter
    } else if (this.platformParameters.length === 1) {
      this.parameterChangeAction.parameter = this.platformParameters[0]
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
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
      await this.addPlatformParameterChangeAction({
        parameterId: this.parameterChangeAction.parameter.id,
        action: this.parameterChangeAction
      })
      this.loadAllPlatformActions(this.platformId)
      this.$router.push('/platforms/' + this.platformId + '/actions')
      this.$store.commit('snackbar/setSuccess', 'New Parameter Change Action added')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
