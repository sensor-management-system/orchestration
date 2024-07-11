<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
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

import { LoadAllPlatformActionsAction } from '@/store/platforms'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('platforms', ['loadAllPlatformActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformActionsPage extends Vue {
  // vuex definition for typescript check
  loadAllPlatformActions!: LoadAllPlatformActionsAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadAllPlatformActions(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch actions')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  head () {
    return {
      titleTemplate: 'Actions - %s'
    }
  }
}
</script>
