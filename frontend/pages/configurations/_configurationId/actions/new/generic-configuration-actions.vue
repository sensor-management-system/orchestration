<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
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
    <GenericActionForm
      ref="genericConfigurationActionForm"
      v-model="genericConfigurationAction"
      :attachments="configurationAttachments"
      :current-user-contact-id="userInfo.contactId"
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
import { Component, Vue, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddConfigurationGenericAction,
  LoadAllConfigurationActionsAction,
  ConfigurationsState
} from '@/store/configurations'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  middleware: ['auth'],
  components: { SaveAndCancelButtons, GenericActionForm },
  computed: {
    ...mapState('configurations', ['configurationAttachments', 'chosenKindOfConfigurationAction']),
    ...mapState('permissions', ['userInfo'])
  },
  methods: {
    ...mapActions('configurations', ['addConfigurationGenericAction', 'loadAllConfigurationActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewGenericConfigurationAction extends mixins(CheckEditAccess) {
  private genericConfigurationAction: GenericAction = new GenericAction()

  // vuex definition for typescript check
  configurationAttachments!: ConfigurationsState['configurationAttachments']
  chosenKindOfConfigurationAction!: ConfigurationsState['chosenKindOfConfigurationAction']
  addConfigurationGenericAction!: AddConfigurationGenericAction
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
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async save () {
    if (!(this.$refs.genericConfigurationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericConfigurationAction.actionTypeName = this.chosenKindOfConfigurationAction?.name || ''
    this.genericConfigurationAction.actionTypeUrl = this.chosenKindOfConfigurationAction?.uri || ''

    try {
      this.setLoading(true)
      await this.addConfigurationGenericAction({
        configurationId: this.configurationId,
        genericAction: this.genericConfigurationAction
      })
      this.loadAllConfigurationActions(this.configurationId)
      const successMessage = this.genericConfigurationAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
      this.$router.push('/configurations/' + this.configurationId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
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

<style scoped>

</style>
