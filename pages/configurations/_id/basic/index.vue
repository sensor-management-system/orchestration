<template>
  <v-card flat>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>

    <ConfigurationsBasicData
      v-model="configuration"
      :readonly="true"
    />

    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { Configuration } from '@/models/Configuration'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import ConfigurationsBasicData from '@/components/configurations/ConfigurationsBasicData.vue'
@Component({
  components: { ConfigurationsBasicData, ConfigurationsBasicDataForm }
})
export default class ConfigurationShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  get configuration (): Configuration {
    return this.value
  }

  set configuration (value: Configuration) {
    this.$emit('input', value)
  }

  get configurationId () {
    return this.$route.params.id
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>

<style scoped>

</style>
