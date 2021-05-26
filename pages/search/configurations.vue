<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
            <v-text-field v-model="searchText" label="Label" placeholder="Label of configuration" @keydown.enter="basicSearch" />
          </v-col>
          <v-col cols="12" md="2">
            <v-btn
              color="primary"
              @click="basicSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
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
            <v-text-field v-model="searchText" label="Label" placeholder="Label of configuration" @keydown.enter="extendedSearch" />
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
            <StringSelect
              v-model="selectedLocationTypes"
              label="Select a location type"
              :items="locationTypes"
              color="blue"
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
          <v-col cols="12" md="3">
            <v-btn
              color="primary"
              @click="extendedSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              @click="clearExtendedSearch"
            >
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>

    <div v-if="loading">
      <div class="text-center pt-2">
        <v-progress-circular indeterminate />
      </div>
    </div>
    <div v-if="searchResults.length == 0 && !loading">
      <v-card>
        <v-card-text>
          <p class="text-center">
            There are no configurations that match our your search criteria
          </p>
        </v-card-text>
      </v-card>
    </div>
    <div v-if="searchResults.length && !loading">
      <v-subheader>
        <template v-if="totalCount == 1">
          1 configuration found
        </template>
        <template v-else>
          {{ totalCount }} configurations found
        </template>
        <v-spacer />

        <template v-if="lastActiveSearcher != null">
          <v-dialog v-model="processing" max-width="100">
            <v-card>
              <v-card-text>
                <div class="text-center pt-2">
                  <v-progress-circular indeterminate />
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-menu
            close-on-click
            close-on-content-click
            offset-x
            left
            z-index="999"
          >
            <template #activator="{ on }">
              <v-btn
                icon
                v-on="on"
              >
                <v-icon
                  dense
                >
                  mdi-file-download
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                dense
                @click.prevent="exportCsv"
              >
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon
                      left
                    >
                      mdi-table
                    </v-icon>
                    CSV
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-subheader>
      <v-hover
        v-for="result in searchResults"
        v-slot="{ hover }"
        :key="result.id"
      >
        <v-card
          :disabled="loading"
          :elevation="hover ? 6 : 2"
          class="ma-2"
        >
          <v-card-text
            @click.stop.prevent="showResultItem(result.id)"
          >
            <v-row
              no-gutters
            >
              <v-col>
                <StatusBadge
                  :value="result.status"
                >
                  <div class="text-caption">
                    {{ getLocationType(result) }}
                  </div>
                </StatusBadge>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <v-menu
                  close-on-click
                  close-on-content-click
                  offset-x
                  left
                  z-index="999"
                >
                  <template #activator="{ on }">
                    <v-btn
                      data-role="property-menu"
                      icon
                      small
                      v-on="on"
                    >
                      <v-icon
                        dense
                        small
                      >
                        mdi-dots-vertical
                      </v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      :disabled="!isLoggedIn"
                      dense
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          :class="isLoggedIn ? 'text' : 'grey-text'"
                        >
                          <v-icon
                            left
                            small
                            :color="isLoggedIn ? 'black' : 'grey'"
                          >
                            mdi-content-copy
                          </v-icon>
                          Copy
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item
                      :disabled="!isLoggedIn"
                      dense
                      @click="showDeleteDialogFor(result.id)"
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          :class="isLoggedIn ? 'red--text' : 'grey--text'"
                        >
                          <v-icon
                            left
                            small
                            :color="isLoggedIn ? 'red' : 'grey'"
                          >
                            mdi-delete
                          </v-icon>
                          Delete
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                {{ getTextOrDefault(result.label, 'Configuration') }}
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <v-btn
                  :to="'/configurations/' + result.id"
                  color="primary"
                  text
                  @click.stop.prevent
                >
                  View
                </v-btn>
                <v-btn
                  icon
                  @click.stop.prevent="showResultItem(result.id)"
                >
                  <v-icon>{{ isResultItemShown(result.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
          <v-expand-transition>
            <v-card
              v-show="isResultItemShown(result.id)"
              flat
              tile
              color="grey lighten-5"
            >
              <v-card-text>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Start:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ result.startDate | formatDate }}
                  </v-col>
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    End:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ result.endDate | formatDate }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Project:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.projectName, '-') }}
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-expand-transition>
          <v-dialog v-model="showDeleteDialog[result.id]" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete configuration
              </v-card-title>
              <v-card-text>
                Do you really want to delete the configuration <em>{{ result.label }}</em>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="hideDeleteDialogFor(result.id)"
                >
                  No
                </v-btn>
                <v-spacer />
                <v-btn
                  color="error"
                  text
                  @click="deleteAndCloseDialog(result.id)"
                >
                  <v-icon left>
                    mdi-delete
                  </v-icon>
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-hover>
    </div>
    <v-btn
      v-if="isLoggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/configurations"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'
import { DateTime } from 'luxon'

