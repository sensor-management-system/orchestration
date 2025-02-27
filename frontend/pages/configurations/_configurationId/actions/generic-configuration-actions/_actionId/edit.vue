<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
      :current-user-contact-id="userInfo.contactId"
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
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    GenericActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['configurationGenericAction', 'configurationAttachments']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapState('permissions', ['userInfo'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfigurationGenericAction', 'loadAllConfigurationActions', 'loadConfigurationAttachments', 'updateConfigurationGenericAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class GenericConfigurationActionEditPage extends mixins(CheckEditAccess) {
  private action: GenericAction = new GenericAction()

  // vuex definition for typescript check
  configurationGenericAction!: ConfigurationsState['configurationGenericAction']
  configurationAttachments!: ConfigurationsState['configurationAttachments']
  loadConfigurationGenericAction!: LoadConfigurationGenericActionAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  updateConfigurationGenericAction!: UpdateConfigurationGenericActionAction
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction
  isLoading!: LoadingSpinnerState['isLoading']
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
        this.loadConfigurationGenericAction(this.actionId),
        this.loadConfigurationAttachments(this.configurationId)
      ])
      if (this.configurationGenericAction) {
        this.action = GenericAction.createFromObject(this.configurationGenericAction)
      }
    } catch (e) {
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
    if (!(this.$refs.genericConfigurationActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      this.setLoading(true)
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
