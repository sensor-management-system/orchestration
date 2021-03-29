<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
      <NuxtChild
        v-model="platform"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { Platform } from '@/models/Platform'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class PlatformPage extends Vue {
  private platform: Platform = new Platform()
  private isLoading: boolean = true

  created () {
    if (this.isBasePath()) {
      this.$router.push('/platforms/' + this.platformId + '/basic')
    }
  }

  mounted () {
    this.initializeAppBar()

    this.$api.platforms.findById(this.platformId).then((platform) => {
      this.platform = platform
      this.isLoading = false
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading platform failed')
      this.isLoading = false
    })
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/platforms/' + this.platformId + '/basic',
          name: 'Basic Data'
        },
        {
          to: '/platforms/' + this.platformId + '/contacts',
          name: 'Contacts'
        },
        {
          to: '/platforms/' + this.platformId + '/attachments',
          name: 'Attachments'
        }
      ],
      title: 'Platforms'
    })
  }

  isBasePath () {
    return this.$route.path === '/platforms/' + this.platformId || this.$route.path === '/platforms/' + this.platformId + '/'
  }

  get platformId () {
    return this.$route.params.platformId
  }

  @Watch('platform', { immediate: true, deep: true })
  // @ts-ignore
  onPlatformChanged (val: Platform) {
    if (val.id) {
      this.$store.commit('appbar/setTitle', val?.shortName || 'Add Platform')
    }
  }
}
</script>
