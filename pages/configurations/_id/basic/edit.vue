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
          v-if="isLoggedIn"
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
          v-if="isLoggedIn"
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
  readonly value!:Configuration

  private configurationCopy: Configuration = new Configuration()
  private isLoading: boolean =false
  private formIsValid: boolean = true

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

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  @Watch('value', { immediate: true, deep: true })
  onConfigurationChanged (val: Configuration) {
    this.configurationCopy = Configuration.createFromObject(val)
  }
}
</script>
