<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/tsm-linking/new'"
      >
        Add Data Linking
      </v-btn>
    </v-card-actions>
    <base-expandable-list-item>
      <template #header>
        <h2>Filter</h2>
        <span class="pl-2">(click to expand)</span>
      </template>
      <template #expandable>
        <TsmLinkingFilters ref="tsmLinkingfilter" />
      </template>
    </base-expandable-list-item>
    <TsmLinkingOverviewTable
      class="ma-2"
      :devices="availableDevices"
    />
    <v-card-actions
      v-if="filteredLinkings.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/tsm-linking/new'"
      >
        Add Data Linking
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'
import TsmLinkingOverviewTable from '@/components/configurations/tsmLinking/TsmLinkingOverviewTable.vue'
import { AvailableDevicesGetter } from '@/store/configurations'
import DateTimePicker from '@/components/DateTimePicker.vue'
import TsmLinkingFilters from '@/components/configurations/tsmLinking/TsmLinkingFilters.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import { FilteredLinkingsGetter } from '@/store/tsmLinking'

@Component({
  components: { BaseExpandableListItem, TsmLinkingFilters, DateTimePicker, TsmLinkingOverviewTable },
  computed: {
    ...mapGetters('configurations', ['availableDevices']),
    ...mapGetters('tsmLinking', ['filteredLinkings'])
  }
})
export default class ConfigurationShowTsmLinkingPage extends Vue {
  @InjectReactive()
    editable!: boolean

  availableDevices!: AvailableDevicesGetter
  filteredLinkings!: FilteredLinkingsGetter

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  mounted () {
    if (this.$refs.tsmLinkingfilter) {
      const tsmLinkingfilter = this.$refs.tsmLinkingfilter as Vue & {clearFilter: () => void}
      tsmLinkingfilter.clearFilter()
    }
  }
}
</script>

<style scoped>

</style>
