<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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

import { SetTitleAction, SetTabsAction } from '@/store/appbar'

import { Configuration } from '@/models/Configuration'

import { CreatePidAction, SaveConfigurationAction } from '@/store/configurations'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'

@Component({
  components: {
    ConfigurationsBasicDataForm,
    NonModelOptionsForm,
    SaveAndCancelButtons,
    ProgressIndicator
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['saveConfiguration', 'createPid']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])
  }
})
export default class ConfigurationNewPage extends Vue {
  private configuration: Configuration = new Configuration()
  private isLoading: boolean = false
  private createOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  initConfigurationsNewAppBar!: () => void
  saveConfiguration!: SaveConfigurationAction
  createPid!: CreatePidAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction

  created () {
    this.initializeAppBar()
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      const savedConfiguration = await this.saveConfiguration(this.configuration)
      if (this.createOptions.persistentIdentifierShouldBeCreated) {
        savedConfiguration.persistentIdentifier = await this.createPid(savedConfiguration.id)
      }
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      await this.$router.push('/configurations/' + savedConfiguration.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }

  initializeAppBar () {
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
        name:
        'Locations',
        disabled: true
      },
      {
        name:
        'Custom Fields',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      },
      {
        name:
        'Actions',
        disabled: true
      }
    ])
    this.setTitle('New Configuration')
  }
}
</script>

<style scoped>

</style>
