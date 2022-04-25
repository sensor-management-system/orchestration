<template>
  <v-row justify="center">
    <v-col cols="4">
      <v-card>
        <v-tabs v-model="tabs">
          <v-tab>Simple</v-tab>
          <v-tab>Extended</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tabs">
          <v-container>
            <PlatformsBasicSearch
              v-model="searchText"
              @search="emitBasicSearch"
            />
          </v-container>
          <v-tab-item>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <PlatformsBasicSearchField
                    v-model="searchText"
                    @start-search="emitExtendedSearch"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <StatusSelect v-model="selectedSearchStates" label="Select a status" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <PlatformTypeSelect v-model="selectedSearchPlatformTypes" label="Select a platform type" />
                </v-col>
              </v-row>
              <v-row v-if="$auth.loggedIn">
                <v-col cols="12">
                  <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  align-self="center"
                >
                  <v-btn
                    color="primary"
                    small
                    @click="emitExtendedSearch"
                  >
                    Search
                  </v-btn>
                  <v-btn
                    text
                    small
                    @click="clearExtendedSearch"
                  >
                    Clear
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import PlatformsBasicSearch from '@/components/platforms/PlatformsBasicSearch.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'
import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
@Component({
  components: { PlatformsBasicSearchField, PlatformTypeSelect, StatusSelect, ManufacturerSelect, PlatformsBasicSearch }
})
export default class PlatformSearch extends Vue {

  private searchText: string | null = null
  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []
  private onlyOwnPlatforms: boolean = false

  private tabs=0;

  get searchParams(){
    return {
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchPlatformTypes,
      onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
    }
  }

  clearBasicSearch () {
    this.searchText = null
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
  }

  emitBasicSearch(){
    this.selectedSearchManufacturers=[]
    this.selectedSearchStates=[]
    this.selectedSearchPlatformTypes=[]
    this.onlyOwnPlatforms=false

    this.initUrlQueryParams()
    this.$emit("basic-search",this.searchParams)
  }
  emitExtendedSearch(){
    this.initUrlQueryParams()
    this.$emit("extended-search",this.searchParams)
  }

  initUrlQueryParams (): void { // todo scheint aktuell nicht zu funktionieren, noch keine Ahnung warum. Er pushed nicht zur route
    this.$router.push({
      query: (new PlatformSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }
}
</script>

<style scoped>

</style>
