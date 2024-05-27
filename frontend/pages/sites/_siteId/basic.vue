<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <NuxtChild />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import { LoadSiteUsagesAction, LoadSiteTypesAction } from '@/store/vocabulary'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('vocabulary', ['loadSiteUsages', 'loadSiteTypes']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteBasicPage extends Vue {
  head () {
    return {
      titleTemplate: 'Basic Data - %s'
    }
  }

  // vuex definition for typescript check
  loadSiteUsages!: LoadSiteUsagesAction
  loadSiteTypes!: LoadSiteTypesAction
  setLoading!: SetLoadingAction

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadSiteUsages(),
        this.loadSiteTypes()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch types or usages')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
