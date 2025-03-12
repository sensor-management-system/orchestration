<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-tabs v-model="tab">
      <v-tab>Basic Search</v-tab>
      <v-tab>Extended Search</v-tab>
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <ConfigurationBasicSearch
            ref="configurationBasicSearch"
          />
        </v-tab-item>
        <v-tab-item>
          <ConfigurationExtendedSearch
            ref="configurationExtendedSearch"
          />
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
    <v-row
      no-gutters
      class="mt-10"
    >
      <v-col
        cols="12"
        md="3"
      >
        <ConfigurationFoundEntries />
      </v-col>
      <v-spacer />
      <v-col
        cols="12"
        md="6"
      >
        <ConfigurationPagination
          ref="configurationPagination"
          @input="updateSearch"
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
        class="flex-grow-1 flex-shrink-0"
      >
        <v-subheader>
          <ConfigurationPageSizeSelect
            @input="setPageAndUpdateSearch"
          />
        </v-subheader>
      </v-col>
    </v-row>

    <base-list :list-items="configurations">
      <template #list-item="{item}">
        <configurations-list-item
          :configuration="item"
          target="_blank"
        >
          <template #additional-actions>
            <v-btn
              color="primary"
              text
              small
              @click.stop.prevent
              @click="selectConfiguration(item)"
            >
              Select
            </v-btn>
          </template>
        </configurations-list-item>
      </template>
    </base-list>
  </div>
</template>

<script lang="ts">
import { mapState } from 'vuex'

import { Component, Vue } from 'nuxt-property-decorator'
import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import ConfigurationBasicSearch from '@/components/configurations/ConfigurationBasicSearch.vue'
import ConfigurationPageSizeSelect from '@/components/configurations/ConfigurationPageSizeSelect.vue'
import ConfigurationPagination from '@/components/configurations/ConfigurationPagination.vue'
import ConfigurationFoundEntries from '@/components/configurations/ConfigurationFoundEntries.vue'
import { Configuration } from '@/models/Configuration'
import ConfigurationExtendedSearch from '@/components/configurations/ConfigurationExtendedSearch.vue'

@Component({
  components: {
    ConfigurationExtendedSearch,
    ConfigurationFoundEntries,
    ConfigurationPagination,
    ConfigurationPageSizeSelect,
    ConfigurationBasicSearch,
    ConfigurationsListItem,
    BaseList
  },
  computed: {
    ...mapState('configurations', [
      'configurations'
    ])
  }
})
export default class ReuseConfigurationSearch extends Vue {
  private tab = 0

  async created () {
    await this.$nextTick()
    await this.updateSearch()
  }

  async updateSearch () {
    if (this.tab === 0) {
      await (this.$refs.configurationBasicSearch as Vue & { search: () => void }).search()
    } else if (this.tab === 1) {
      await (this.$refs.configurationExtendedSearch as Vue & { search: () => void }).search()
    }
  }

  setPageAndUpdateSearch () {
    (this.$refs.configurationPagination as Vue & { setPage: (val: number) => void }).setPage(1)
    this.updateSearch()
  }

  selectConfiguration (configuration: Configuration | null) {
    this.$emit('selected', configuration)
  }
}
</script>

<style scoped>

</style>
