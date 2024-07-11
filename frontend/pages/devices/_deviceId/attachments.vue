<!--
SPDX-FileCopyrightText: 2020 - 2024
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

import { LoadDeviceAttachmentsAction } from '@/store/devices'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('devices', ['loadDeviceAttachments']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceAttachmentsPage extends Vue {
  // vuex definition for typescript check
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      await this.loadDeviceAttachments(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  head () {
    return {
      titleTemplate: 'Attachments - %s'
    }
  }
}
</script>
