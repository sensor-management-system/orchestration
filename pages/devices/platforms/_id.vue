<template>
  <div>
    <h1>Platform URN</h1>

    <v-form>
      <v-card>
        <v-card-text>
          <v-select v-model="platform.platformTypeId" label="platform type" :items="platformTypes" :item-text="(x) => x.name" :item-value="(x) => x.id" />
          <v-text-field v-model="platform.shortName" label="platform short name" />
          <v-text-field v-model="platform.longName" label="platform long name" />
          <v-textarea v-model="platform.description" label="description" />
          <v-select v-model="platform.manufactureId" label="manufacture" :items="manufactures" :item-text="(x) => x.name" :item-value="(x) => x.id" />
          <!--<v-select v-model="platform.type" label="type" :items="types" />-->
          <v-text-field v-model="platform.website" label="link to website" />
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          Responsible persons
        </v-card-title>
        <v-card-text>
          <div v-for="(personId, index) in platform.responsiblePersonIds" :key="index">
            <v-select v-model="platform.responsiblePersonIds[index]" label="Person" :items="persons" :item-text="(x) => x.name" :item-value="(x) => x.id" />
            <v-btn @click="removePerson(index)">
              Delete
            </v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="addEmptyPerson()">
            +
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card>
        <v-card-actions>
          <v-btn @click="goBack()">
            Cancel
          </v-btn>
          <v-btn @click="save()">
            Save
          </v-btn>
          <v-btn>Save and create copy</v-btn>
        </v-card-actions>
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
  private platformTypes: PlatformType[] = []
  private manufactures: Manufacture[] = []
  private types: Array<string> = ['Type 01']
  private persons: Person[] = []
  private platform: Platform = Platform.createEmpty()

  // mounted
  mounted () {
    MasterDataService.findAllManufactures().then((foundManufactures) => {
      this.manufactures = foundManufactures
    })
    MasterDataService.findAllPlatformTypes().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    PersonService.findAllPersons().then((foundPersons) => {
      this.persons = foundPersons
    })

    const platformId = this.$route.params.id
    if (platformId) {
      DeviceService.findPlatformById(platformId).then((foundPlatform) => {
        this.platform = foundPlatform
      }).catch((error: any) => {
        console.error(error)
      })
    }
  }

  // methods
  goBack () {
    this.$router.back()
  }

  addEmptyPerson () {
    this.$set(this.platform.responsiblePersonIds, this.platform.responsiblePersonIds.length, undefined)
  }

  removePerson (index: number) {
    this.$delete(this.platform.responsiblePersonIds, index)
  }

  save () {
    DeviceService.savePlatform(this.platform).then(() => {
      this.$router.push('/devices')
    })
  }
}

</script>
