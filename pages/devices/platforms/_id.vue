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

    <v-form>
      <v-card outlined>
        <v-tabs-items
          v-model="activeTab"
        >
          <v-tab-item :eager="true">
            <!-- Basic data tab -->
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="platform.shortName" label="short name" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="platform.longName" label="long name" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="platform.platformTypeId"
                      label="type"
                      :items="platformTypes"
                      :item-text="(x) => x.name"
                      :item-value="(x) => x.id"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="platform.manufactureId"
                      label="manufacturer"
                      :items="manufactures"
                      :item-text="(x) => x.name"
                      :item-value="(x) => x.id"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-col>
                  <!--<v-select v-model="platform.type" label="type" :items="types" />-->
                </v-row>
                <v-divider />
                <v-row>
                  <v-col cols="12" md="5">
                    <v-textarea v-model="platform.description" label="Description" rows="3" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field v-model="platform.website" label="Website" placeholder="https://" :readonly="readonly" :disabled="readonly" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <!-- responsible persons tab -->
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <PersonSelect :selected-persons.sync="platform.responsiblePersons" :readonly="!isInEditMode" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-btn
          v-if="!isInEditMode"
          fab
          fixed
          bottom
          right
          color="secondary"
          @click="toggleEditMode"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import MasterDataService from '../../../services/MasterDataService'
import DeviceService from '../../../services/DeviceService'

import Manufacture from '../../../models/Manufacture'
import PlatformType from '../../../models/PlatformType'
import Platform from '../../../models/Platform'

// @ts-ignore
import PersonSelect from '../../../components/PersonSelect.vue'
// @ts-ignore
import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
// @ts-ignore
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'

@Component
// @ts-ignore
export class AppBarEditModeContentExtended extends AppBarEditModeContent {
  get title (): string {
    return 'Add Platform'
  }
}

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Basic Data',
      'Persons'
    ]
  }
}

@Component({
  components: { PersonSelect }
})
// @ts-ignore
export default class PlatformIdPage extends Vue {
  // data
  // first for the data to chose the elements
  private platformTypes: PlatformType[] = []
  private manufactures: Manufacture[] = []
  private types: Array<string> = ['Type 01']

  // then for our platform that we want to change
  private platform: Platform = Platform.createEmpty()

  // and some general data for the page
  private activeTab: number = 0
  private showSaveSuccess: boolean = false
  private showLoadingError: boolean = false
  private editMode: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContentExtended)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      if (this.platform && this.platform.id) {
        this.toggleEditMode()
      } else {
        this.$router.push('/devices')
      }
    })

    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    this.showLoadingError = false
    MasterDataService.findAllManufactures().then((foundManufactures) => {
      this.manufactures = foundManufactures
    })
    MasterDataService.findAllPlatformTypes().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    this.loadPlatform()

    // make sure that all components (especially the dynamically passed ones) are rendered
    this.$nextTick(() => {
      this.$nuxt.$emit('AppBarContent:save-button-hidden', !this.editMode)
      this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !this.editMode)
    })
  }

  destroyed () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
  }

  loadPlatform () {
    const platformId = this.$route.params.id
    if (platformId) {
      this.isInEditMode = false
      DeviceService.findPlatformById(platformId).then((foundPlatform) => {
        this.platform = foundPlatform
      }).catch(() => {
        // We don't take the error directly
        this.showLoadingError = true
      })
    } else {
      this.isInEditMode = true
    }
  }

  get isInEditMode (): boolean {
    return this.editMode
  }

  set isInEditMode (editMode: boolean) {
    this.editMode = editMode
  }

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$nuxt.$emit('AppBarContent:save-button-hidden', !editMode)
    this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !editMode)
  }

  // methods
  save () {
    this.showSaveSuccess = false
    DeviceService.savePlatform(this.platform).then(() => {
      this.showSaveSuccess = true
      // this.$router.push('/devices')
      this.toggleEditMode()
    })
  }

  get platformURN () {
    // return the current platform urn to display it in the form
    const removeWhitespace = (text: string) => {
      return text.replace(' ', '_')
    }

    let partPlatformType = '[platformtype]'
    if (this.platform.platformTypeId != null) {
      let foundPlatformType = null
      for (const singlePlatformType of this.platformTypes) {
        if (singlePlatformType.id === this.platform.platformTypeId) {
          foundPlatformType = singlePlatformType
          break
        }
      }
      if (foundPlatformType != null) {
        partPlatformType = removeWhitespace(foundPlatformType.name)
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
}

</script>
