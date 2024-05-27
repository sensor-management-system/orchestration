<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-alert text type="info">
      The feature to link measured quantities to datastreams of time series management systems is currently in an experimental phase.
      It could be that some of the functionality is only accessible from your institutes intranet.
      If you encounter any problems, feel free to use the gitlab service desk &amp; report the issue.
    </v-alert>
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/tsm-linking/new'"
        >
          Add TSM Linking
        </v-btn>
      </v-card-actions>
    </v-card>
    <TsmLinkingOverviewTable />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import TsmLinkingOverviewTable from '@/components/configurations/tsmLinking/TsmLinkingOverviewTable.vue'

@Component({
  components: { TsmLinkingOverviewTable }
})
export default class ConfigurationShowTsmLinkingPage extends Vue {
  @InjectReactive()
    editable!: boolean

  get configurationId (): string {
    return this.$route.params.configurationId
  }
}
</script>

<style scoped>

</style>
