<template>
  <div>
    <h1>Platform URN</h1>

    <v-form>
      <v-card>
        <v-card-text>
          <v-select v-model="platform.platformType" label="platform type" :items="platformTypes" :item-text="(x) => x.name" :item-value="(x) => x.id" />
          <v-text-field v-model="platform.shortName" label="platform short name" />
          <v-text-field v-model="platform.longName" label="platform long name" />
          <v-textarea v-model="platform.description" label="description" />
          <v-select v-model="platform.manufacture" label="manufacture" :items="manufactures" :item-text="(x) => x.name" :item-value="(x) => x.id" />
          <v-select v-model="platform.type" label="type" :items="types" />
          <v-text-field v-model="platform.website" label="link to website" />
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          Responsible persons
        </v-card-title>
        <v-card-text>
          <div v-for="(person, index) in platform.responsiblePersons" :key="index">
            <v-select v-model="platform.responsiblePersons[index]" label="Person" :items="persons" :item-text="(x) => x.name" :item-value="(x) => x.id" />
            <v-btn @click="removePerson(index)">
              Delete
            </v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="addEmptyPerson()">+</v-btn>
        </v-card-actions>
      </v-card>
      <v-card>
        <v-card-actions>
          <v-btn @click="goBack()">
            Cancel
          </v-btn>
          <v-btn @click="save()">Save</v-btn>
          <v-btn>Save and create copy</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </div>
</template>

<script>
import masterdataservice from '../../../services/masterdataservice'
import personservice from '../../../services/personservice'
import deviceservice from '../../../services/deviceservice'

export default {
  data () {
    return {
      platformTypes: [],
      manufactures: [],
      types: ['Type 01'],
      persons: [],

      platform: {
        id: null,
        platformType: null,
        shortName: null,
        longName: null,
        description: null,
        manfature: null,
        type: null,
        website: null,
        responsiblePersons: []
      }
    }
  },
  mounted () {
    masterdataservice.findAllManufactures().then((foundManufactures) => {
      this.manufactures = foundManufactures
    })
    masterdataservice.findAllPlatformTypes().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    })
    personservice.findAllPersons().then((foundPersons) => {
      this.persons = foundPersons
    })

    const platformId = this.$route.params.id
    if (platformId) {
      deviceservice.findPlatformById(platformId).then((foundPlatform) => {
        this.platform = foundPlatform
      }).catch((error) => {
        console.err(error)
      })
    }
  },
  methods: {
    goBack () {
      this.$router.back()
    },
    addEmptyPerson () {
      this.$set(this.platform.responsiblePersons, this.platform.responsiblePersons.length, {})
    },
    removePerson (index) {
      this.$delete(this.platform.responsiblePersons, index)
    },
    save () {
      deviceservice.savePlatform(this.platform).then(() => {
        this.$router.push('/devices')
      })
    }
  }
}
</script>
