<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-container>
    <v-row
      dense
    >
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchText"
          label="Search term"
          placeholder="Search configurations"
          hint="Please enter at least 3 characters"
          @keydown.enter="search"
        />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <StringSelect
          v-model="selectedConfigurationStates"
          label="Select a status"
          :items="configurationStates"
          color="green"
          small
        />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <StringSelect
          v-model="selectedProjects"
          label="Select a project"
          :items="projects"
          color="red"
          small
        />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <StringSelect
          v-model="selectedCampaigns"
          label="Select a campaign"
          :items="campaigns"
          color="brown"
          small
        />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <site-search-select v-model="selectedSites" label="Select a site" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col cols="12" md="12">
        <permission-group-search-select v-model="selectedPermissionGroups" label="Select a permission group" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col v-if="$auth.loggedIn" cols="12" md="3">
        <v-checkbox v-model="onlyOwnConfigurations" label="Only own configurations" />
      </v-col>
      <v-col cols="12" md="3">
        <v-checkbox v-model="includeArchivedConfigurations" label="Include archived configurations" />
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="5"
        align-self="center"
      >
        <v-btn
          color="primary"
          small
          @click="search"
        >
          Search
        </v-btn>
        <v-btn
          text
          small
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import StringSelect from '@/components/StringSelect.vue'
import SiteSearchSelect from '@/components/SitesSearchSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Site } from '@/models/Site'
import {
  ConfigurationsState,
  LoadCampaignsAction,
  LoadProjectsAction,
  SearchConfigurationsPaginatedAction
} from '@/store/configurations'
import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { SetLoadingAction } from '@/store/progressindicator'
import { LoadPermissionGroupsAction } from '@/store/permissions'

@Component({
  components: { PermissionGroupSearchSelect, SiteSearchSelect, StringSelect },
  computed: {
    ...mapState('configurations', ['configurationStates', 'projects', 'campaigns'])
  },
  methods: {
    ...mapActions('configurations', [
      'searchConfigurationsPaginated',
      'loadConfigurationsStates',
      'loadProjects',
      'loadCampaigns'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationExtendedSearch extends Vue {
  private searchText: string | null = null
  private selectedConfigurationStates: string[] = []
  private selectedPermissionGroups: PermissionGroup[] = []
  private selectedProjects: string[] = []
  private selectedCampaigns: string[] = []
  private selectedSites: Site[] = []
  private onlyOwnConfigurations: boolean = false
  private includeArchivedConfigurations: boolean = false

  // vuex definition for typescript check
  configurationStates!: ConfigurationsState['configurationStates']
  projects!: ConfigurationsState['projects']
  campaigns!: ConfigurationsState['campaigns']
  setLoading!: SetLoadingAction
  searchConfigurationsPaginated!: SearchConfigurationsPaginatedAction
  loadConfigurationsStates!: () => void
  loadProjects!: LoadProjectsAction
  loadCampaigns!: LoadCampaignsAction
  loadPermissionGroups!: LoadPermissionGroupsAction

  async created () {
    this.setLoading(true)
    try {
      // Only load the data if not present
      if (this.configurationStates.length === 0) {
        await this.loadConfigurationsStates()
      }
      if (this.projects.length === 0) {
        await this.loadProjects()
      }

      if (this.campaigns.length === 0) {
        await this.loadCampaigns()
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of configuration extended search filter options failed')
    } finally {
      this.setLoading(false)
    }
  }

  get searchParams (): IConfigurationSearchParams {
    return {
      searchText: this.searchText,
      states: this.selectedConfigurationStates,
      permissionGroups: this.selectedPermissionGroups,
      onlyOwnConfigurations: this.onlyOwnConfigurations && this.$auth.loggedIn,
      projects: this.selectedProjects,
      campaigns: this.selectedCampaigns,
      sites: this.selectedSites,
      includeArchivedConfigurations: this.includeArchivedConfigurations
    }
  }

  public async search () {
    try {
      this.setLoading(true)
      await this.searchConfigurationsPaginated(this.searchParams)
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.setLoading(false)
    }
  }

  clearSearch () {
    this.selectedConfigurationStates = []
    this.selectedProjects = []
    this.selectedCampaigns = []
    this.selectedSites = []
    this.selectedPermissionGroups = []
    this.onlyOwnConfigurations = false
    this.includeArchivedConfigurations = false
    this.searchText = null
  }
}
</script>

<style scoped>

</style>
