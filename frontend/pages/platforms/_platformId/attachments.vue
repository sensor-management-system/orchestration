<!--
SPDX-FileCopyrightText: 2020 - 2021
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

import { LoadPlatformAttachmentsAction } from '@/store/platforms'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('platforms', ['loadPlatformAttachments']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformAttachmentsPage extends Vue {
  // vuex definition for typescript check
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadPlatformAttachments(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  head () {
    return {
      titleTemplate: 'Attachments - %s'
    }
  }
}
</script>
