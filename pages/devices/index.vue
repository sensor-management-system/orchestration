<template>
  <div>
    <v-card>
      <v-tabs-items
        v-model="activeTab"
      >
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <v-row>
                <v-col cols="12" md="5">
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
                </v-col>
                <v-col cols="12" md="3">
                  <v-select v-model="selectedSearchType" label="Type" placeholder="Platform / Sensor" :items="searchTypes" />
                </v-col>
                <v-col cols="12" md="2">
                  <v-btn @click="basicSearch">
                    Search
                  </v-btn>
                </v-col>
                <v-col cols="12" md="1">
                  <v-btn @click="clearBasicSearch">
                    Clear
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item :eager="true">
          <v-card>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
                </v-col>
                <v-col cols="12" md="3">
                  <v-select label="Type" placeholder="Platform / Sensor" :items="searchTypes" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <v-autocomplete
                    v-model="manufactureToAdd"
                    label="add manufacture"
                    :items="notSelectedManufactures"
                    :item-text="(x) => x.name"
                    :item-value="(x) => x"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    fab
                    depressed
                    small
                    :disabled="manufactureToAdd == null"
                    @click="addSelectedManufacture"
                  >
                    <v-icon>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <v-chip
                    v-for="(manufacture, index) in selectedSearchManufactures"
                    :key="manufacture.id"
                    class="ma-2"
                    color="brown"
                    text-color="white"
                    :close="true"
                    @click:close="removeManufacture(index)"
                  >
                    {{ manufacture.name }}
                  </v-chip>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <v-autocomplete
                    v-model="instituteToAdd"
                    label="add institute"
                    :items="notSelectedInstitutes"
                    :item-text="(x) => x.name"
                    :item-value="(x) => x"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    fab
                    depressed
                    small
                    :disabled="instituteToAdd == null"
                    @click="addSelectedInstitute"
                  >
                    <v-icon>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <v-chip
                    v-for="(institute, index) in selectedSearchInstitutes"
                    :key="institute.id"
                    class="ma-2"
                    color="blue"
                    text-color="white"
                    :close="true"
                    @click:close="removeInstitute(index)"
                  >
                    {{ institute.name }}
                  </v-chip>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <v-autocomplete
                    v-model="parameterToAdd"
                    label="add parameter"
                    :items="notSelectedParameters"
                    :item-text="(x) => x.name"
                    :item-value="(x) => x"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    fab
                    depressed
                    small
                    :disabled="parameterToAdd == null"
                    @click="addSelectedParameter"
                  >
                    <v-icon>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <v-chip
                    v-for="(parameter, index) in selectedSearchParameter"
                    :key="parameter.id"
                    class="ma-2"
                    color="pink"
                    text-color="white"
                    :close="true"
                    @click:close="removeParameter(index)"
                  >
                    {{ parameter.name }}
                  </v-chip>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="extendedSearch">
                Search
              </v-btn>
              <v-btn @click="clearExtendedSearch">
                Clear
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>

    <h2>Results:</h2>
    <v-card v-for="result in searchResults" :key="result.id">
      <v-card-title>
        {{ result.name }}
      </v-card-title>
      <v-card-text>
        <p>{{ result.type }}</p>
        <p>Project {{ result.project }}</p>
        <p>State {{ result.state }}</p>
      </v-card-text>
      <v-card-actions v-if="result.devicetype == 'platform'">
        <v-btn :to="'/devices/platforms/' + result.id">
          View
        </v-btn>
        <v-btn>Copy</v-btn>
      </v-card-actions>
      <v-card-actions v-if="result.devicetype == 'device'">
        <v-btn>View</v-btn>
        <v-btn>Edit</v-btn>
        <v-btn>Copy</v-btn>
      </v-card-actions>
    </v-card>

    <v-card>
      <v-btn to="/devices/platforms">
        Add Platform
      </v-btn>
      <v-btn to="/devices/sensors">
        Add Sensor
      </v-btn>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import MasterDataService from '../../services/MasterDataService'
import DeviceService from '../../services/DeviceService'

import Manufacture from '../../models/Manufacture'
import Institute from '../../models/Institute'

// @ts-ignore
import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
// @ts-ignore
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Search',
      'Extended Search'
    ]
  }
}

@Component
export default class DevicesIndexPage extends Vue {
  private activeTab: number = 0

