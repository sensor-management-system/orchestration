<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020,2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
<!--    <ConfigurationsSearch-->
<!--      :active-tab="activeTab"-->
<!--      load-initial-data-->
<!--      :delete-callback="deleteConfiguration"-->
<!--      @change-active-tab="activeTab = $event"-->
<!--    />-->
    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="configurations.length <=0 && !loading">
      <p class="text-center">
        There are no platforms that match your search criteria.
      </p>
    </div>
    <div
      v-if="configurations.length >0"
    >
      <v-subheader>
        <template v-if="configurations.length == 1">
          1 configuration found
        </template>
        <template v-else>
          {{ configurations.length }} configurations found
        </template>
        <v-spacer />

<!--        <template v-if="platforms.length>0">-->
<!--          <v-dialog v-model="processing" max-width="100">-->
<!--            <v-card>-->
<!--              <v-card-text>-->
<!--                <div class="text-center pt-2">-->
<!--                  <v-progress-circular indeterminate />-->
<!--                </div>-->
<!--              </v-card-text>-->
<!--            </v-card>-->
<!--          </v-dialog>-->
<!--          <v-menu-->
<!--            close-on-click-->
<!--            close-on-content-click-->
<!--            offset-x-->
<!--            left-->
<!--            z-index="999"-->
<!--          >-->
<!--            <template #activator="{ on }">-->
<!--              <v-btn-->
<!--                icon-->
<!--                v-on="on"-->
<!--              >-->
<!--                <v-icon-->
<!--                  dense-->
<!--                >-->
<!--                  mdi-file-download-->
<!--                </v-icon>-->
<!--              </v-btn>-->
<!--            </template>-->
<!--            <v-list>-->
<!--              <v-list-item-->
<!--                dense-->
<!--                @click.prevent="exportCsv"-->
<!--              >-->
<!--                <v-list-item-content>-->
<!--                  <v-list-item-title>-->
<!--                    <v-icon-->
<!--                      left-->
<!--                    >-->
<!--                      mdi-table-->
<!--                    </v-icon>-->
<!--                    CSV-->
<!--                  </v-list-item-title>-->
<!--                </v-list-item-content>-->
<!--              </v-list-item>-->
<!--            </v-list>-->
<!--          </v-menu>-->
<!--        </template>-->
      </v-subheader>


      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
      <BaseList
        :list-items="configurations"
      >
        <template #list-item="{item}">
          <ConfigurationsListItem
            :configuration="item"
          >
            <template #dot-menu-items>
              <DotMenuActionDelete
                :readonly="!$auth.loggedIn"
                @click="initDeleteDialog(item)"
                />
            </template>
          </ConfigurationsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <ConfigurationsDeleteDialog
      v-model="showDeleteDialog"
      :configuration-to-delete="configurationToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <v-btn
      v-if="$auth.loggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      nuxt
      to="/configurations/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Configuration } from '@/models/Configuration'

import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import { mapActions, mapState } from 'vuex'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

@Component({
  components: {
    DotMenuActionDelete,
    ConfigurationsDeleteDialog,
    ConfigurationsListItem,
    BaseList
  },
  computed:mapState('configurations',['configurations','pageNumber','pageSize','totalPages']),
  methods:mapActions('configurations',['searchConfigurationsPaginated','setPageNumber'])
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private searchText: string | null = null
  private loading=false

  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  async created () {
    this.initializeAppBar()
    await this.runInitialSearch()
  }

  get searchParams() : IConfigurationSearchParams{ //Todo rest
    return {
      searchText: this.searchText,
      states:[],
      projects:[]
    }
  }
  get page(){
    return this.pageNumber;
  }

  set page(newVal){
    this.setPageNumber(newVal);
  }

  async runInitialSearch() {
    //todo an andere entitäten angleichen
    await this.runSearch()
    }

  async runSearch() {
    try {
      this.loading=true
      this.searchConfigurationsPaginated(this.searchParams);
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    }finally {
      this.loading=false
    }
    }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Search',
        'Extended Search'
      ],
      title: 'Configurations'
    })
  }

  initDeleteDialog (configuration: Configuration) {
    this.showDeleteDialog = true
    this.configurationToDelete = configuration
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.configurationToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.configurationToDelete === null || this.configurations.id === null) {
      this.closeDialog()
      return
    }
    try {
      //Todo
      this.loading = true
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    } catch {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    }finally {
      this.loading = false
      this.closeDialog()
    }
  }
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>
