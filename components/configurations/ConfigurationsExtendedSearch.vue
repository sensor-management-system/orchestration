<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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

  private selectedProjects: Project[] = []

  mounted () {
    this.$api.configurationStates.findAll().then((foundStates) => {
      this.configurationStates = foundStates
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading configuration states failed')
    })
  }

  emitSearch () {
    this.$emit('search', {
      searchText: this.searchText,
      selectedConfigurationStates: this.selectedConfigurationStates,
      selectedProjects: this.selectedProjects
    })
  }

  clearSearch () {
    this.searchText = null
    this.selectedConfigurationStates = []
    this.selectedProjects = []
  }
}
</script>

<style scoped>

</style>
