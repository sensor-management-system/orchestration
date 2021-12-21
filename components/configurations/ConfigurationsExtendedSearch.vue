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
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="searchTextModel" label="Label" placeholder="Label of configuration" @keydown.enter="emitSearch" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <StringSelect
          v-model="selectedConfigurationStatesModel"
          label="Select a status"
          :items="configurationStates"
          color="green"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <ProjectSelect
          v-model="selectedProjectsModel"
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
          @click="emitSearch"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Project } from '@/models/Project'

import { IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'

import ProjectSelect from '@/components/ProjectSelect.vue'
import StringSelect from '@/components/StringSelect.vue'

@Component({
  components: {
    StringSelect,
    ProjectSelect
  }
})
export default class ConfigurationsExtendedSearch extends Vue {
  @Prop({
    default: '',
    required: false,
    type: String
  })
  private readonly searchText!: string

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  private readonly selectedConfigurationStates!: string[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  private readonly selectedProjects!: Project[]

  private internalSearchText: string | null = null
  private internalSelectedConfigurationStates: string[] = []
  private internalSelectedProjects: Project[] = []

  private configurationStates: string[] = []

  mounted () {
    this.$api.configurationStates.findAll().then((foundStates) => {
      this.configurationStates = foundStates
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading configuration states failed')
    })
  }

  get searchTextModel (): string | null {
    return this.internalSearchText || this.searchText
  }

  set searchTextModel (value: string | null) {
    this.internalSearchText = value
  }

  get selectedConfigurationStatesModel (): string[] {
    return this.internalSelectedConfigurationStates.length ? this.internalSelectedConfigurationStates : this.selectedConfigurationStates
  }

  set selectedConfigurationStatesModel (value: string[]) {
    this.internalSelectedConfigurationStates = value
  }

  get selectedProjectsModel (): Project[] {
    return this.internalSelectedProjects.length ? this.internalSelectedProjects : this.selectedProjects
  }

  set selectedProjectsModel (value: Project[]) {
    this.internalSelectedProjects = value
  }

  emitSearch () {
    this.$emit('search', {
      searchText: this.searchTextModel,
      states: this.selectedConfigurationStatesModel,
      projects: this.selectedProjectsModel
    } as IConfigurationSearchParams)
  }

  clearSearch () {
    this.searchTextModel = null
    this.selectedConfigurationStatesModel = []
    this.selectedProjectsModel = []
  }
}
</script>

<style scoped>

</style>
