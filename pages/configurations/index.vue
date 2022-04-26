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
    <v-tabs-items
      v-model="activeTab"
    >
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchText"
              label="Label"
              placeholder="Label of configuration"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
            cols="12"
            md="7"
            align-self="center"
          >
            <v-btn
              color="primary"
              small
              @click="basicSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearBasicSearch"
            >
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Label"
              placeholder="Label of configuration"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <StringSelect
              v-model="selectedConfigurationStates"
              label="Select a status"
              :items="configurationStates"
              color="green"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <ProjectSelect
              v-model="selectedProjects"
              label="Select a project"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            align-self="center"
          >
            <v-btn
              color="primary"
              small
              @click="extendedSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearExtendedSearch"
            >
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>
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
import { Project } from '@/models/Project'
import StringSelect from '@/components/StringSelect.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'

@Component({
  components: {
    ProjectSelect,
    StringSelect,
    DotMenuActionDelete,
    ConfigurationsDeleteDialog,
    ConfigurationsListItem,
    BaseList
  },
  computed:mapState('configurations',['configurations','pageNumber','pageSize','totalPages','configurationStates']),
  methods:mapActions('configurations',['searchConfigurationsPaginated','setPageNumber','loadConfigurationsStates','deleteConfiguration'])
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private loading=false

  private searchText: string | null = null
  private selectedConfigurationStates: string[] = []
  private selectedProjects: Project[] = []


  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  async created () {
    this.initializeAppBar()
    this.loadConfigurationsStates()
    await this.runInitialSearch()
  }

  get searchParams() : IConfigurationSearchParams{
    return {
      searchText: this.searchText,
      states:this.selectedConfigurationStates,
      projects:this.selectedProjects
    }
  }
  get page(){
    return this.pageNumber;
  }

  set page(newVal){
    this.setPageNumber(newVal);
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  async runInitialSearch() {
    //todo an andere entitäten angleichen
    await this.runSearch()
    }

  basicSearch (): Promise<void> {
    this.selectedSearchManufacturers=[]
    this.selectedSearchStates=[]
    this.selectedSearchPlatformTypes=[]
    this.onlyOwnPlatforms=false
    return this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch (): Promise<void> {
    return this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedConfigurationStates = []
    this.selectedProjects = []
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
      this.loading = true
      this.deleteConfiguration(this.configurationToDelete.id)
      this.runSearch()
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
