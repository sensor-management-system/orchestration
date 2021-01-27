<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
    <v-card outlined>
      <v-tabs-items
        v-model="activeTab"
      >
        <v-tab-item :eager="true">
          <v-form ref="basicForm">
            <!-- Basic data tab -->
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="platform.persistentIdentifier"
                      label="Persistent identifier (PID)"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="platform.shortName"
                      label="Short name"
                      required
                      class="required"
                      :rules="[rules.required]"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="platform.longName" label="Long name" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-combobox
                      v-model="platformStatusName"
                      label="Status"
                      :items="statusNames"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-combobox
                      v-model="platformPlatformTypeName"
                      label="Platform type"
                      :items="platformTypeNames"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-combobox
                      v-model="platformManufacturerName"
                      label="Manufacturer"
                      :items="manufacturerNames"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="platform.model"
                      label="Model"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="9">
                    <v-textarea v-model="platform.description" label="Description" rows="3" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="9">
                    <v-text-field
                      v-if="readonly"
                      v-model="platform.website"
                      label="Website"
                      placeholder="https://"
                      type="url"
                      :readonly="true"
                      :disabled="true"
                    >
                      <template slot="append">
                        <a v-if="platform.website.length > 0" :href="platform.website" target="_blank">
                          <v-icon>
                            mdi-open-in-new
                          </v-icon>
                        </a>
                      </template>
                    </v-text-field>
                    <v-text-field
                      v-else
                      v-model="platform.website"
                      label="Website"
                      placeholder="https://"
                      type="url"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="platform.serialNumber"
                      label="Serial number"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field v-model="platform.inventoryNumber" label="Inventory number" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-form>
        </v-tab-item>
        <!-- contact tab -->
        <v-tab-item :eager="true">
          <v-form ref="contactsForm" @submit.prevent>
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <ContactSelect v-model="platform.contacts" :readonly="!editMode" label="Add a contact" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-form>
        </v-tab-item>
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-title>
              Platform URN: {{ platformURN }}
            </v-card-title>
            <v-card-text>
              <AttachmentList v-model="platform.attachments" :readonly="!editMode" />
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
      <!-- Buttons for all tabs -->
      <v-btn
        v-if="!editMode"
        fab
        fixed
        bottom
        right
        color="secondary"
        @click="onEditButtonClick"
      >
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </v-card>
  </div>
</template>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, Watch, mixins } from 'nuxt-property-decorator'
import { Rules } from '@/mixins/Rules'

import AttachmentList from '@/components/AttachmentList.vue'
import ContactSelect from '@/components/ContactSelect.vue'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

@Component({
  components: {
    ContactSelect,
    AttachmentList
  }
})
// @ts-ignore
export default class PlatformIdPage extends mixins(Rules) {
  // data
  // first for the data to chose the elements
  private platformTypes: PlatformType[] = []
  private manufacturers: Manufacturer[] = []
  private states: Status[] = []

  // then for our platform that we want to change
  private platform: Platform = Platform.createEmpty()
  private platformBackup: Platform | null = null

  // and some general data for the page
  private editMode: boolean = false

  created () {
    this.initializeAppBar()
    this.registerButtonActions()
  }

