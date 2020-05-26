<template>
  <div>
    <v-breadcrumbs :items="navigation" />
    <h1>Devices</h1>

    <v-card>
      <v-tabs
        v-model="activeSearchTypeTabIdx"
        background-color="grey lighten-3"
      >
        <v-tab>Basic search</v-tab>
        <v-tab>Extended search</v-tab>
        <v-tab-item>
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
        <v-tab-item>
          <v-card>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
                </v-col>
                <v-col cols="12" md="3">
                  <v-select label="search type" placeholder="Platform / Sensor" :items="searchTypes" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <v-autocomplete
                    v-model="manufacturerToAdd"
                    label="add manufacturer"
                    :items="notSelectedManufacturers"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    fab
                    depressed
                    small
                    :disabled="manufacturerToAdd == null"
                    @click="addSelectedManufacturer"
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
                    v-for="(manufacturer, index) in selectedSearchManufacturers"
                    :key="manufacturer.id"
                    class="ma-2"
                    color="brown"
                    text-color="white"
                    :close="true"
                    @click:close="removeManufacture(index)"
                  >
                    {{ manufacturer }}
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
      </v-tabs>
    </v-card>

    <h2>Results:</h2>
    <v-card v-for="result in searchResults" :key="result.devicetype + result.id">
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
        <!-- We must make sure if we want to allow deleting here.
             For developlement it was needed to clean up the things
             a bit easier.
        -->
        <!--<v-btn @click="deletePlatform(result.id)">
          Delete
        </v-btn>-->
      </v-card-actions>
      <v-card-actions v-if="result.devicetype == 'device'">
        <v-btn :to="'devices/devices/' + result.id">
          View
        </v-btn>
        <v-btn>Copy</v-btn>
      </v-card-actions>
    </v-card>

    <v-card>
      <v-btn to="/devices/platforms">
        Add Platform
      </v-btn>
      <v-btn to="/devices/devices">
        Add Device
      </v-btn>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import MasterDataService from '../../services/MasterDataService'
import DeviceService from '../../services/DeviceService'

import Institute from '../../models/Institute'

@Component
export default class DevicesIndexPage extends Vue {
  private activeSearchTypeTabIdx: number = 0

  private searchManufacturers: String[] = []
  private selectedSearchManufacturers: String[] = []
  private manufacturerToAdd: String | null = null

  private searchInstitutes: Institute[] = []
  private selectedSearchInstitutes: Institute[] = []
  private instituteToAdd: Institute | null = null

  private searchResults: Array<object> = []
  private searchText: string | null = null
  private searchTypes: string[] = ['Sensor / Platform', 'Sensor', 'Platform']

  private selectedSearchType: string = 'Sensor / Platform';

  mounted () {
    MasterDataService.findAllManufacturers().then((manufacturers) => {
      this.searchManufacturers = manufacturers
    })
    MasterDataService.findAllInstitutes().then((institutes) => {
      this.searchInstitutes = institutes
    })
    DeviceService.findPlatformsAndSensors(this.searchText).then((findResults) => {
      this.searchResults = findResults
    })
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

    this.selectedSearchManufacturers = []
    this.selectedSearchInstitutes = []

    this.manufacturerToAdd = null
    this.instituteToAdd = null
  }

  runSearch (searchText: string | null) {
    DeviceService.findPlatformsAndSensors(searchText).then((findResults) => {
      this.searchResults = findResults
    })
  }

  addSelectedManufacturer () {
    this.$set(
      this.selectedSearchManufacturers,
      this.selectedSearchManufacturers.length,
      this.manufacturerToAdd
    )
    this.manufacturerToAdd = null
  }

  removeManufacture (index: number) {
    this.$delete(this.selectedSearchManufacturers, index)
  }

  addSelectedInstitute () {
    this.$set(this.selectedSearchInstitutes, this.selectedSearchInstitutes.length, this.instituteToAdd)
    this.instituteToAdd = null
  }

  removeInstitute (index: number) {
    this.$delete(this.selectedSearchInstitutes, index)
  }

  deletePlatform (id: number) {
    DeviceService.deletePlatform(id).then(() => {
      this.runSearch(this.searchText)
    })
  }

  get notSelectedManufacturers () {
    const result = []
    const selectedManufactures = new Set()

    for (const singleManufacturer of this.selectedSearchManufacturers) {
      selectedManufactures.add(singleManufacturer)
    }

    for (const singleManufacturer of this.searchManufacturers) {
      if (!selectedManufactures.has(singleManufacturer)) {
        result.push(singleManufacturer)
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
