<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    <div v-if="currentlyActiveLocationActionIsStatic">
      <v-card>
        <!-- 1) Ready-only static location view -->
        <v-card-title>
          Begin of the static location
          <v-spacer />
          <ConfigurationLocationsMenu
            v-if="$auth.loggedIn"
            :show-edit="hasNoStopActiveLocation"
            @edit-click="openEditStaticLocationForm"
            @delete-click="openDeleteStaticLocationDialog"
          />
        </v-card-title>
        <v-card-text class="text--primary">
          <ConfigurationStaticLocationBeginActionData
            :value="currentlyActiveLocationAction"
            :epsg-codes="epsgCodes"
            :elevation-data="elevationData"
          />
        </v-card-text>
        <v-card-actions v-if="$auth.loggedIn">
          <v-spacer />
          <v-btn v-if="hasNoStopActiveLocation" color="primary" small @click="openStopStaticLocationForm">
            Stop static location
          </v-btn>
          <v-btn v-else color="primary" small @click="openEditStaticLocationForm">
            Edit
          </v-btn>
        </v-card-actions>
        <template v-if="stopActionForActiveLocation">
          <v-divider class="mx-4 mt-4" />
          <v-card-title>
            End of the static location
            <v-spacer />
            <ConfigurationLocationsMenu
              v-if="$auth.loggedIn"
              :show-edit="false"
              @delete-click="openDeleteStaticLocationEndDialog"
            />
          </v-card-title>
          <v-card-text class="text--primary">
            <ConfigurationStaticLocationEndActionData
              v-model="stopActionForActiveLocation"
            />
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-spacer />
            <v-btn color="primary" small @click="openEditStaticLocationEndForm">
              Edit
            </v-btn>
          </v-card-actions>
        </template>
      </v-card>
      <v-dialog v-model="viewDeleteStaticLocationDialog" max-width="350">
        <v-card>
          <v-card-title class="headline">
            Delete static location
          </v-card-title>
          <v-card-text>
            Do you really want to delete the static location?
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-btn
              text
              small
              @click="closeDeleteStaticLocationDialog"
            >
              Cancel
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              small
              @click="deleteStaticLocationAction"
            >
              <v-icon left>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="viewDeleteStaticLocationEndDialog" max-width="350">
        <v-card>
          <v-card-title class="headline">
            Delete static location end
          </v-card-title>
          <v-card-text>
            Do you really want to delete the end of the static location?
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-btn
              text
              small
              @click="closeDeleteStaticLocationEndDialog"
            >
              Cancel
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              small
              @click="deleteStaticLocationEndAction"
            >
              <v-icon left>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div v-else-if="currentlyActiveLocationActionIsDynamic">
      <v-card>
        <!-- Read-only dynamic location view -->
        <v-card-title>
          Begin of the dynamic location
          <v-spacer />
          <ConfigurationLocationsMenu
            v-if="$auth.loggedIn"
            :show-edit="hasNoStopActiveLocation"
            @edit-click="openEditDynamicLocationForm"
            @delete-click="openDeleteDynamicLocationDialog"
          />
        </v-card-title>
        <v-card-text class="text--primary">
          <ConfigurationDynamicLocationBeginActionData
            :value="currentlyActiveLocationAction"
            :epsg-codes="epsgCodes"
            :elevation-data="elevationData"
            :devices="devices"
          />
        </v-card-text>
        <v-card-actions v-if="$auth.loggedIn">
          <v-spacer />
          <v-btn v-if="hasNoStopActiveLocation" color="primary" small @click="openStopDynamicLocationForm">
            Stop dynamic location
          </v-btn>
          <v-btn v-else color="primary" small @click="openEditDynamicLocationForm">
            Edit
          </v-btn>
        </v-card-actions>
        <v-divider class="mx-4 mt-4" />
        <template v-if="stopActionForActiveLocation">
          <v-card-title>
            End of the dynamic location
            <v-spacer />
            <ConfigurationLocationsMenu
              v-if="$auth.loggedIn"
              :show-edit="false"
              @delete-click="openDeleteDynamicLocationEndDialog"
            />
          </v-card-title>
          <v-card-text class="text--primary">
            <ConfigurationDynamicLocationEndActionData
              v-model="stopActionForActiveLocation"
            />
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-spacer />
            <v-btn color="primary" small @click="openEditDynamicLocationEndForm">
              Edit
            </v-btn>
          </v-card-actions>
        </template>
      </v-card>
      <v-dialog v-model="viewDeleteDynamicLocationDialog" max-width="350">
        <v-card>
          <v-card-title class="headline">
            Delete dynamic location
          </v-card-title>
          <v-card-text>
            Do you really want to delete the dynamic location?
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-btn
              text
              small
              @click="closeDeleteDynamicLocationDialog"
            >
              Cancel
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              small
              @click="deleteDynamicLocationAction"
            >
              <v-icon left>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="viewDeleteDynamicLocationEndDialog" max-width="350">
        <v-card>
          <v-card-title class="headline">
            Delete dynamic location end
          </v-card-title>
          <v-card-text>
            Do you really want to delete the end of the dynamic location?
          </v-card-text>
          <v-card-actions v-if="$auth.loggedIn">
            <v-btn
              text
              small
              @click="closeDeleteDynamicLocationEndDialog"
            >
              Cancel
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              small
              @click="deleteDynamicLocationEndAction"
            >
              <v-icon left>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'
