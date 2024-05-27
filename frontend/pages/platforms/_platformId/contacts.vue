<!--
SPDX-FileCopyrightText: 2020 - 2022
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

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

import { LoadPlatformContactRolesAction } from '@/store/platforms'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('platforms', ['loadPlatformContactRoles']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformContactsPage extends Vue {
  // vuex definition for typescript check
  loadPlatformContactRoles!: LoadPlatformContactRolesAction
  loadCvContactRoles!: LoadCvContactRolesAction
  setLoading!: SetLoadingAction

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadPlatformContactRoles(this.platformId),
        this.loadCvContactRoles()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  head () {
    return {
      titleTemplate: 'Contacts - %s'
    }
  }
}
</script>
