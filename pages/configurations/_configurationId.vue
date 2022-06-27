<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
    />
    <v-card flat>
      <NuxtChild />
      <modification-info
        v-if="configuration"
        v-model="configuration"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, ProvideReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter } from '@/store/permissions'

import { Configuration } from '@/models/Configuration'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ModificationInfo from '@/components/ModificationInfo.vue'

@Component({
  components: {
    ProgressIndicator,
    ModificationInfo
  },
  computed: {
    ...mapState('configurations', ['configuration']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfiguration']),
    ...mapActions('appbar', ['initConfigurationsConfigurationIdAppBar', 'setDefaults'])
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private isLoading: boolean = false

  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  // vuex definition for typescript check
  configuration!: Configuration | null
  initConfigurationsConfigurationIdAppBar!: (id: string) => void
  setDefaults!: () => void
  loadConfiguration!: (id: string) => void
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter

  async created () {
    try {
      this.isLoading = true
      this.initConfigurationsConfigurationIdAppBar(this.configurationId)
      await this.loadConfiguration(this.configurationId)

      if (!this.configuration) {
        throw new Error('initialization of configuration failed')
      }

      if (!this.canAccessEntity(this.configuration)) {
        this.$router.replace('/configurations/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this configuration.')
        return
      }

      this.editable = this.canModifyEntity(this.configuration)
      this.deletable = this.canDeleteEntity(this.configuration)

      if (this.isBasePath()) {
        this.$router.replace('/configurations/' + this.configurationId + '/basic')
      }
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Loading configuration failed')
    } finally {
      this.isLoading = false
    }
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  get configurationId () {
    return this.$route.params.configurationId
  }

  isBasePath () {
    return this.$route.path === '/configurations/' + this.configurationId ||
      this.$route.path === '/configurations/' + this.configurationId + '/'
  }
}
</script>
