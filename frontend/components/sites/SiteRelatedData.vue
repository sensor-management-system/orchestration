<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
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
