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
import { SetLoadingAction } from '@/store/progressindicator'
import { LoadCvContactRolesAction } from '@/store/vocabulary'
import { LoadConfigurationContactRolesAction } from '@/store/configurations'

@Component({
  methods: {
    ...mapActions('configurations', ['loadConfigurationContactRoles']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ContactTab extends Vue {
  // vuex definition for typescript check
  loadConfigurationContactRoles!: LoadConfigurationContactRolesAction
  loadCvContactRoles!: LoadCvContactRolesAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadConfigurationContactRoles(this.configurationId),
        this.loadCvContactRoles()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  head () {
    return {
      titleTemplate: 'Contacts - %s'
    }
  }
}
</script>
