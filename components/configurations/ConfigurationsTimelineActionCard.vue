<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
        </v-card-subtitle>
      </template>
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            {{ action.title }}
          </v-card-title>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col>
          <v-card-subtitle class="text--primary pt-0">
            {{ contactName | orDefault }}
          </v-card-subtitle>
        </v-col>
      </v-row>
      <template v-if="action.genericAction" #dot-menu-items>
        <DotMenuActionDelete
          :readonly="!editable"
          @click="initDeleteDialogGenericAction(action.genericAction)"
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
      v-model="showDeleteDialog"
      title="Delete Action"
      @cancel="closeDialog"
      @delete="deleteGenericAction"
    >
      Do you really want to delete the action?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import {
  DeleteConfigurationGenericAction,
  LoadAllConfigurationActionsAction
} from '@/store/configurations'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'

import { ITimelineAction } from '@/utils/configurationInterfaces'
import { dateToDateTimeString } from '@/utils/dateHelper'
import { GenericAction } from '@/models/GenericAction'
import { Attachment } from '@/models/Attachment'

@Component({
  filters: {
    dateToDateTimeString
  },
  components: {
    BaseExpandableListItem,
    DotMenu,
    DotMenuActionDelete,
    DeleteDialog
  },
  methods: mapActions('configurations', ['deleteConfigurationGenericAction', 'loadAllConfigurationActions'])
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

  private isSaving: boolean = false
  private showDeleteDialog: boolean = false
  private genericActionToDelete: GenericAction | null = null

  // vuex definition for typescript check
  deleteConfigurationGenericAction!: DeleteConfigurationGenericAction
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get contactName () {
    if (this.action.contact) {
      return this.action.contact.toString()
    }
    return ''
  }

  initDeleteDialogGenericAction (action: GenericAction) {
    this.showDeleteDialog = true
    this.genericActionToDelete = action
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.genericActionToDelete = null
  }

  async deleteGenericAction () {
    if (this.genericActionToDelete === null || this.genericActionToDelete.id === null) {
      return
    }

    try {
      this.isSaving = true
      await this.deleteConfigurationGenericAction(this.genericActionToDelete.id)
      this.loadAllConfigurationActions(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Generic action deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Generic action could not be deleted')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }

  openAttachment (attachment: Attachment) {
    this.$emit('open-attachment', attachment)
  }
}
</script>

<style scoped>

</style>
