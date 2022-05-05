<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          save-btn-text="Apply"
          :to="`/configurations/${configurationId}/basic`"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Configuration, IConfiguration } from '@/models/Configuration'
@Component({
  components: { ProgressIndicator, ConfigurationsBasicDataForm, SaveAndCancelButtons },
  middleware: ['auth'],
  computed: mapState('configurations', ['configuration']),
  methods: mapActions('configurations', ['saveConfiguration', 'loadConfiguration'])
})
export default class ConfigurationEditBasicPage extends Vue {
  private configurationCopy: Configuration = new Configuration()
  private isLoading: boolean = false

  // vuex definition for typescript check
  configuration!: IConfiguration
  saveConfiguration!: (configuration: Configuration) => void
  loadConfiguration!: (id: string) => void

  created () {
    this.configurationCopy = Configuration.createFromObject(this.configuration)
  }

  get configurationId () {
    return this.$route.params.configurationId
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      await this.saveConfiguration(this.configurationCopy)
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Configuration updated')
      await this.$router.push('/configurations/' + this.configurationId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>
