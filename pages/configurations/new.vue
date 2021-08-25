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
          :to="'/configurations'"
          @save="save()"
        />
      </v-card-actions>
      <ConfigurationsBasicDataForm
        ref="basicDataForm"
        v-model="configuration"
        :readonly="false"
      />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          :to="'/configurations'"
          @save="save()"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'

@Component({
  components: { ConfigurationsBasicDataForm, SaveAndCancelButtons, ProgressIndicator }
})
export default class ConfigurationNewPage extends Vue {
  private configuration: Configuration = new Configuration()
  private isLoading: boolean =false

  created () {
    this.$store.commit('configurations/setConfiguration', this.configuration)
  }

  mounted () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  private initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
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
          name: 'Actions',
          disabled: true
        }
      ],
      title: 'Add Configuration'
    })
  }

  async save () {
    if (!(this.$refs.basicDataForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      const savedConfiguration = await this.$api.configurations.save(this.configuration)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      await this.$router.push('/configurations/' + savedConfiguration.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>

<style scoped>

</style>
