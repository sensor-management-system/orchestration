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
      <NuxtChild/>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Configuration } from '@/models/Configuration'
import { mapActions } from 'vuex'

@Component({
  components: {
    ProgressIndicator
  },
  methods:mapActions('configurations',['loadConfiguration'])
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private isLoading: boolean = false

  get configurationId () {
    return this.$route.params.configurationId
  }

  async created () {
    this.initializeAppBar()
    try {
      this.isLoading = true
      await this.loadConfiguration(this.configurationId)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Loading configuration failed')
    } finally {
      this.isLoading = false
    }

    if (this.isBasePath()) { // Todo prüfen ob man das wirklich braucht, oder gleich direkt den redirect machen
      this.$router.replace('/configurations/' + this.configurationId + '/basic')
    }
  }

  isBasePath () {
    return this.$route.path === '/configurations/' + this.configurationId ||
      this.$route.path === '/configurations/' + this.configurationId + '/'
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/configurations/' + this.$route.params.id + '/basic',
          name: 'Basic Data'
        },
        {
          to: '/configurations/' + this.$route.params.id + '/contacts',
          name: 'Contacts'
        },
        {
          to: '/configurations/' + this.$route.params.id + '/platforms-and-devices',
          name: 'Platforms and Devices'
        },
        {
          to: '/configurations/' + this.$route.params.id + '/locations',
          name: 'Locations'
        },
        {
          to: '/configurations/' + this.$route.params.id + '/actions',
          name: 'Actions'
        }
      ],
      title: this.configuration.label || 'Configuration'
    })
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }
}
</script>
