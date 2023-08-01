<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <ProgressIndicator
      v-model="isInProgress"
      dark
    />
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :disabled="isFetching"
        :to="'/configurations/' + configurationId + '/parameters/new'"
      >
        Add Parameter
      </v-btn>
    </v-card-actions>
    <hint-card v-if="configurationParameters.length === 0">
      There are no parameters for this configuration.
    </hint-card>
    <BaseList
      :list-items="configurationParameters"
    >
      <template #list-item="{item,index}">
        <parameter-list-item
          :value="item"
          :index="index"
          :parameter-change-actions="configurationParameterChangeActions"
        >
          <template
            v-if="editable"
            #actions
          >
            <v-btn
              :to="'/configurations/' + configurationId + '/parameters/' + item.id + '/edit'"
              color="primary"
              text
              small
              @click.stop.prevent
            >
              Edit
            </v-btn>
          </template>
          <template
            v-if="editable"
            #dot-menu-items
          >
            <DotMenuActionCopy
              :readonly="!editable"
              :path="'/configurations/' + configurationId + '/parameters/' + item.id + '/copy'"
            />
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn || parameterHasChangeActions(item.id)"
              @click="initDeleteDialog(item)"
            />
          </template>
        </parameter-list-item>
      </template>
    </BaseList>

    <ParameterValueTable
      :value="configurationParameterChangeActions"
    />

    <v-card-actions
      v-if="configurationParameters.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/parameters/new'"
      >
        Add Parameter
      </v-btn>
    </v-card-actions>

    <DeleteDialog
      v-if="editable && parameterToDelete"
      v-model="showDeleteDialog"
      title="Delete Parameter"
      :disabled="isInProgress"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the parameter <em>{{ parameterToDelete.label }}</em>?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive, Prop } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import {
  DeleteConfigurationParameterAction,
  ConfigurationsState,
  LoadConfigurationParametersAction
} from '@/store/configurations'
import { VocabularyState } from '@/store/vocabulary'

import { HTTP409ConflictError } from '@/services/HTTPErrors'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'
import HintCard from '@/components/HintCard.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import ParameterValueTable from '@/components/shared/ParameterValueTable.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    BaseList,
    DeleteDialog,
    DotMenuActionCopy,
    DotMenuActionDelete,
    ExpandableText,
    HintCard,
    ParameterListItem,
    ParameterValueTable,
    ProgressIndicator
  },
  computed: {
    ...mapState('vocabulary', ['units']),
    ...mapState('configurations', ['configurationParameters', 'configurationParameterChangeActions'])
  },
  methods: {
    ...mapActions('configurations', ['deleteConfigurationParameter', 'loadConfigurationParameters'])
  },
  scrollToTop: true
})
export default class ConfigurationPropertyShowPage extends Vue {
  @InjectReactive()
  private editable!: boolean

  @Prop({
    type: Boolean
  })
  private isFetching!: boolean

  private isInProgress = false

  private showDeleteDialog = false
  private parameterToDelete: Parameter | null = null

  // vuex definition for typescript check
  units!: VocabularyState['units']
  configurationParameters!: ConfigurationsState['configurationParameters']
  configurationParameterChangeActions!: ConfigurationsState['configurationParameterChangeActions']
  loadConfigurationParameters!: LoadConfigurationParametersAction
  deleteConfigurationParameter!: DeleteConfigurationParameterAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  initDeleteDialog (parameter: Parameter) {
    this.showDeleteDialog = true
    this.parameterToDelete = parameter
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.parameterToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.parameterToDelete === null || this.parameterToDelete.id === null) {
      return
    }
    try {
      this.isInProgress = true

      await this.deleteConfigurationParameter(this.parameterToDelete.id)
      this.loadConfigurationParameters(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Parameter has been deleted')
    } catch (error) {
      if (error instanceof HTTP409ConflictError) {
        this.$store.commit('snackbar/setError', 'Failed to delete parameter as other resources depend on it')
      } else {
        this.$store.commit('snackbar/setError', 'Failed to delete parameter')
      }
    } finally {
      this.isInProgress = false
      this.closeDialog()
    }
  }

  parameterHasChangeActions (parameterId: string): boolean {
    return this.configurationParameterChangeActions.filter(action => action.parameter?.id === parameterId).length > 0
  }
}
</script>
