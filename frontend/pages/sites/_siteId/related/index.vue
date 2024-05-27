<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
