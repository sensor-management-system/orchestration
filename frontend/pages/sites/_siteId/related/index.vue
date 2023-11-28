<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <SiteRelatedData
      v-if="site"
      v-model="site"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import SiteRelatedData from '@/components/sites/SiteRelatedData.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { LoadSiteAction, SitesState } from '@/store/sites'

@Component({
  components: {
    SiteRelatedData
  },
  computed: mapState('sites', ['site']),
  methods: {
    ...mapActions('sites', [
      'loadSite'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteShowRelatedPage extends Vue {
  // vuex definition for typescript check
  site!: SitesState['site']
  loadSite!: LoadSiteAction
  setLoading!: SetLoadingAction

  get siteId () {
    return this.$route.params.siteId
  }
}
</script>
