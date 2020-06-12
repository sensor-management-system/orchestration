<template>
  <div>
    <!-- The very first: the snackback if we have some messages from the system -->
    <v-snackbar v-model="showSaveSuccess" top color="success">
      Save successful
      <v-btn fab @click="showSaveSuccess = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-snackbar>
    <v-snackbar v-model="showLoadingError" top color="error">
      Loading platform failed
      <v-btn fab @click="showLoadingError = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-snackbar>

    <!-- Then the breadcrumps for navigation -->
    <v-breadcrumbs :items="navigation" />
    <h1>{{ verb }} Platform</h1>

    <v-form>
      <v-card outlined>
        <v-tabs
          v-model="activeTabIdx"
          background-color="grey lighten-3"
        >
          <v-tab>Basic data</v-tab>
          <v-tab>Contacts</v-tab>
          <v-tab-item>
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
                    <v-text-field v-model="platform.shortName" label="short name" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="platform.longName" label="Long name" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <!-- TODO: Auch hier den Namen und die URI ändern!!!
                    -->
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
                      v-model="platformStatusName"
                      label="Status"
                      :items="statusNames"
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
                  <v-col cols="12" md="5">
                    <v-textarea v-model="platform.description" label="Description" rows="3" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="platform.website"
                      label="Website"
                      placeholder="https://"
                      :readonly="readonly"
                      :disabled="readonly"
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
              <v-card-actions>
                <v-btn
                  text
                  @click="nextTab"
                >
                  next ❯
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <!-- contacts tab -->
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <ContactSelect :selected-contacts.sync="platform.contacts" :readonly="!isInEditMode" />
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="previousTab"
                >
                  ❮ previous
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
        </v-tabs>
        <!-- Buttons for all tabs -->
        <div v-if="!isInEditMode">
          <v-btn
            fab
            fixed
            bottom
            right
            color="secondary"
            @click="switchIntoEditMode"
          >
            <v-icon>
              mdi-pencil
            </v-icon>
          </v-btn>
        </div>
        <div v-if="isInEditMode">
          <v-btn
            fab
            fixed
            bottom
            right
            color="primary"
            @click="save"
          >
            <v-icon>
              mdi-content-save
            </v-icon>
          </v-btn>
        </div>
      </v-card>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import VCService from '../../../services/VCService'
import SmsService from '../../../services/SmsService'

import Platform from '../../../models/Platform'

// @ts-ignore
import ContactSelect from '../../../components/ContactSelect.vue'
import Manufacturer from '../../../models/Manufacturer'
import PlatformType from '../../../models/PlatformType'
import Status from '../../../models/Status'

@Component({
  components: { ContactSelect }
})
// @ts-ignore
export default class PlatformIdPage extends Vue {
  // data
  // first for the data to chose the elements
  private platformTypes: PlatformType[] = []
  private manufacturers: Manufacturer[] = []
  private states: Status[] = []

  // then for our platform that we want to change
  private platform: Platform = Platform.createEmpty()

  // and some general data for the page
  private activeTabIdx: number = 0
  private showSaveSuccess: boolean = false
  private showLoadingError: boolean = false
  private isInEditMode: boolean = false

  mounted () {
    this.showLoadingError = false
    VCService.findAllManufacturers().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    })
    VCService.findAllPlatformTypes().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    VCService.findAllStates().then((foundStates) => {
      this.states = foundStates
    })
    this.loadPlatform()
  }

  loadPlatform () {
    const platformId = this.$route.params.id
    if (platformId) {
      this.isInEditMode = false
      SmsService.findPlatformById(platformId).then((foundPlatform) => {
        this.platform = foundPlatform
      }).catch(() => {
        // We don't take the error directly
        this.showLoadingError = true
      })
    } else {
      this.isInEditMode = true
    }
  }

  // methods
  save () {
    this.showSaveSuccess = false
    SmsService.savePlatform(this.platform).then((savedPlatform) => {
      this.platform = savedPlatform
      this.showSaveSuccess = true
      // this.$router.push('/devices')
    })
  }

  switchIntoEditMode () {
    this.isInEditMode = true
  }

  previousTab () {
    this.activeTabIdx -= 1
  }

  nextTab () {
    this.activeTabIdx += 1
  }

  get platformURN () {
    // return the current platform urn to display it in the form
    const removeWhitespace = (text: string) => {
      return text.replace(' ', '_')
    }
    // TODO: I don't have the platform type
    // I just have the platformTypeUri
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

  get verb (): string {
    // return the verb (do we add a platform or do we edit one?)
    let verb = 'Add'
    if (this.$route.params.id) {
      if (this.isInEditMode) {
        verb = 'Edit'
      } else {
        verb = 'View'
      }
    }
    return verb
  }

  get readonly () {
    return !this.isInEditMode
  }

  get navigation () {
    // navigation for the breadcrumps
    return [
      {
        disabled: false,
        exact: true,
        to: '/',
        text: 'Home'
      },
      {
        disabled: false,
        exact: true,
        to: '/devices',
        text: 'Devices'
      },
      {
        disabled: true,
        text: this.verb + ' Platform'
      }
    ]
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
}

</script>
