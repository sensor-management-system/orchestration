<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
  <v-card
    v-if="value"
    outlined
  >
    <v-breadcrumbs :items="breadcrumbs" divider=">" />
    <v-expansion-panels multiple>
      <v-expansion-panel>
        <v-expansion-panel-header>
          <span v-if="value.isPlatform()">
            Platform overview
          </span>
          <span v-else>
            Device overview
          </span>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <template v-if="description">
            {{ description }}
          </template>
          <template v-else-if="value.isPlatform()">
            <span class="text--disabled">The selected platform has no description.</span>
          </template>
          <template v-else-if="value.isDevice()">
            <span class="text--disabled">The selected device has no description.</span>
          </template>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>
          Mount information
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-form
            ref="mountUpdateForm"
            @submit.prevent
          >
            <v-card-text>
              <v-row>
                <v-col>
                  <label>Mounted:</label>
                  {{ value.unpack().date }}
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  md="3"
                >
                  <v-text-field
                    v-model="offsetX"
                    label="Offset (x)"
                    type="number"
                    :readonly="readonly"
                    :disabled="readonly"
                    required
                    :rules="[rules.numericRequired]"
                    class="m-annotated"
                    @wheel.prevent
                  />
                </v-col>
                <v-col
                  cols="12"
                  md="3"
                >
                  <v-text-field
                    v-model="offsetY"
                    label="Offset (y)"
                    type="number"
                    :readonly="readonly"
                    :disabled="readonly"
                    required
                    :rules="[rules.numericRequired]"
                    class="m-annotated"
                    @wheel.prevent
                  />
                </v-col>
                <v-col
                  cols="12"
                  md="3"
                >
                  <v-text-field
                    v-model="offsetZ"
                    label="Offset (z)"
                    type="number"
                    :readonly="readonly"
                    :disabled="readonly"
                    required
                    :rules="[rules.numericRequired]"
                    class="m-annotated"
                    @wheel.prevent
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-autocomplete
                    v-model="mountContact"
                    :items="contacts"
                    label="Contact"
                    clearable
                    required
                    :rules="[rules.required]"
                    :readonly="readonly"
                    :disabled="readonly"
                  />
                </v-col>
                <v-col>
                  <v-btn v-if="!readonly" small @click="selectCurrentUserAsMountContact">
                    Set current user
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="12">
                  <v-textarea
                    v-model="mountDescription"
                    label="Description"
                    rows="3"
                    :readonly="readonly"
                    :disabled="readonly"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-form>
          <div
            v-if="value && !readonly"
          >
            <v-btn v-if="isMountedOnSelectedDate" @click="overwriteExistingMountAction">
              Update
            </v-btn>
            <v-btn v-else @click="addNewMountAction">
              Update
            </v-btn>
            <v-menu
              v-if="!isMountedOnSelectedDate"
              close-on-click
              close-on-content-click
              offset-x
              right
              z-indx="999"
            >
              <template #activator="{ on }">
                <v-btn
                  data-role="property menu"
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
                  @click="overwriteExistingMountAction"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Update for {{ value.unpack().date | dateToDateTimeStringHHMM }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  dense
                  @click="addNewMountAction"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Update for {{ selectedDate | dateToDateTimeStringHHMM }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!readonly">
        <v-expansion-panel-header class="unmount-expansion-panel">
          Unmount
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ConfigurationsSelectedItemUnmountForm
            v-if="value"
            :key="valueKey"
            :contacts="contacts"
            :readonly="readonly"
            @remove="remove"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script lang="ts">
/**
* @file provides a component to display information about a selected tree node
* @author <marc.hanisch@gfz-potsdam.de>
*/
import { Vue, Component, Prop, Watch, mixins } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

// @ts-ignore
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'

import { Contact } from '@/models/Contact'

import { Rules } from '@/mixins/Rules'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { IUnmountData } from '@/viewmodels/IUnmountData'
import { PlatformNode } from '@/viewmodels/PlatformNode'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

/**
* A class component to display information about a selected tree node
* @extends Vue
*/
@Component({
  components: {
    ConfigurationsSelectedItemUnmountForm
  },
  filters: {
    dateToDateTimeStringHHMM
  }
})
// @ts-ignore
export default class ConfigurationsSelectedItem extends mixins(Rules) {
  private offsetX: number = 0.0
  private offsetY: number = 0.0
  private offsetZ: number = 0.0

  private mountContact: Contact | null = null

  private mountDescription: string = ''

  /**
   * the selected node
   */
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value: ConfigurationsTreeNode | null

  @Prop({
    default: DateTime.utc(),
    type: DateTime
  })
  readonly selectedDate!: DateTime

  /**
   * the breadcrumbs string array
   */
  @Prop({
    default: () => [],
    type: Array
  })
  // @ts-ignore
  readonly breadcrumbs: string[]

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * returns the description of a node
   *
   * @return {string} the description
   */
  get description (): string {
    if (!this.value) {
      return ''
    }
    if (this.value.isPlatform()) {
      return (this.value as PlatformNode).unpack().platform.description
    }
    return (this.value as DeviceNode).unpack().device.description
  }

  get isMountedOnSelectedDate (): boolean {
    if (!this.value) {
      return false
    }
    const value = this.value
    const node = value.unpack()
    const date = node.date
    return date.equals(this.selectedDate)
  }

  get valueKey (): string {
    if (this.value && this.value.id) {
      return this.value.id
    }
    return 'no-key'
  }

  /**
   * triggers a remove event for a node
   *
   * @fires ConfigurationsSelectedItem#remove
   */
  remove (unmountData: IUnmountData) {
    /**
     * fires an input event
     * @event ConfigurationsSelectedItem#remove
     * @type {ConfigurationsTreeNode}
     */
    this.$emit('remove', this.value, unmountData.contact, unmountData.description)
  }

  overwriteExistingMountAction () {
    if (this.validateMountUpdateForm()) {
      this.$emit(
        'overwriteExistingMountAction',
        this.value,
        {
          offsetX: this.offsetX,
          offsetY: this.offsetY,
          offsetZ: this.offsetZ,
          contact: this.mountContact,
          description: this.mountDescription
        }
      )
    } else {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
    }
  }

  addNewMountAction () {
    if (this.validateMountUpdateForm()) {
      this.$emit(
        'addNewMountAction',
        this.value,
        {
          offsetX: this.offsetX,
          offsetY: this.offsetY,
          offsetZ: this.offsetZ,
          contact: this.mountContact,
          description: this.mountDescription
        }
      )
    } else {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
    }
  }

  selectCurrentUserAsMountContact () {
    const currentUserMail = this.$store.getters['oidc/userEmail']
    if (currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === currentUserMail)
      if (userIndex > -1) {
        this.mountContact = this.contacts[userIndex]
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  @Watch('value')
  onValueChange (node: ConfigurationsTreeNode | null) {
    this.offsetX = node?.unpack().offsetX || 0.0
    this.offsetY = node?.unpack().offsetY || 0.0
    this.offsetZ = node?.unpack().offsetZ || 0.0
    this.mountContact = node?.unpack().contact || null
    this.mountDescription = node?.unpack().description || ''
  }

  validateMountUpdateForm (): boolean {
    return (this.$refs.mountUpdateForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style scoped>
/* the m-annotated class is to add the unit (meters) to the fields */
.m-annotated::after {
  content: " m";
  white-space: pre;
}
</style>