  private searchManufactures: Manufacture[] = []
  private selectedSearchManufactures: Manufacture[] = []
  private manufactureToAdd: Manufacture | null = null

  private searchInstitutes: Institute[] = []
  private selectedSearchInstitutes: Institute[] = []
  private instituteToAdd: Institute | null = null

  private searchParameter: Array<any> = []
  private selectedSearchParameter: Array<any> = []
  private parameterToAdd: any | null = null

  private searchResults: Array<object> = []
  private searchText: string | null = null
  private searchTypes: string[] = ['Sensor / Platform', 'Sensor', 'Platform']

  private selectedSearchType: string = 'Sensor / Platform';

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    MasterDataService.findAllManufactures().then((manufactures) => {
      this.searchManufactures = manufactures
    })
    MasterDataService.findAllInstitutes().then((institutes) => {
      this.searchInstitutes = institutes
    })
    MasterDataService.findAllParameter().then((paramater) => {
      this.searchParameter = paramater
    })
    DeviceService.findPlatformsAndSensors(this.searchText).then((findResults) => {
      this.searchResults = findResults
    })
    // make sure that all components (especially the dynamically passed ones) are rendered
    this.$nextTick(() => {
      this.$nuxt.$emit('AppBarContent:title', 'Devices')
    })
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarExtension:change')
  }

  basicSearch () {
    // only uses the text and the type (sensor or platform)
    this.runSearch(this.searchText)
  }

  clearBasicSearch () {
    this.searchText = null
    this.selectedSearchType = 'Sensor / Platform'
  }

  extendedSearch () {
    this.runSearch(this.searchText)
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufactures = []
    this.selectedSearchInstitutes = []
    this.selectedSearchParameter = []

    this.manufactureToAdd = null
    this.instituteToAdd = null
    this.parameterToAdd = null
  }

  runSearch (searchText: string | null) {
    DeviceService.findPlatformsAndSensors(searchText).then((findResults) => {
      this.searchResults = findResults
    })
  }

  addSelectedManufacture () {
    this.$set(this.selectedSearchManufactures, this.selectedSearchManufactures.length, this.manufactureToAdd)
    this.manufactureToAdd = null
  }

  removeManufacture (index: number) {
    this.$delete(this.selectedSearchManufactures, index)
  }

  addSelectedInstitute () {
    this.$set(this.selectedSearchInstitutes, this.selectedSearchInstitutes.length, this.instituteToAdd)
    this.instituteToAdd = null
  }

  removeInstitute (index: number) {
    this.$delete(this.selectedSearchInstitutes, index)
  }

  addSelectedParameter () {
    this.$set(this.selectedSearchParameter, this.selectedSearchParameter.length, this.parameterToAdd)
    this.parameterToAdd = null
  }

  removeParameter (index: number) {
    this.$delete(this.selectedSearchParameter, index)
  }

  get notSelectedManufactures () {
    const result = []
    const selectedManufactureIds = new Set()

    for (const singleManufacture of this.selectedSearchManufactures) {
      selectedManufactureIds.add(singleManufacture.id)
    }

    for (const singleManufacture of this.searchManufactures) {
      if (!selectedManufactureIds.has(singleManufacture.id)) {
        result.push(singleManufacture)
      }
    }
    return result
  }

  get notSelectedInstitutes () {
    const result = []
    const selectedInstituteIds = new Set()

    for (const singleInstitute of this.selectedSearchInstitutes) {
      selectedInstituteIds.add(singleInstitute.id)
    }

    for (const singleInstitute of this.searchInstitutes) {
      if (!selectedInstituteIds.has(singleInstitute.id)) {
        result.push(singleInstitute)
      }
    }

    return result
  }

  get notSelectedParameters () {
    const result = []
    const selectedParameterIds = new Set()

    for (const singleParameter of this.selectedSearchParameter) {
      selectedParameterIds.add(singleParameter.id)
    }

    for (const singleParameter of this.searchParameter) {
      if (!selectedParameterIds.has(singleParameter.id)) {
        result.push(singleParameter)
      }
    }
    return result
  }

  get navigation () {
    return [
      {
        disabled: false,
        exact: true,
        to: '/',
        text: 'Home'
      },
      {
        disabled: true,
        text: 'Devices'
      }
    ]
  }
}

</script>
