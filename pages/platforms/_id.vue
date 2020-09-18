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
                    <ContactSelect v-model="platform.contacts" :readonly="!isInEditMode" label="Add a contact" />
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
              <AttachmentList v-model="platform.attachments" :readonly="!isInEditMode" />
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
      <!-- Buttons for all tabs -->
      <v-btn
        v-if="!isInEditMode"
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
@import "~/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, Watch, mixins } from 'nuxt-property-decorator'
import { Rules } from '@/mixins/Rules'

import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'
import AttachmentList from '@/components/AttachmentList.vue'
import ContactSelect from '@/components/ContactSelect.vue'

import Manufacturer from '@/models/Manufacturer'
import Platform from '@/models/Platform'
import PlatformType from '@/models/PlatformType'
import Status from '@/models/Status'

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Basic Data',
      'Contacts',
      'Attachments'
    ]
  }
}

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
  private platformCopy: Platform | null = null

  // and some general data for the page
  private activeTab: number = 0
  private editMode: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      this.cancel()
    })

    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    this.$api.manufacturer.findAll().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    })
    this.$api.platformTypes.findAll().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    this.$api.states.findAll().then((foundStates) => {
      this.states = foundStates
    })
    this.loadPlatform()

    // make sure that all components (especially the dynamically passed ones) are rendered
    this.$nextTick(() => {
      if (!this.$route.params.id) {
        this.$nuxt.$emit('AppBarContent:title', 'Add Platform')
      }
      this.$nuxt.$emit('AppBarContent:save-button-hidden', !this.editMode)
      this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !this.editMode)
    })
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarContent:save-button-click')
    this.$nuxt.$off('AppBarContent:cancel-button-click')
    this.$nuxt.$off('AppBarExtension:change')
  }

  loadPlatform () {
    const platformId = this.$route.params.id
    if (!platformId) {
      this.createWorkingCopy()
      this.isInEditMode = true
      return
    }
    this.isInEditMode = false
    this.$api.platforms.findById(platformId).then((foundPlatform) => {
      this.platform = foundPlatform
    }).catch(() => {
      // We don't take the error directly
      this.$store.commit('snackbar/setError', 'Loading platform failed')
    })
  }

  get isInEditMode (): boolean {
    return this.editMode
  }

  set isInEditMode (editMode: boolean) {
    this.editMode = editMode
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$nuxt.$emit('AppBarContent:save-button-hidden', !editMode)
    this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !editMode)
  }

  createWorkingCopy () {
    this.platformCopy = this.platform
    this.platform = Platform.createFromObject(this.platformCopy)
  }

  restoreWorkingCopy () {
    if (!this.platformCopy) {
      return
    }
    this.platform = this.platformCopy
    this.platformCopy = null
  }

  // methods
  save () {
    this.$api.platforms.save(this.platform).then((savedPlatform) => {
      this.platform = savedPlatform
      this.platformCopy = null
      this.isInEditMode = false
      this.$store.commit('snackbar/setSuccess', 'Save successful')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  cancel () {
    this.restoreWorkingCopy()
    if (this.platform && this.platform.id) {
      this.isInEditMode = false
    } else {
      this.$router.push('/search/platforms')
    }
  }

  onEditButtonClick () {
    this.createWorkingCopy()
    this.isInEditMode = true
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
    return !this.isInEditMode
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
      this.$nuxt.$emit('AppBarContent:title', 'Platform ' + val.shortName)
    }
  }
}

</script>
