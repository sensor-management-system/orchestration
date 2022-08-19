<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    />
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import { LoadMountingActionsAction } from '@/store/configurations'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator },
  methods: { ...mapActions('configurations', ['loadMountingActions']) }
})
export default class ConfigurationPlatformsAndDevices extends Vue {
  loadMountingActions!: LoadMountingActionsAction
  private isLoading: boolean = false
  head () {
    return {
      titleTemplate: 'Platforms and Devices - %s'
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async created () {
    try {
      this.isLoading = true
      await this.loadMountingActions(this.configurationId)
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of mounting actions failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>
