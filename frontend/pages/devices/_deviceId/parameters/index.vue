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
        :to="'/devices/' + deviceId + '/parameters/new'"
      >
        Add Parameter
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceParametersSortedAlphabetically.length === 0">
      There are no parameters for this device.
    </hint-card>
    <BaseList
      :list-items="deviceParametersSortedAlphabetically"
    >
      <template #list-item="{item,index}">
        <parameter-list-item
          :value="item"
          :index="index"
          :parameter-change-actions="deviceParameterChangeActions"
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
              :path="'/devices/' + deviceId + '/parameters/' + item.id + '/copy'"
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
                :to="'/devices/' + deviceId + '/actions/parameter-change-actions/' + parameterAction.id + '/edit'"
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
      :value="deviceParameterChangeActions"
    />

    <v-card-actions
      v-if="deviceParametersSortedAlphabetically.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/parameters/new'"
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
  DeleteDeviceParameterAction, DeleteDeviceParameterChangeActionAction,
  DevicesState, LoadDeviceParameterChangeActionsAction,
  LoadDeviceParametersAction, SetChosenKindOfDeviceActionAction, SetDevicePresetParameterAction
} from '@/store/devices'
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
import { deviceParameterChangeActionOption } from '@/models/ActionKind'
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
    ...mapState('devices', ['deviceParameterChangeActions']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('devices', ['deviceParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('devices', ['deleteDeviceParameter', 'loadDeviceParameters', 'setChosenKindOfDeviceAction', 'setDevicePresetParameter', 'deleteDeviceParameterChangeAction', 'loadDeviceParameterChangeActions']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class DeviceParameterShowPage extends Vue {
  @InjectReactive()
  private editable!: boolean

  private showDeleteDialog = false
  private showDeleteDialogForParameterChangeActionToDelete = false

  private parameterToDelete: Parameter | null = null
  private parameterChangeActionToDelete: ParameterChangeAction | null = null

  // vuex definition for typescript check
  units!: VocabularyState['units']
  deviceParametersSortedAlphabetically!: DevicesState['deviceParameters']
  deviceParameterChangeActions!: DevicesState['deviceParameterChangeActions']
  loadDeviceParameters!: LoadDeviceParametersAction
  deleteDeviceParameter!: DeleteDeviceParameterAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setChosenKindOfDeviceAction!: SetChosenKindOfDeviceActionAction
  setDevicePresetParameter!: SetDevicePresetParameterAction
  deleteDeviceParameterChangeAction!: DeleteDeviceParameterChangeActionAction
  loadDeviceParameterChangeActions!: LoadDeviceParameterChangeActionsAction

  get deviceId (): string {
    return this.$route.params.deviceId
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

      await this.deleteDeviceParameter(this.parameterToDelete.id)
      this.loadDeviceParameters(this.deviceId)
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
    return this.deviceParameterChangeActions.filter(action => action.parameter?.id === parameterId).length > 0
  }

  openPageToAddValue (parameter: Parameter) {
    this.setDevicePresetParameter(parameter)
    this.setChosenKindOfDeviceAction(deviceParameterChangeActionOption)
    this.$router.push('/devices/' + this.deviceId + '/actions/new/parameter-change-actions')
  }

  openEditForm (parameter: Parameter) {
    this.$router.push('/devices/' + this.deviceId + '/parameters/' + parameter.id + '/edit')
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
      await this.deleteDeviceParameterChangeAction(this.parameterChangeActionToDelete.id)
      this.loadDeviceParameterChangeActions(this.deviceId)
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
