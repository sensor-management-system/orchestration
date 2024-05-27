<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          save-btn-text="Apply"
          :to="`/configurations/${configurationId}/basic`"
          @save="save"
        />
      </v-card-actions>
      <ConfigurationsBasicDataForm
        ref="basicDataForm"
        v-model="configurationCopy"
        :readonly="false"
      />
      <NonModelOptionsForm
        v-model="editOptions"
        :entity="configurationCopy"
      />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          save-btn-text="Apply"
          :to="`/configurations/${configurationId}/basic`"
          @save="save"
        />
      </v-card-actions>

      <navigation-guard-dialog
        v-model="showNavigationWarning"
        :has-entity-changed="configurationHasBeenEdited"
        :to="to"
        @close="to = null"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, mixins } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'

import { mapActions, mapState } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'

import { SetTitleAction } from '@/store/appbar'

import { Configuration } from '@/models/Configuration'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import { CreatePidAction, LoadConfigurationAction, SaveConfigurationAction, LoadConfigurationAttachmentsAction, SaveConfigurationImagesAction } from '@/store/configurations'

@Component({
  components: {
    ConfigurationsBasicDataForm,
    NavigationGuardDialog,
    NonModelOptionsForm,
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  computed: mapState('configurations', ['configuration']),
  methods: {
    ...mapActions('configurations', ['saveConfiguration', 'loadConfiguration', 'loadConfigurationAttachments', 'createPid', 'saveConfigurationImages']),
    ...mapActions('appbar', ['setTitle']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationEditBasicPage extends mixins(CheckEditAccess) {
  private configurationCopy: Configuration = new Configuration()

  private hasSaved: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private editOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  configuration!: Configuration
  saveConfiguration!: SaveConfigurationAction
  saveConfigurationImages!: SaveConfigurationImagesAction
  loadConfiguration!: LoadConfigurationAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  createPid!: CreatePidAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/basic'
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

  async created () {
    if (this.configuration) {
      this.configurationCopy = Configuration.createFromObject(this.configuration)
      try {
        this.setLoading(true)
        await this.loadConfigurationAttachments(this.configurationId)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      } finally {
        this.setLoading(false)
      }
    }
  }

  get configurationId () {
    return this.$route.params.configurationId
  }

  get configurationHasBeenEdited () {
    return (JSON.stringify(this.configuration) !== JSON.stringify(this.configurationCopy))
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    // handle images first
    try {
      this.setLoading(true)
      const savedImagesWithIds = await this.saveConfigurationImages({
        configurationId: this.configurationId,
        configurationImages: this.configuration!.images,
        configurationCopyImages: this.configurationCopy.images
      })
      this.configurationCopy.images = savedImagesWithIds
    } catch (e) {
      this.$store.commit('snackbar/setWarning', 'Save of images failed')
    }

    try {
      this.setLoading(true)
      await this.saveConfiguration(this.configurationCopy)
      if (this.editOptions.persistentIdentifierShouldBeCreated) {
        try {
          await this.createPid(this.configurationId)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      this.loadConfiguration(this.configurationId)
      this.hasSaved = true

      this.$store.commit('snackbar/setSuccess', 'Configuration updated')
      this.$router.push('/configurations/' + this.configurationId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (this.configurationHasBeenEdited && !this.hasSaved) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }

  @Watch('configuration', {
    immediate: true,
    deep: true
  })
  onConfigurationChanged (value: Configuration | null): void {
    if (value) {
      this.configurationCopy = Configuration.createFromObject(value)
    }
  }
}
</script>
