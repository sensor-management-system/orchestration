<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <div v-if="action">
    <base-expandable-list-item v-if="action" :expandable-color="'grey lighten-5'">
      <template #header>
        <v-card-subtitle class="pb-0">
          <span>{{ action.date | dateToDateTimeString }}</span>
          <span v-if="action.endDate"> - {{ action.endDate | dateToDateTimeString }}</span>
          <span class="text-caption text--secondary">(UTC)</span>
          by {{ contactName | orDefault }}
        </v-card-subtitle>
      </template>
      <template #default="{show}">
        <v-row no-gutters>
          <v-col cols="12">
            <v-card-title class="text--primary pt-0 pb-0">
              {{ action.title }}
            </v-card-title>
          </v-col>
        </v-row>
        <v-row v-show="!show && action.description" no-gutters>
          <v-col>
            <v-card-subtitle class="text--primary pt-0 description-preview">
              {{ action.description }}
            </v-card-subtitle>
          </v-col>
        </v-row>
      </template>
      <template v-if="action.genericAction || action.parameterChangeAction || action.mountAction" #dot-menu-items>
        <DotMenuActionDelete
          v-if="action.genericAction"
          :readonly="!editable"
          @click="initDeleteDialogGenericAction(action.genericAction)"
        />
        <DotMenuActionDelete
          v-if="action.parameterChangeAction"
          :readonly="!editable"
          @click="initDeleteDialogParameterChangeAction(action.parameterChangeAction)"
        />
        <DotMenuActionEdit
          v-if="action.mountAction && action.mountAction.device"
          :readonly="!editable"
          @click="openEditDeviceMountActionForm(action)"
        />
        <DotMenuActionEdit
          v-if="action.mountAction && action.mountAction.platform"
          :readonly="!editable"
          @click="openEditPlatformMountActionForm(action)"
        />
      </template>
      <template #actions>
        <v-btn
          v-if="action.genericAction && editable"
          :to="'/configurations/' + configurationId + '/actions/generic-configuration-actions/' + action.genericAction.id + '/edit'"
          color="primary"
          text
          @click.stop.prevent
        >
          Edit
        </v-btn>
        <v-btn
          v-if="action.parameterChangeAction && editable"
          :to="'/configurations/' + configurationId + '/actions/parameter-change-actions/' + action.parameterChangeAction.id + '/edit'"
          color="primary"
          text
          @click.stop.prevent
        >
          Edit
        </v-btn>
        <v-btn
          v-if="action.mountAction && action.mountAction.platform"
          :to="'/platforms/' + action.mountAction.platform.id"
          color="primary"
          text
          @click.stop.prevent
        >
          View
        </v-btn>
        <v-btn
          v-if="action.mountAction && action.mountAction.device"
          :to="'/devices/' + action.mountAction.device.id"
          color="primary"
          text
          @click.stop.prevent
        >
          View
        </v-btn>
        <v-btn
          v-if="action.staticLocationInfo"
          :to="'/configurations/' + configurationId + '/locations/static-location-actions/' + action.staticLocationInfo.id"
          color="primary"
          text
          @click.stop.prevent
        >
          View
        </v-btn>
        <v-btn
          v-if="action.dynamicLocationInfo"
          :to="'/configurations/' + configurationId + '/locations/dynamic-location-actions/' + action.dynamicLocationInfo.id"
          color="primary"
          text
          @click.stop.prevent
        >
          View
        </v-btn>
      </template>
      <template #expandable>
        <div
          class="text--primary pt-0 px-3"
        >
          <div v-if="action.mountInfo">
            <v-row
              v-if="action.mountInfo.parentPlatform"
              dense
            >
              <v-col cols="12" md="4">
                <label>Mounted on</label>
                {{ action.mountInfo.parentPlatform.shortName }}
              </v-col>
            </v-row>
            <v-row
              v-if="action.mountInfo.parentDevice"
              dense
            >
              <v-col cols="12" md="4">
                <label>Mounted on</label>
                {{ action.mountInfo.parentDevice.shortName }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col cols="12" md="3">
                <label>Offset x</label>
                {{ action.mountInfo.offsetX }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Offset y</label>
                {{ action.mountInfo.offsetY }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Offset z</label>
                {{ action.mountInfo.offsetZ }}
              </v-col>
            </v-row>
          </div>
          <div v-else-if="action.staticLocationInfo">
            <v-row
              dense
            >
              <v-col cols="12" md="3">
                <label>x</label>
                {{ action.staticLocationInfo.x | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>y</label>
                {{ action.staticLocationInfo.y | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>EPSG Code</label>
                {{ action.staticLocationInfo.epsgCode | orDefault }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col cols="12" md="3" />
              <v-col cols="12" md="3">
                <label>z</label>
                {{ action.staticLocationInfo.z }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Elevation Datum</label>
                {{ action.staticLocationInfo.elevationDatumName | orDefault }}
              </v-col>
            </v-row>
          </div>
          <div v-else-if="action.dynamicLocationInfo">
            <v-row
              dense
            >
              <v-col cols="12" md="3">
                <label>Device that measures x</label>
                {{ action.dynamicLocationInfo.deviceX | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Device that measures y</label>
                {{ action.dynamicLocationInfo.deviceY | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Device that measures z</label>
                {{ action.dynamicLocationInfo.deviceZ | orDefault }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col cols="12" md="3">
                <label>Measured Quantity for x</label>
                {{ action.dynamicLocationInfo.x | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Measured Quantity for y</label>
                {{ action.dynamicLocationInfo.y | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Measured Quantity for z</label>
                {{ action.dynamicLocationInfo.z | orDefault }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col cols="12" md="3">
                <label>EPSG Code</label>
                {{ action.dynamicLocationInfo.epsgCode | orDefault }}
              </v-col>
              <v-col cols="12" md="3">
                <label>Elevation Datum</label>
                {{ action.dynamicLocationInfo.elevationDatumName | orDefault }}
              </v-col>
            </v-row>
          </div>
          <template
            v-if="action.parameterChangeAction"
          >
            <v-row
              dense
            >
              <v-col>
                <label>Value</label>
                {{ action.parameterChangeAction.value | orDefault }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col>
                <label>Unit</label>
                {{ action.parameterChangeAction.parameter.unitName | orDefault }}
              </v-col>
            </v-row>
          </template>
          <v-row dense>
            <v-col>
              <label>Description</label>
              {{ action.description | orDefault }}
            </v-col>
          </v-row>
          <v-row v-if="action.genericAction && action.genericAction.attachments.length > 0" dense>
            <v-col>
              <label>Attachments</label>
              <div v-for="(attachment, index) in action.genericAction.attachments" :key="index">
                <span class="text-caption">
                  <template v-if="isPublic || !attachment.isUpload">
                    <a :href="attachment.url" target="_blank">
                      {{ attachment.label }}&nbsp;<v-icon small>mdi-open-in-new</v-icon>
                    </a>
                  </template>
                  <template v-else>
                    <span>
                      {{ attachment.label }}&nbsp;<v-icon small @click="openAttachment(attachment)">mdi-link-lock</v-icon>
                    </span>
                  </template>
                </span>
              </div>
            </v-col>
          </v-row>
        </div>
      </template>
    </base-expandable-list-item>
    <DeleteDialog
      v-if="actionToDelete"
      v-model="showDeleteDialog"
      title="Delete Action"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the action?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import {
  DeleteConfigurationGenericAction,
  DeleteConfigurationParameterChangeActionAction,
  LoadAllConfigurationActionsAction, SetSelectedDateAction
} from '@/store/configurations'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { DeviceMountTimelineAction, ITimelineAction, PlatformMountTimelineAction } from '@/utils/configurationInterfaces'
import { dateToDateTimeString } from '@/utils/dateHelper'
import { GenericAction } from '@/models/GenericAction'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { Attachment } from '@/models/Attachment'
import DotMenuActionEdit from '@/components/DotMenuActionEdit.vue'

@Component({
  filters: {
    dateToDateTimeString
  },
  components: {
    DotMenuActionEdit,
    BaseExpandableListItem,
    DotMenu,
    DotMenuActionDelete,
    DeleteDialog
  },
  computed: mapState('progressindicator', ['isLoading']),
  methods: {
    ...mapActions('configurations', ['deleteConfigurationGenericAction', 'deleteConfigurationParameterChangeAction', 'loadAllConfigurationActions', 'setSelectedDate']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationsTimelineActionCard extends Vue {
  @InjectReactive()
    editable!: boolean

  @Prop({
    required: true,
    type: Object
  })
  readonly action!: ITimelineAction

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly isPublic!: boolean

  private showDeleteDialog: boolean = false
  private genericActionToDelete: GenericAction | null = null
  private parameterChangeActionToDelete: ParameterChangeAction | null = null

  // vuex definition for typescript check
  deleteConfigurationGenericAction!: DeleteConfigurationGenericAction
  deleteConfigurationParameterChangeAction!: DeleteConfigurationParameterChangeActionAction
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  private setSelectedDate!: SetSelectedDateAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get contactName () {
    if (this.action.contact) {
      return this.action.contact.toString()
    }
    return ''
  }

  get actionToDelete () {
    if (this.genericActionToDelete) {
      return this.genericActionToDelete
    }
    if (this.parameterChangeActionToDelete) {
      return this.parameterChangeActionToDelete
    }
    return null
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true
    this.genericActionToDelete = action
    this.parameterChangeActionToDelete = null
  }

  initDeleteDialogParameterChangeAction (action: ParameterChangeAction) {
    this.showDeleteDialog = true
    this.parameterChangeActionToDelete = action
    this.genericActionToDelete = null
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.genericActionToDelete = null
    this.parameterChangeActionToDelete = null
  }

  async deleteAndCloseDialog (): Promise<void> {
    try {
      switch (true) {
        case this.genericActionToDelete !== null:
          await this.deleteGenericAction()
          break
        case this.parameterChangeActionToDelete !== null:
          await this.deleteParameterChangeAction()
          break
      }
    } finally {
      this.loadAllConfigurationActions(this.configurationId)
      this.closeDialog()
    }
  }

  async deleteGenericAction () {
    if (this.genericActionToDelete === null || this.genericActionToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteConfigurationGenericAction(this.genericActionToDelete.id)
      this.$store.commit('snackbar/setSuccess', 'Generic action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Generic action could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  async deleteParameterChangeAction () {
    if (this.parameterChangeActionToDelete === null || this.parameterChangeActionToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteConfigurationParameterChangeAction(this.parameterChangeActionToDelete.id)
      this.$store.commit('snackbar/setSuccess', 'Parameter change action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Parameter change action could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  openAttachment (attachment: Attachment) {
    this.$emit('open-attachment', attachment)
  }

  openEditDeviceMountActionForm (action: DeviceMountTimelineAction) {
    this.setSelectedDate(action.mountAction.beginDate)
    this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices/device-mount-actions/' + action.mountAction.id + '/edit')
  }

  openEditPlatformMountActionForm (action: PlatformMountTimelineAction) {
    this.setSelectedDate(action.mountAction.beginDate)
    this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices/platform-mount-actions/' + action.mountAction.id + '/edit')
  }
}
</script>

<style scoped>
.description-preview{
  vertical-align: middle !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
</style>