import * as VueRouter from 'vue-router'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Configuration } from '@/models/Configuration'
import { Device } from '@/models/Device'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

import {
  getCurrentlyActiveLocationAction,
  getEndActionForActiveLocation
} from '@/utils/locationHelper'

import ConfigurationDynamicLocationBeginActionData from '@/components/configurations/ConfigurationDynamicLocationBeginActionData.vue'
import ConfigurationDynamicLocationEndActionData from '@/components/configurations/ConfigurationDynamicLocationEndActionData.vue'
import ConfigurationStaticLocationBeginActionData from '@/components/configurations/ConfigurationStaticLocationBeginActionData.vue'
import ConfigurationStaticLocationEndActionData from '@/components/configurations/ConfigurationStaticLocationEndActionData.vue'
import ConfigurationLocationsMenu from '@/components/configurations/ConfigurationLocationsMenu.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ConfigurationDynamicLocationBeginActionData,
    ConfigurationDynamicLocationEndActionData,
    ConfigurationStaticLocationBeginActionData,
    ConfigurationStaticLocationEndActionData,
    ConfigurationLocationsMenu,
    ProgressIndicator
  }
})
export default class ConfigurationLocationsAtTimestamp extends mixins(Rules) {
  private viewDeleteStaticLocationDialog: boolean = false
  private viewDeleteStaticLocationEndDialog: boolean = false
  private viewDeleteDynamicLocationDialog: boolean = false
  private viewDeleteDynamicLocationEndDialog: boolean = false
  private isSaving: boolean = false

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly elevationData!: ElevationDatum[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly epsgCodes!: EpsgCode[]

  get selectedDate (): DateTime {
    return this.dateFromUrlParam(this.$route) || DateTime.utc()
  }

  get currentlyActiveLocationAction () : StaticLocationBeginAction | DynamicLocationBeginAction | null {
    return getCurrentlyActiveLocationAction(this.value, this.selectedDate)
  }

  get stopActionForActiveLocation (): StaticLocationEndAction | DynamicLocationEndAction | null {
    return getEndActionForActiveLocation(this.value, this.currentlyActiveLocationAction)
  }

  get hasNoStopActiveLocation (): boolean {
    return this.stopActionForActiveLocation === null
  }

  get currentlyActiveLocationActionIsStatic (): boolean {
    return this.currentlyActiveLocationAction instanceof StaticLocationBeginAction
  }

  get currentlyActiveLocationActionIsDynamic (): boolean {
    return this.currentlyActiveLocationAction instanceof DynamicLocationBeginAction
  }

  openEditStaticLocationForm (): void {
    if (this.currentlyActiveLocationAction instanceof StaticLocationBeginAction) {
      this.$router.push('/configurations/' + this.value.id + '/locations/static-location-begin-actions/' + this.currentlyActiveLocationAction.id + '/edit')
    }
  }

  openEditDynamicLocationForm (): void {
    if (this.currentlyActiveLocationAction instanceof DynamicLocationBeginAction) {
      this.$router.push('/configurations/' + this.value.id + '/locations/dynamic-location-begin-actions/' + this.currentlyActiveLocationAction.id + '/edit')
    }
  }

  openStopStaticLocationForm (): void {
    this.$router.push('/configurations/' + this.value.id + '/locations/static-location-end-actions/new?date=' + this.selectedDate.toISO())
  }

  openEditStaticLocationEndForm (): void {
    if (this.stopActionForActiveLocation instanceof StaticLocationEndAction) {
      this.$router.push('/configurations/' + this.value.id + '/locations/static-location-end-actions/' + this.stopActionForActiveLocation.id + '/edit')
    }
  }

  openStopDynamicLocationForm (): void {
    this.$router.push('/configurations/' + this.value.id + '/locations/dynamic-location-end-actions/new?date=' + this.selectedDate.toISO())
  }

  openEditDynamicLocationEndForm (): void {
    if (this.stopActionForActiveLocation instanceof DynamicLocationEndAction) {
      this.$router.push('/configurations/' + this.value.id + '/locations/dynamic-location-end-actions/' + this.stopActionForActiveLocation.id + '/edit')
    }
  }

  openDeleteStaticLocationDialog () {
    this.viewDeleteStaticLocationDialog = true
  }

  closeDeleteStaticLocationDialog () {
    this.viewDeleteStaticLocationDialog = false
  }

  openDeleteStaticLocationEndDialog () {
    this.viewDeleteStaticLocationEndDialog = true
  }

  closeDeleteStaticLocationEndDialog () {
    this.viewDeleteStaticLocationEndDialog = false
  }

  openDeleteDynamicLocationDialog () {
    this.viewDeleteDynamicLocationDialog = true
  }

  closeDeleteDynamicLocationDialog () {
    this.viewDeleteDynamicLocationDialog = false
  }

  openDeleteDynamicLocationEndDialog () {
    this.viewDeleteDynamicLocationEndDialog = true
  }

  closeDeleteDynamicLocationEndDialog () {
    this.viewDeleteDynamicLocationEndDialog = false
  }

  async deleteStaticLocationAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    this.isSaving = true
    this.closeDeleteStaticLocationDialog()

    const beginAction = this.currentlyActiveLocationAction
    const endAction = this.stopActionForActiveLocation
    try {
      const configuration = Configuration.createFromObject(this.value)
      configuration.staticLocationBeginActions = configuration.staticLocationBeginActions.filter(x => x.id !== beginAction?.id)
      // And in case we have also an existing end action we want to remove it as well
      // (because the end action without a begin doesn't make that much sense)
      configuration.staticLocationEndActions = configuration.staticLocationEndActions.filter(x => x.id !== endAction?.id)

      this.$store.commit('configurations/setConfiguration', configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Delete successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Delete failed')
    } finally {
      this.isSaving = false
    }
  }

  async deleteStaticLocationEndAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    this.isSaving = true
    this.closeDeleteStaticLocationEndDialog()

    const endAction = this.stopActionForActiveLocation
    try {
      const configuration = Configuration.createFromObject(this.value)
      configuration.staticLocationEndActions = configuration.staticLocationEndActions.filter(x => x.id !== endAction?.id)

      this.$store.commit('configurations/setConfiguration', configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Delete successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Delete failed')
    } finally {
      this.isSaving = false
    }
  }

  async deleteDynamicLocationAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    this.isSaving = true
    this.closeDeleteDynamicLocationDialog()

    const beginAction = this.currentlyActiveLocationAction
    const endAction = this.stopActionForActiveLocation
    try {
      const configuration = Configuration.createFromObject(this.value)
      configuration.dynamicLocationBeginActions = configuration.dynamicLocationBeginActions.filter(x => x.id !== beginAction?.id)
      // And in case we have also an existing end action we want to remove it as well
      // (because the end action without a begin doesn't make that much sense)
      configuration.dynamicLocationEndActions = configuration.dynamicLocationEndActions.filter(x => x.id !== endAction?.id)

      this.$store.commit('configurations/setConfiguration', configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Delete successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Delete failed')
    } finally {
      this.isSaving = false
    }
  }

  async deleteDynamicLocationEndAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    this.isSaving = true
    this.closeDeleteDynamicLocationEndDialog()

    const endAction = this.stopActionForActiveLocation
    try {
      const configuration = Configuration.createFromObject(this.value)
      configuration.dynamicLocationEndActions = configuration.dynamicLocationEndActions.filter(x => x.id !== endAction?.id)

      this.$store.commit('configurations/setConfiguration', configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Delete successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Delete failed')
    } finally {
      this.isSaving = false
    }
  }

  /**
   * returns all devices that are used in the configuration
   *
   * @return {Device[]} a list of devices
   */
  get devices (): Device[] {
    return this.value.deviceMountActions.map(a => a.device)
  }

  dateFromUrlParam (route: VueRouter.Route): DateTime | undefined {
    if (!route.params.timestamp) {
      return
    }
    return DateTime.fromISO(route.params.timestamp).toUTC()
  }
}
</script>
