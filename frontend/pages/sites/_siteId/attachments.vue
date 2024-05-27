<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
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

import { LoadSiteAttachmentsAction } from '@/store/sites'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('sites', ['loadSiteAttachments']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteAttachmentsPage extends Vue {
  // vuex definition for typescript check
  loadSiteAttachments!: LoadSiteAttachmentsAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      await this.loadSiteAttachments(this.siteId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId (): string {
    return this.$route.params.siteId
  }

  head () {
    return {
      titleTemplate: 'Attachments - %s'
    }
  }
}
</script>
