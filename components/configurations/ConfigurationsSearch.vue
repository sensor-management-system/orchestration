<template>
  <div>
    <ConfigurationsBasicSearch
      @search="basicSearch"
    />
    <ConfigurationsExtendedSearch
      @search="extendedSearch"
    />
    <div v-if="loading">
      <div class="text-center pt-2">
        <v-progress-circular indeterminate />
      </div>
    </div>
    <div v-if="searchResults.length === 0 && !loading">
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
        {{ numbersFoundMessage }}
        <v-spacer />

        <ConfigurationsDownloader
          v-if="lastActiveSearcher != null"
          :last-active-searcher="lastActiveSearcher"
        />
      </v-subheader>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Project } from '@/models/Project'
import { Configuration } from '@/models/Configuration'
import { IConfigurationSearchOption } from '@/models/SearchTypes'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { ConfigurationSearcher } from '@/services/sms/ConfigurationApi'

import ConfigurationsDownloader from '@/components/configurations/ConfigurationsDownloader.vue'
import ConfigurationsBasicSearch from '@/components/configurations/ConfigurationsBasicSearch.vue'
import ConfigurationsExtendedSearch from '@/components/configurations/ConfigurationsExtendedSearch.vue'

@Component({
  components: {
    ConfigurationsDownloader,
    ConfigurationsExtendedSearch,
    ConfigurationsBasicSearch
  }
})
export default class ConfigurationsSearch extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  readonly value!: Configuration[]

  @Prop({
    required: false,
    type: Boolean
  })
  private loadInitialData!:boolean;

  private lastActiveSearcher: ConfigurationSearcher | null = null
  private loader: null | IPaginationLoader<Configuration> = null
  private loading:boolean=true
  private pageSize: number = 20

  created () {
    if (this.loadInitialData) {
      this.basicSearch('')
    }

    window.onscroll = () => { // TODO falls infinite scroll wirklich genutzt werden soll (wovon ich bei wissenschaftlichen Anwendungen abrate), dann sollte man doch gleich den von vuetify nutzen)
      const isOnBottom = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight

      if (isOnBottom && this.canLoadNext()) {
        this.loadNext()
      }
    }
  }

  get searchResults () {
    return this.value
  }

  set searchResults (value: Configuration[]) {
    this.$emit('input', value)
  }

  get numbersFoundMessage () {
    let message = ''
    if (this.searchResults.length === 1) {
      message = '1 configuration found'
    }
    if (this.searchResults.length > 1) {
      message = `${this.searchResults.length} configurations found`
    }
    return message
  }

  basicSearch (searchText: string) {
    this.runSearch(searchText, [], [], [])
  }

  extendedSearch ({
    searchText,
    selectedConfigurationStates,
    selectedLocationTypes,
    selectedProjects
  }: IConfigurationSearchOption) {
    this.runSearch(
      searchText,
      selectedConfigurationStates,
      selectedLocationTypes,
      selectedProjects
    )
  }

  runSearch (
    searchText: string | null,
    configurationStates: string[],
    locationTypes: string[],
    projects: Project[]
  ) {
    this.loading = true
    this.searchResults = []
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

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader) // TODO die Rekursion versteh ich hier nicht so ganz bzw. allgmein das komplexe laden der Daten --> da brauch ich mal ne Erläuterung
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional configurations failed')
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional configurations failed')
      })
    }
  }
}
</script>

<style scoped>

</style>