import ProjectSelect from '@/components/ProjectSelect.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import StringSelect from '@/components/StringSelect.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Configuration } from '@/models/Configuration'
import { StationaryLocation, DynamicLocation, LocationType } from '@/models/Location'
import { Project } from '@/models/Project'

import { ConfigurationSearcher } from '@/services/sms/ConfigurationApi'

import { dateToString } from '@/utils/dateHelper'

@Component({
  filters: {
    formatDate: (possibleDate: DateTime | null) => {
      if (possibleDate != null) {
        // TODO: handle also the time
        return dateToString(possibleDate)
      }
      return '-'
    }
  },
  components: {
    ProjectSelect,
    StatusBadge,
    StringSelect
  }
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private pageSize: number = 20
  private loading: boolean = true
  private processing: boolean = false

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Configuration> = null
  private lastActiveSearcher: ConfigurationSearcher | null = null

  private selectedConfigurationStates: string[] = []
  private selectedLocationTypes: string[] = []
  private selectedProjects: Project[] = []

  private configurationStates: string[] = []
  private locationTypes: string[] = []
  private projects: Project[] = []

  private searchResults: Configuration[] = []
  private searchText: string | null = null

  private showDeleteDialog: { [id: string]: boolean} = {}

  private searchResultItemsShown: { [id: string]: boolean} = {}

  created () {
    this.initializeAppBar()
  }

  mounted () {
    this.$api.configurationStates.findAll().then((foundStates) => {
      this.configurationStates = foundStates
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading configuration states failed')
    })
    this.locationTypes = [
      LocationType.Stationary,
      LocationType.Dynamic
    ]
    this.$api.projects.findAll().then((foundProjects) => {
      this.projects = foundProjects
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading of projects failed')
    })
    this.runSelectedSearch()

    window.onscroll = () => {
      const isOnBottom = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight

      if (isOnBottom && this.canLoadNext()) {
        this.loadNext()
      }
    }
  }

  beforeDestroy () {
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Search',
        'Extended Search'
      ],
      title: 'Configurations',
      saveBtnHidden: true,
      cancelBtnHidden: true
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  runSelectedSearch () {
    if (this.activeTab === 0) {
      this.basicSearch()
    } else {
      this.extendedSearch()
    }
  }

  basicSearch () {
    this.runSearch(this.searchText, [], [], [])
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch () {
    this.runSearch(
      this.searchText,
      this.selectedConfigurationStates,
      this.selectedLocationTypes,
      this.selectedProjects
    )
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedConfigurationStates = []
    this.selectedLocationTypes = []
    this.selectedProjects = []
  }

  runSearch (
    searchText: string | null,
    configurationStates: string[],
    locationTypes: string[],
    projects: Project[]
  ) {
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
    this.lastActiveSearcher = this.$api.configurations
      .newSearchBuilder()
      .withText(searchText)
      .withOneStatusOf(configurationStates)
      .withOneLocationTypeOf(locationTypes)
      .withOneMatchingProjectOf(projects)
      .build()
    this.lastActiveSearcher
      .findMatchingAsPaginationLoader(this.pageSize)
      .then(this.loadUntilWeHaveSomeEntries).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of configurations failed')
      })
  }

  loadUntilWeHaveSomeEntries (loader: IPaginationLoader<Configuration>) {
    this.loader = loader
    this.loading = false
    this.searchResults = [...this.searchResults, ...loader.elements]
    this.totalCount = loader.totalCount

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader)
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional configurations failed')
      })
    }
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
        this.totalCount = nextLoader.totalCount
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional configurations failed')
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  exportCsv () {
    if (this.lastActiveSearcher != null) {
      this.processing = true
      this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
        this.processing = false
        saveAs(blob, 'configurations.csv')
      }).catch((_err) => {
        this.processing = false
        this.$store.commit('snackbar/setError', 'CSV export failed')
      })
    }
  }

  deleteAndCloseDialog (id: string) {
    this.$api.configurations.deleteById(id).then(() => {
      this.showDeleteDialog = {}

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
        this.totalCount -= 1
      }

      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    }).catch((_error) => {
      this.showDeleteDialog = {}
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    })
  }

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
  }

  showResultItem (id: string) {
    const show = !!this.searchResultItemsShown[id]
    Vue.set(this.searchResultItemsShown, id, !show)
  }

  isResultItemShown (id: string): boolean {
    return this.searchResultItemsShown[id]
  }

  unsetResultItemsShown (): void {
    this.searchResultItemsShown = {}
  }

  getTextOrDefault = (text: string, defaultValue: string): string => text || defaultValue

  getLocationType (configuration: Configuration): string {
    if (configuration.location instanceof StationaryLocation) {
      return LocationType.Stationary
    }
    if (configuration.location instanceof DynamicLocation) {
      return LocationType.Dynamic
    }
    return ''
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>
