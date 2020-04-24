<template>
  <div>
    <v-row>
      <h1>Devices</h1>
    </v-row>
    <v-card>
      <v-row>
        <v-col>
          <v-form>
            <v-container>
              <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
              <v-select label="Type" placeholder="Platform / Sensor" :items="searchTypes" />
              <v-btn @click="search">search</v-btn>
              <a href="#" @click="toggleExtendedSearch">
                <div v-if="!showExtendedSearch">Show extended search</div>
                <div v-else>Hide extended search</div>
              </a>
            </v-container>
          </v-form>
        </v-col>
      </v-row>
    </v-card>
    <v-card v-if="showExtendedSearch">
      Extended Search
      <v-row>
        <v-col>
          <v-form>
            <v-container>
              <v-select label="Manufacture" :items="searchManufactures" :item-text="(x) => x.name" :item-value="(x) => x.id" />
              <v-btn>+</v-btn>
              <v-select label="Institute" :items="searchInstitutes" :item-text="(x) => x.name" :item-value="(x) => x.id" />
              <v-btn>+</v-btn>
              <v-select label="Parameter" :items="searchParameter" :item-text="(x) => x.name" :item-value="(x) => x.id" />
              <v-btn>+</v-btn>
            </v-container>
          </v-form>
        </v-col>
      </v-row>
    </v-card>
    <p>Results:</p>
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
        <v-btn>View</v-btn>
        <v-btn :to="'/devices/platforms/' + result.id">
          Edit
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
      <v-btn>Add Sensor</v-btn>
    </v-card>
  </div>
</template>

<script>

import masterdataservice from '../../services/masterdataservice'
import deviceservice from '../../services/deviceservice'

export default {
  data () {
    return {
      showExtendedSearch: false,
      searchManufactures: [],
      searchInstitutes: [],
      searchParameter: [],
      searchTypes: ['Platform / Sensor', 'Sensor', 'Platform'],
      searchResults: [],
      searchText: null
    }
  },
  mounted () {
    masterdataservice.findAllManufactures().then((manufactures) => {
      this.searchManufactures = manufactures
    })
    masterdataservice.findAllInstitutes().then((institutes) => {
      this.searchInstitutes = institutes
    })
    masterdataservice.findAllParameter().then((paramater) => {
      this.searchParameter = paramater
    })
    deviceservice.findPlatformsAndSensors(this.searchText).then((findResults) => {
      this.searchResults = findResults
    })
  },
  methods: {
    toggleExtendedSearch (event) {
      event.preventDefault()
      this.showExtendedSearch = !this.showExtendedSearch
    },
    search () {
      deviceservice.findPlatformsAndSensors(this.searchText).then((findResults) => {
        this.searchResults = findResults
      })
    }
  }
}

</script>
