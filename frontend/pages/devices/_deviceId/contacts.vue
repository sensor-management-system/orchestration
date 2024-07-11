<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
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

import { LoadDeviceContactRolesAction } from '@/store/devices'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('devices', ['loadDeviceContactRoles']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceContactsPage extends Vue {
  // vuex definition for typescript check
  loadDeviceContactRoles!: LoadDeviceContactRolesAction
  loadCvContactRoles!: LoadCvContactRolesAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDeviceContactRoles(this.deviceId),
        this.loadCvContactRoles()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  head () {
    return {
      titleTemplate: 'Contacts - %s'
    }
  }
}
</script>
