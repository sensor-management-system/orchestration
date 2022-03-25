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
          v-if="$auth.loggedIn"
          :to="`/configurations/${configurationId}/basic`"
          @save="save()"
        />
      </v-card-actions>
      <ConfigurationsBasicDataForm
        ref="basicDataForm"
        v-model="configurationCopy"
        :readonly="false"
        :form-is-valid="formIsValid"
      />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          v-if="$auth.loggedIn"
          :to="`/configurations/${configurationId}/basic`"
          @save="save()"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import { Configuration } from '@/models/Configuration'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
@Component({
  components: { ProgressIndicator, ConfigurationsBasicDataForm, SaveAndCancelButtons }
})
export default class ConfigurationEditBasicPage extends Vue {
  @Prop({
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

  private configurationCopy: Configuration = new Configuration()
  private isLoading: boolean = false
  private formIsValid: boolean = true

  head () {
    return {
      titleTemplate: 'Basic Data - %s'
    }
  }

  get configurationId () {
    return this.$route.params.id
  }

  created () {
    this.configurationCopy = Configuration.createFromObject(this.value)
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      this.$store.commit('configurations/setConfiguration', this.configurationCopy)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      await this.$router.push('/configurations/' + this.$store.state.configurations.configuration.id + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }

  @Watch('value', { immediate: true, deep: true })
  onConfigurationChanged (val: Configuration) {
    this.configurationCopy = Configuration.createFromObject(val)
  }
}
</script>
