<!--
SPDX-FileCopyrightText: 2020 - 2022
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

import { LoadConfigurationAttachmentsAction } from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('configurations', ['loadConfigurationAttachments']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationAttachmentsPage extends Vue {
  // vuex definition for typescript check
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      await this.loadConfigurationAttachments(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  head () {
    return {
      titleTemplate: 'Attachments - %s'
    }
  }
}
</script>
