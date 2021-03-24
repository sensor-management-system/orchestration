<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditPropertiesPage"
        color="primary"
        small
        @click="addProperty"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <v-expansion-panels
      v-model="openedPanels"
      multiple
    >
      <v-expansion-panel
        v-for="(property, index) in deviceProperties"
        :key="'property-' + property.id"
      >
        <v-expansion-panel-header>
          <v-row no-gutters>
            <v-col class="text-subtitle-1" cols="10">
              Measured quantity {{ index+1 }} {{ property.label ? ' - ' + property.label : '' }}
            </v-col>
            <v-col
              align-self="end"
              class="text-right"
            >
              <v-btn
                v-if="isLoggedIn && (!isEditModeForSomeProperty())"
                color="primary"
                text
                small
                @click.prevent.stop="openInEditMode(property)"
              >
                Edit
              </v-btn>
              <template
                v-if="isLoggedIn && (isEditModeForProperty(property))"
              >
                <v-btn
                  text
                  small
                  @click.prevent.stop="cancelEditMode()"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="green"
                  small
                  @click.prevent.stop="saveProperty(property)"
                >
                  Apply
                </v-btn>
              </template>

              <v-menu
                v-if="isLoggedIn && (!isEditModeForSomeProperty())"
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template v-slot:activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    dense
                    @click="copyProperty(property)"
                  >
                    <v-list-item-title>
                      <v-icon
                        left
                        small
                      >
                        mdi-content-copy
                      </v-icon>
                      Copy
                    </v-list-item-title>
                  </v-list-item>
                  <v-list-item
                    dense
                    @click="showDeleteDialogFor(property.id)"
                  >
                    <v-list-item-content>
                      <v-list-item-title class="red--text">
                        <v-icon left small color="red">
                          mdi-delete
                        </v-icon>
                        Delete measured quantity...
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
          <v-dialog v-model="showDeleteDialog[property.id]" max-width="400">
            <v-card>
              <v-card-title class="headline">
                Delete Measured Quantity
              </v-card-title>
              <v-card-text>
                Do you really want to delete the measured quantity <em>{{ property.label }}</em>?
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="hideDeleteDialogFor(property.id)"
                >
                  No
                </v-btn>
                <v-spacer />
                <v-btn
                  color="error"
                  text
                  @click="deleteAndCloseDialog(property.id)"
                >
                  <v-icon left>
                    mdi-delete
                  </v-icon>
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <template v-if="isEditModeForProperty(property)">
            <NuxtChild
              :ref="'deviceProperty_' + property.id"
              v-model="deviceProperties[index]"
              :compartments="compartments"
              :sampling-medias="samplingMedias"
              :properties="properties"
              :units="units"
              :measured-quantity-units="measuredQuantityUnits"
              @showsave="showsave"
            />
          </template>
          <template v-else>
            <DevicePropertyInfo
              v-model="deviceProperties[index]"
              :compartments="compartments"
              :sampling-medias="samplingMedias"
              :properties="properties"
              :units="units"
              :measured-quantity-units="measuredQuantityUnits"
            />
          </template>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-card-actions
      v-if="deviceProperties.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditPropertiesPage"
        color="primary"
        small
        @click="addProperty"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import DevicePropertyInfo from '@/components/DevicePropertyInfo.vue'

import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator,
    DevicePropertyInfo
  }
})
export default class DevicePropertiesPage extends Vue {
  private openedPanels: number[] = [] as number[]
  private deviceProperties: DeviceProperty[] = []
  private isLoading = false
  private isSaving = false

  private showDeleteDialog: {[idx: string]: boolean} = {}

  private compartments: Compartment[] = []
  private samplingMedias: SamplingMedia[] = []
  private properties: Property[] = []
  private units: Unit[] = []
  private measuredQuantityUnits: MeasuredQuantityUnit[] = []

