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
          <v-tab>Persons</v-tab>
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
          <!-- responsible persons tab -->
          <v-tab-item>
            <v-card
              flat
            >
              <v-card-title>
                Platform URN: {{ platformURN }}
              </v-card-title>
              <v-card-text>
                <v-row v-if="isInEditMode">
                  <v-col cols="5" md="3">
                    <v-autocomplete
                      v-model="personToAdd"
                      :items="possiblePersonsToSelect"
                      :item-text="(x) => x.name"
                      :item-value="(x) => x.id"
                      label="add a person"
                      no-data-text="There is no person to add"
                    />
                  </v-col>
                  <v-col cols="5" md="1">
                    <v-btn
                      fab
                      depressed
                      small
                      :disabled="personToAdd == null"
                      @click="addSelectedPerson"
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
                      v-for="(personId, index) in platform.responsiblePersonIds"
                      :key="personId"
                      class="ma-2"
                      color="indigo"
                      text-color="white"
                      :close="isInEditMode"
                      @click:close="removePerson(index)"
                    >
                      <v-avatar left>
                        <v-icon>mdi-account-circle</v-icon>
                      </v-avatar>
                      {{ findPersonNameById(personId) }}
                    </v-chip>
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

import MasterDataService from '../../../services/MasterDataService'
import PersonService from '../../../services/PersonService'
import DeviceService from '../../../services/DeviceService'

import Manufacture from '../../../models/Manufacture'
import PlatformType from '../../../models/PlatformType'
import Person from '../../../models/Person'
import Platform from '../../../models/Platform'

@Component
export default class PlatformIdPage extends Vue {
  // data
  // first for the data to chose the elements
  private platformTypes: PlatformType[] = []
  private manufactures: Manufacture[] = []
  private types: Array<string> = ['Type 01']
  private persons: Person[] = []

  // then for our platform that we want to change
  private platform: Platform = Platform.createEmpty()

  // for a person that we may want to add
  private personToAdd: number | null = null

  // and some general data for the page
  private activeTabIdx: number = 0
  private showSaveSuccess: boolean = false
  private showLoadingError: boolean = false
  private isInEditMode: boolean = false

  mounted () {
    this.showLoadingError = false
    MasterDataService.findAllManufactures().then((foundManufactures) => {
      this.manufactures = foundManufactures
    })
    MasterDataService.findAllPlatformTypes().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    PersonService.findAllPersons().then((foundPersons) => {
      this.persons = foundPersons
    })

    this.loadPlatform()
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

  // methods
  addSelectedPerson () {
    this.$set(this.platform.responsiblePersonIds, this.platform.responsiblePersonIds.length, this.personToAdd)
    this.personToAdd = null
  }

  removePerson (index: number) {
    this.$delete(this.platform.responsiblePersonIds, index)
  }

  save () {
    this.showSaveSuccess = false
    DeviceService.savePlatform(this.platform).then(() => {
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

  findPersonNameById (personId: number | null): string {
    let foundPerson = null
    for (const singlePerson of this.persons) {
      if (singlePerson.id === personId) {
        foundPerson = singlePerson
        break
      }
    }
    if (foundPerson != null) {
      return foundPerson.name
    }
    return 'Unknown person'
  }

  get possiblePersonsToSelect (): Person[] {
    // this here gives an filtered person array back
    // it takes the original set from the person service
    // but takes all out that are already in use for the
    // current platform
    //
    // this way it is not possible to select the same person
    // multiple times
    const result = []
    const usedPersonIds: Set<number> = new Set()

    for (const personId of this.platform.responsiblePersonIds) {
      usedPersonIds.add(personId)
    }
    for (const person of this.persons) {
      if (person.id != null && !usedPersonIds.has(person.id)) {
        result.push(person)
      }
    }
    return result
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
