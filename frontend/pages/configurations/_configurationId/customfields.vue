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

import { LoadConfigurationCustomFieldsAction } from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('configurations', ['loadConfigurationCustomFields']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationCustomFieldsPage extends Vue {
  // vuex definition for typescript check
  loadConfigurationCustomFields!: LoadConfigurationCustomFieldsAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadConfigurationCustomFields(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch custom fields')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  head () {
    return {
      titleTemplate: 'Custom Fields - %s'
    }
  }
}
</script>
