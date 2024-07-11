<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :disabled="isLoading"
        :to="'/platforms/' + platformId + '/parameters/new'"
      >
        Add Parameter
      </v-btn>
    </v-card-actions>
    <hint-card v-if="platformParametersSortedAlphabetically.length === 0">
      There are no parameters for this platform.
    </hint-card>
    <BaseList
      :list-items="platformParametersSortedAlphabetically"
    >
      <template #list-item="{item,index}">
        <parameter-list-item
          :value="item"
          :index="index"
          :parameter-change-actions="platformParameterChangeActions"
        >
          <template
            v-if="editable"
            #actions
          >
            <v-btn
              color="primary"
              text
              small
              @click.stop.prevent="openPageToAddValue(item)"
            >
              Add value
            </v-btn>
          </template>
          <template
            v-if="editable"
            #dot-menu-items
          >
            <DotMenuActionEdit
              :readonly="!editable"
              @click="openEditForm(item)"
            />
            <DotMenuActionCopy
              :readonly="!editable"
              :path="'/platforms/' + platformId + '/parameters/' + item.id + '/copy'"
            />
            <v-tooltip bottom>
              <template #activator="{ on }">
                <div v-on="$auth.loggedIn && parameterHasChangeActions(item.id)? on:null">
                  <DotMenuActionDelete
                    :readonly="!$auth.loggedIn || parameterHasChangeActions(item.id)"
                    @click="initDeleteDialog(item)"
                  />
                </div>
              </template>
              The paramter can't be deleted because it has assigend values.
            </v-tooltip>
          </template>
          <template #action-header>
            <th>Actions</th>
          </template>
          <template
            v-if="editable"
            #parameter-actions="{parameterAction}"
          >
            <td>
              <v-btn
                icon
                :to="'/platforms/' + platformId + '/actions/parameter-change-actions/' + parameterAction.id + '/edit'"
              >
                <v-icon
                  small
                  color="primary"
                >
                  mdi-pencil
                </v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon
                  small
                  color="red"
                  @click="initDeleteDialogParameterChangeAction(parameterAction)"
                >
                  mdi-delete
                </v-icon>
              </v-btn>
            </td>
          </template>
        </parameter-list-item>
      </template>
    </BaseList>

    <ParameterValueTable
      :value="platformParameterChangeActions"
    />

    <v-card-actions
      v-if="platformParametersSortedAlphabetically.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/platforms/' + platformId + '/parameters/new'"
      >
        Add Parameter
      </v-btn>
    </v-card-actions>

    <DeleteDialog
      v-if="editable && parameterToDelete"
      v-model="showDeleteDialog"
      title="Delete Parameter"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the parameter <em>{{ parameterToDelete.label }}</em>?
    </DeleteDialog>
    <DeleteDialog
      v-if="parameterChangeActionToDelete"
      v-model="showDeleteDialogForParameterChangeActionToDelete"
      title="Delete parameter value"
      :disabled="isLoading"
      @cancel="closeDeleteDialogForParameterChangeActionToDelete"
      @delete="deleteParameterChangeAction"
    >
      Do you really want to delete the parameter value?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import {
  DeletePlatformParameterAction,
  PlatformsState,
  LoadPlatformParametersAction,
  SetPlatformPresetParameterAction,
  SetChosenKindOfPlatformActionAction,
  DeletePlatformParameterChangeActionAction, LoadPlatformParameterChangeActionsAction
} from '@/store/platforms'
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
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { platformParameterChangeActionOption } from '@/models/ActionKind'
import DotMenuActionEdit from '@/components/DotMenuActionEdit.vue'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'

@Component({
  components: {
    DotMenuActionEdit,
    BaseList,
    DeleteDialog,
    DotMenuActionCopy,
    DotMenuActionDelete,
    ExpandableText,
    HintCard,
    ParameterListItem,
    ParameterValueTable
  },
  computed: {
    ...mapState('vocabulary', ['units']),
    ...mapState('platforms', ['platformParameterChangeActions']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('platforms', ['platformParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('platforms', ['deletePlatformParameter', 'loadPlatformParameters', 'setPlatformPresetParameter', 'setChosenKindOfPlatformAction', 'loadPlatformParameterChangeActions', 'deletePlatformParameterChangeAction']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class PlatformParameterShowPage extends Vue {
  @InjectReactive()
  private editable!: boolean

  private showDeleteDialog = false
  private showDeleteDialogForParameterChangeActionToDelete = false

  private parameterToDelete: Parameter | null = null
  private parameterChangeActionToDelete: ParameterChangeAction | null = null

  // vuex definition for typescript check
  units!: VocabularyState['units']
  platformParametersSortedAlphabetically!: PlatformsState['platformParameters']
  platformParameterChangeActions!: PlatformsState['platformParameterChangeActions']
  loadPlatformParameters!: LoadPlatformParametersAction
  deletePlatformParameter!: DeletePlatformParameterAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setPlatformPresetParameter!: SetPlatformPresetParameterAction
  setChosenKindOfPlatformAction!: SetChosenKindOfPlatformActionAction
  loadPlatformParameterChangeActions!: LoadPlatformParameterChangeActionsAction
  deletePlatformParameterChangeAction!: DeletePlatformParameterChangeActionAction

  get platformId (): string {
    return this.$route.params.platformId
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
      this.setLoading(true)

      await this.deletePlatformParameter(this.parameterToDelete.id)
      this.loadPlatformParameters(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Parameter has been deleted')
    } catch (error) {
      if (error instanceof HTTP409ConflictError) {
        this.$store.commit('snackbar/setError', 'Failed to delete parameter as other resources depend on it')
      } else {
        this.$store.commit('snackbar/setError', 'Failed to delete parameter')
      }
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  parameterHasChangeActions (parameterId: string): boolean {
    return this.platformParameterChangeActions.filter(action => action.parameter?.id === parameterId).length > 0
  }

  openPageToAddValue (parameter: Parameter) {
    this.setPlatformPresetParameter(parameter)
    this.setChosenKindOfPlatformAction(platformParameterChangeActionOption)
    this.$router.push('/platforms/' + this.platformId + '/actions/new/parameter-change-actions')
  }

  openEditForm (parameter: Parameter) {
    this.$router.push('/platforms/' + this.platformId + '/parameters/' + parameter.id + '/edit')
  }

  initDeleteDialogParameterChangeAction (action: ParameterChangeAction) {
    this.showDeleteDialogForParameterChangeActionToDelete = true
    this.parameterChangeActionToDelete = action
  }

  async deleteParameterChangeAction () {
    if (this.parameterChangeActionToDelete === null || this.parameterChangeActionToDelete.id === null) {
      return
    }

    try {
      this.setLoading(true)
      await this.deletePlatformParameterChangeAction(this.parameterChangeActionToDelete.id)
      this.loadPlatformParameterChangeActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Parameter value deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Parameter value could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDeleteDialogForParameterChangeActionToDelete()
    }
  }

  closeDeleteDialogForParameterChangeActionToDelete () {
    this.showDeleteDialogForParameterChangeActionToDelete = false
    this.parameterChangeActionToDelete = null
  }
}
</script>
