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
      <NuxtChild/>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Platform } from '@/models/Platform'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions } from 'vuex'

@Component({
  components: {
    ProgressIndicator
  },
  methods: {
    ...mapActions('platforms', ['loadPlatform']),
    ...mapActions('appbar', ['initPlatformsPlatformIdAppBar', 'setDefaults'])
  }
})
export default class PlatformPage extends Vue {
  private isLoading: boolean = false

  async created () {
    try {
      this.isLoading = true
      this.initPlatformsPlatformIdAppBar(this.platformId)
      await this.loadPlatform({
          platformId: this.platformId,
          includeContacts: false,
          includePlatformAttachments: false
        }
      )
      if(this.isBasePath()){
        this.$router.replace('/platforms/' + this.platformId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading platform failed')
    } finally {
      this.isLoading = false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get platformId () {
    return this.$route.params.platformId
  }

  isBasePath () {
    return this.$route.path === '/platforms/' + this.platformId || this.$route.path === '/platforms/' + this.platformId + '/'
  }
}
</script>
