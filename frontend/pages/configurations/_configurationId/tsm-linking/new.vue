<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <NuxtChild
      v-if="configuration"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

@Component({
  computed: {
    ...mapState('configurations', ['configuration'])
  }
})
export default class ConfigurationNewTsmLinkingPageParent extends mixins(CheckEditAccess) {
  created () {
    // reset new linkings to remove cached data
    this.$store.commit('tsmLinking/setNewLinkings', [])
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }
}
</script>

<style scoped>

</style>
