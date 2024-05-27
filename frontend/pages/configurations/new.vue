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
        <SaveAndCancelButtons
          :to="'/configurations'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <ConfigurationsBasicDataForm
        ref="basicDataForm"
        v-model="configuration"
        :readonly="false"
      />
      <NonModelOptionsForm
        v-model="createOptions"
        :entity="configuration"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/configurations'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'

import { Configuration } from '@/models/Configuration'

import { CreatePidAction, SaveConfigurationAction, ClearConfigurationAttachmentsAction } from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'

@Component({
  components: {
    ConfigurationsBasicDataForm,
    NonModelOptionsForm,
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['saveConfiguration', 'createPid', 'clearConfigurationAttachments']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationNewPage extends Vue {
  private configuration: Configuration = new Configuration()
  private createOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  initConfigurationsNewAppBar!: () => void
  saveConfiguration!: SaveConfigurationAction
  createPid!: CreatePidAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction
  clearConfigurationAttachments!: ClearConfigurationAttachmentsAction

  created () {
    this.initializeAppBar()
    this.clearConfigurationAttachments()
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const savedConfiguration = await this.saveConfiguration(this.configuration)
      if (this.createOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedConfiguration.persistentIdentifier = await this.createPid(savedConfiguration.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      this.$store.commit('snackbar/setSuccess', 'Configuration created')
      await this.$router.push('/configurations/' + savedConfiguration.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Creation of configuration failed')
    } finally {
      this.setLoading(false)
    }
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([
      {
        to: '/configurations/new',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Platforms and Devices',
        disabled: true
      },
      {
        name: 'Locations',
        disabled: true
      },
      {
        name: 'Parameters',
        disabled: true
      },
      {
        name: 'Custom Fields',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      },
      {
        name:
        'TSM Linkings',
        disabled: true
      }
    ])
    this.setTitle('New Configuration')
  }
}
</script>

<style scoped>

</style>
