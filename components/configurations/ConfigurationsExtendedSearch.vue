<template>
  <v-tab-item :eager="true">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="searchText" label="Label" placeholder="Label of configuration" @keydown.enter="emitSearch" />
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
          @click="emitSearch"
        >
          Search
        </v-btn>
        <v-btn
          text
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
  </v-tab-item>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { LocationType } from '@/models/Location'
import { Project } from '@/models/Project'

import ProjectSelect from '@/components/ProjectSelect.vue'
import StringSelect from '@/components/StringSelect.vue'

@Component({
  components: {
    StringSelect,
    ProjectSelect
  }
})
export default class ConfigurationsExtendedSearch extends Vue {
  private searchText:string|null=null

  private selectedConfigurationStates: string[] = []
  private configurationStates: string[] = []

  private selectedLocationTypes: string[] = []
  private locationTypes: string[] = []

  private selectedProjects: Project[] = []

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
  }

  emitSearch () {
    this.$emit('search', {
      searchText: this.searchText,
      selectedConfigurationStates: this.selectedConfigurationStates,
      selectedLocationTypes: this.selectedLocationTypes,
      selectedProjects: this.selectedProjects
    })
  }

  clearSearch () {
    this.searchText = null
    this.selectedConfigurationStates = []
    this.selectedLocationTypes = []
    this.selectedProjects = []
  }
}
</script>

<style scoped>

</style>
