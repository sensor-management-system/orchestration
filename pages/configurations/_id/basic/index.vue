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
  <v-card flat>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionDelete
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>

    <ConfigurationsBasicData
      v-model="configuration"
      :readonly="true"
    />

    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionDelete
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
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { Configuration } from '@/models/Configuration'
import ConfigurationsBasicDataForm from '@/components/configurations/ConfigurationsBasicDataForm.vue'
import ConfigurationsBasicData from '@/components/configurations/ConfigurationsBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
@Component({
  components: { ConfigurationsDeleteDialog, DotMenuActionDelete, DotMenu, ConfigurationsBasicData, ConfigurationsBasicDataForm }
})
export default class ConfigurationShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  private showDeleteDialog:boolean=false;

  head () {
    return {
      titleTemplate: 'Basic Data - %s'
    }
  }

  get configuration (): Configuration {
    return this.value
  }

  set configuration (value: Configuration) {
    this.$emit('input', value)
  }

  get configurationId () {
    return this.$route.params.id
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.configuration === null) {
      return
    }

    this.$api.configurations.deleteById(this.configuration.id).then(() => {
      this.$router.push('/configurations')
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    })
  }
}
</script>

<style scoped>

</style>
