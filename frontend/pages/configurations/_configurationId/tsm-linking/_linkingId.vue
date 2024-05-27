<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <NuxtChild v-if="linking" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import {
  ITsmLinkingState,
  LoadConfigurationTsmLinkingAction
} from '@/store/tsmLinking'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  computed: {
    ...mapState('tsmLinking', ['linking'])
  },
  methods: {
    ...mapActions('tsmLinking', [
      'loadConfigurationTsmLinking'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class LinkingIdPage extends Vue {
  // vuex definition for typescript check
  linking!: ITsmLinkingState['linking']
  loadConfigurationTsmLinking!: LoadConfigurationTsmLinkingAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      this.$store.commit('tsmLinking/setLinking', null)
      await this.loadConfigurationTsmLinking(this.linkingId)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Loading of linking failed')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get linkingId (): string {
    return this.$route.params.linkingId
  }
}
</script>

<style scoped>

</style>
