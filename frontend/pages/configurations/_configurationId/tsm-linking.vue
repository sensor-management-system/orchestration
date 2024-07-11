<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import { LoadConfigurationTsmLinkingsAction, LoadTsmEndpointsAction } from '@/store/tsmLinking'
import { LoadLicensesAction } from '@/store/vocabulary'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  middleware: ['auth'],
  methods: {
    ...mapActions('tsmLinking', ['loadConfigurationTsmLinkings', 'loadTsmEndpoints']),
    ...mapActions('vocabulary', ['loadLicenses']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationTsmLinking extends Vue {
  // vuex definition for typescript check
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  loadTsmEndpoints!: LoadTsmEndpointsAction
  loadLicenses!: LoadLicensesAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadConfigurationTsmLinkings(this.configurationId),
        this.loadTsmEndpoints(),
        this.loadLicenses()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch linkings')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId () {
    return this.$route.params.configurationId
  }

  head () {
    return {
      titleTemplate: 'Data Linking - %s'
    }
  }
}
</script>