  mounted () {
    this.$api.manufacturer.findAllPaginated().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    })
    this.$api.platformTypes.findAllPaginated().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of platform types failed')
    })
    this.$api.states.findAllPaginated().then((foundStates) => {
      this.states = foundStates
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of states failed')
    })
    this.loadPlatform().then((platform) => {
      if (platform === null) {
        this.$store.commit('appbar/setTitle', 'Add Platform')
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading platform failed')
    })
  }

  beforeDestroy () {
    this.unregisterButtonActions()
    this.$store.dispatch('appbar/setDefaults')
  }

  registerButtonActions () {
    this.$nuxt.$on('AppBarEditModeContent:save-btn-click', () => {
      this.save().then(() => {
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      }).catch(() => {
        this.$store.commit('snackbar/setError', 'Save failed')
      })
    })
    this.$nuxt.$on('AppBarEditModeContent:cancel-btn-click', () => {
      this.cancel()
    })
  }

  unregisterButtonActions () {
    this.$nuxt.$off('AppBarEditModeContent:save-btn-click')
    this.$nuxt.$off('AppBarEditModeContent:cancel-btn-click')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Basic Data',
        'Contacts',
        'Attachments'
      ],
      title: 'Platforms',
      saveBtnHidden: true,
      cancelBtnHidden: true
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  loadPlatform (): Promise<Platform|null> {
    return new Promise((resolve, reject) => {
      const platformId = this.$route.params.id
      if (!platformId) {
        this.createBackup()
        this.editMode = true
        resolve(null)
        return
      }
      this.editMode = false
      this.$api.platforms.findById(platformId).then((foundPlatform) => {
        this.platform = foundPlatform
        resolve(foundPlatform)
      }).catch((_error) => {
        reject(_error)
      })
    })
  }

  createBackup () {
    this.platformBackup = Platform.createFromObject(this.platform)
  }

  restoreBackup () {
    if (!this.platformBackup) {
      return
    }
    this.platform = this.platformBackup
    this.platformBackup = null
  }

  // methods
  save (): Promise<Platform|null> {
    return new Promise((resolve, reject) => {
      this.$api.platforms.save(this.platform).then((savedPlatform) => {
        this.platform = savedPlatform
        this.platformBackup = null
        this.editMode = false
        resolve(savedPlatform)
      }).catch((_error) => {
        reject(_error)
      })
    })
  }

  cancel () {
    this.restoreBackup()
    if (this.platform.id) {
      this.editMode = false
    } else {
      this.$router.push('/search/platforms')
    }
  }

  onEditButtonClick () {
    this.createBackup()
    this.editMode = true
  }

  get platformURN () {
    // return the current platform urn to display it in the form
    const removeWhitespace = (text: string) => {
      return text.replace(' ', '_')
    }
    let partPlatformType = '[platformtype]'
    if (this.platform.platformTypeUri !== '') {
      const ptIndex = this.platformTypes.findIndex(pt => pt.uri === this.platform.platformTypeUri)
      if (ptIndex > -1) {
        partPlatformType = this.platformTypes[ptIndex].name
      }
    }

    let partShortName = '[short_name]'
    if (this.platform.shortName !== '') {
      partShortName = removeWhitespace(this.platform.shortName)
    }

    return partPlatformType + '_' + partShortName
  }

  get readonly () {
    return !this.editMode
  }

  get manufacturerNames () : string[] {
    return this.manufacturers.map(m => m.name)
  }

  get platformManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.platform.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.platform.manufacturerName
  }

  set platformManufacturerName (newName: string) {
    this.platform.manufacturerName = newName
    const manufacturerIndex = this.manufacturers.findIndex(m => m.name === newName)
    if (manufacturerIndex > -1) {
      this.platform.manufacturerUri = this.manufacturers[manufacturerIndex].uri
    } else {
      this.platform.manufacturerUri = ''
    }
  }

  get statusNames () : string[] {
    return this.states.map(s => s.name)
  }

  get platformStatusName (): string {
    const statusIndex = this.states.findIndex(s => s.uri === this.platform.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.platform.statusName
  }

  set platformStatusName (newName: string) {
    this.platform.statusName = newName
    const statusIndex = this.states.findIndex(s => s.name === newName)
    if (statusIndex > -1) {
      this.platform.statusUri = this.states[statusIndex].uri
    } else {
      this.platform.statusUri = ''
    }
  }

  get platformTypeNames () : string[] {
    return this.platformTypes.map(t => t.name)
  }

  get platformPlatformTypeName () : string {
    const platformTypeIndex = this.platformTypes.findIndex(t => t.uri === this.platform.platformTypeUri)
    if (platformTypeIndex > -1) {
      return this.platformTypes[platformTypeIndex].name
    }
    return this.platform.platformTypeName
  }

  set platformPlatformTypeName (newName: string) {
    this.platform.platformTypeName = newName
    const platformTypeIndex = this.platformTypes.findIndex(t => t.name === newName)
    if (platformTypeIndex > -1) {
      this.platform.platformTypeUri = this.platformTypes[platformTypeIndex].uri
    } else {
      this.platform.platformTypeUri = ''
    }
  }

  @Watch('platform', { immediate: true, deep: true })
  // @ts-ignore
  onPlatformChanged (val: Platform) {
    if (val.id) {
      this.$store.commit('appbar/setTitle', val?.shortName || 'Add Platform')
    }
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$store.commit('appbar/setSaveBtnHidden', !editMode)
    this.$store.commit('appbar/setCancelBtnHidden', !editMode)
  }
}

</script>
