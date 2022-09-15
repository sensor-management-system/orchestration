<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <DotMenu>
          <template #actions>
            <DotMenuActionSensorML
              @click="openSensorML"
            />
            <DotMenuActionDelete
              v-if="$auth.loggedIn"
              :readonly="!deletable"
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>

      <ConfigurationsBasicData
        v-if="configuration"
        v-model="configuration"
        :readonly="true"
      />

      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <DotMenu>
          <template #actions>
            <DotMenuActionSensorML
              @click="openSensorML"
            />
            <DotMenuActionDelete
              v-if="$auth.loggedIn"
              :readonly="!deletable"
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
      <ConfigurationsDeleteDialog
        v-model="showDeleteDialog"
        :configuration-to-delete="configuration"
        @cancel-deletion="closeDialog"
        @submit-deletion="deleteAndCloseDialog"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import ConfigurationsBasicData from '@/components/configurations/ConfigurationsBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { IConfiguration } from '@/models/Configuration'

import { ExportAsSensorMLAction } from '@/store/configurations'

@Component({
  components: { ProgressIndicator, ConfigurationsDeleteDialog, DotMenuActionDelete, DotMenuActionSensorML, DotMenu, ConfigurationsBasicData },
  computed: mapState('configurations', ['configuration']),
  methods: mapActions('configurations', ['deleteConfiguration', 'exportAsSensorML'])
})
export default class ConfigurationShowBasicPage extends Vue {
  @InjectReactive()
    editable!: boolean

  @InjectReactive()
    deletable!: boolean

  private isSaving = false

  private showDeleteDialog: boolean = false

  // vuex definition for typescript check
  configuration!: IConfiguration
  deleteConfiguration!: (id: string) => void
  exportAsSensorML!: ExportAsSensorMLAction

  get configurationId () {
    return this.$route.params.configurationId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async openSensorML () {
    try {
      const blob = await this.exportAsSensorML(this.configurationId)
      const url = window.URL.createObjectURL(blob)
      window.open(url)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Configuration could not be exported as SensorML')
    }
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.configuration === null) {
      return
    }
    try {
      this.isSaving = true
      await this.deleteConfiguration(this.configuration.id)
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
      this.$router.push('/configurations')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
