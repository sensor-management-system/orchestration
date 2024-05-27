<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <div v-if="innerSites.length > 0 || siteConfigurations.length > 0">
      <v-row v-if="innerSites.length>0">
        <v-col cols="12">
          <label>Sites & labs included in this site / lab</label>
          <div>
            <BaseList
              :list-items="innerSites"
            >
              <template #list-item="{item}">
                <SitesListItem
                  :site="item"
                />
              </template>
            </BaseList>
          </div>
        </v-col>
      </v-row>
      <v-row v-if="siteConfigurations.length>0">
        <v-col cols="12">
          <label>Configurations on site / lab</label>
          <div>
            <BaseList
              :list-items="siteConfigurations"
            >
              <template #list-item="{item}">
                <ConfigurationsListItem
                  :configuration="item"
                />
              </template>
            </BaseList>
          </div>
        </v-col>
      </v-row>
    </div>
    <hint-card v-else>
      There are no related sites, labs or configurations for this site / lab.
    </hint-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Site } from '@/models/Site'

import BaseList from '@/components/shared/BaseList.vue'
import HintCard from '@/components/HintCard.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import SitesListItem from '@/components/sites/SitesListItem.vue'

import { SearchSitesAction, SitesState } from '@/store/sites'

@Component({
  components: {
    BaseList,
    ConfigurationsListItem,
    HintCard,
    SitesListItem
  },
  computed: {
    ...mapState('sites', ['siteConfigurations']),
    ...mapState('sites', ['sites'])
  },
  methods: {
    ...mapActions('sites', ['searchSites'])
  }
})
export default class SiteRelatedData extends Vue {
  @Prop({
    default: () => new Site(),
    required: true,
    type: Site
  })
  readonly value!: Site

  // vuex definition for typescript check
  siteConfigurations!: SitesState['siteConfigurations']

  // vuex definition for typescript check
  sites!: SitesState['sites']
  searchSites!: SearchSitesAction

  async mounted () {
    try {
      await this.searchSites()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load sites')
    }
  }

  get innerSites () {
    return this.sites.filter(x => x.outerSiteId === this.value.id)
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