  async fetch () {
    try {
      this.isLoading = true
      this.deviceProperties = await this.$api.devices.findRelatedDeviceProperties(this.deviceId)
      this.openPanelIfStartedInEditMode()
      this.isLoading = false
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
      this.isLoading = false
    }
    try {
      this.compartments = await this.$api.compartments.findAllPaginated()
      this.samplingMedias = await this.$api.samplingMedia.findAllPaginated()
      this.properties = await this.$api.properties.findAllPaginated()
      this.units = await this.$api.units.findAllPaginated()
      this.measuredQuantityUnits = await this.$api.measuredQuantityUnits.findAllPaginated()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of system values failed')
    }
  }

  openPanelIfStartedInEditMode () {
    if (this.isEditPropertiesPage) {
      const propertyId = this.getPropertyIdFromUrl()
      if (propertyId) {
        const propertyIndex = this.deviceProperties.findIndex((p: DeviceProperty) => p.id === propertyId)
        if (propertyIndex > -1) {
          this.openedPanels.push(propertyIndex)
        }
      }
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditPropertiesPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/measuredquantities\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  getPropertyIdFromUrl (): string | undefined {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/measuredquantities\/([0-9]+)\/?.*$'
    const matches = this.$route.path.match(editUrl)
    if (!matches) {
      return
    }
    return matches[1]
  }

  addProperty (): void {
    const property = new DeviceProperty()
    this.copyProperty(property)
  }

  deleteAndCloseDialog (id: string) {
    this.isSaving = true
    this.showDeleteDialog = {}

    this.$api.deviceProperties.deleteById(id).then(() => {
      const searchIndex = this.deviceProperties.findIndex(p => p.id === id)
      if (searchIndex > -1) {
        this.deviceProperties.splice(searchIndex, 1)
      }
      this.isSaving = false
    }).catch((_error) => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to delete measured quantity')
    })
  }

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
  }

  showsave (isSaving: boolean) {
    this.isSaving = isSaving
  }

  copyProperty (oldProperty: DeviceProperty) {
    const property = DeviceProperty.createFromObject(oldProperty)
    property.id = null
    this.isSaving = true
    this.$api.deviceProperties.add(this.deviceId, property).then((newProperty: DeviceProperty) => {
      this.isSaving = false
      this.deviceProperties.push(newProperty)
      this.openedPanels = [...this.openedPanels, this.deviceProperties.length - 1]
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities/' + newProperty.id + '/edit')
      this.openPanelIfStartedInEditMode()
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    })
  }

  saveProperty (property: DeviceProperty) {
    const childComponents = this.$refs['deviceProperty_' + property.id]
    if (Array.isArray(childComponents)) {
      const firstChild: any = childComponents[0]
      if (firstChild.save) {
        firstChild.save()
      } else {
        throw new Error('Can\'t save with the given child reference: No method given.')
      }
    } else {
      throw new TypeError('Can\'t access the child component to run the save method')
    }
  }

  isEditModeForProperty (property: DeviceProperty): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/measuredquantities/' + property.id + '/edit'
  }

  isEditModeForSomeProperty (): boolean {
    return this.deviceProperties.some((p: DeviceProperty) => this.isEditModeForProperty(p))
  }

  openInEditMode (property: DeviceProperty) {
    const propertyIndex = this.deviceProperties.findIndex((p: DeviceProperty) => p.id === property.id)
    if (propertyIndex > -1) {
      const openPanelIndex = this.openedPanels.findIndex((v: number) => v === propertyIndex)
      const alreadyExpanded = openPanelIndex > -1
      if (!alreadyExpanded) {
        const newOpenPanels = []
        for (const idx of this.openedPanels) {
          newOpenPanels.push(idx)
        }
        newOpenPanels.push(propertyIndex)
        this.openedPanels = [...this.openedPanels, propertyIndex]
      }
    }
    this.$router.push('/devices/' + this.deviceId + '/measuredquantities/' + property.id + '/edit')
  }

  cancelEditMode () {
    this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
  }
}
</script>
