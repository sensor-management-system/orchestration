<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-card>
      <v-container>
        <v-tabs v-model="activeTab">
          <v-tab>Search</v-tab>
          <v-tab>Extended Search</v-tab>
        </v-tabs>
        <v-tabs-items
          v-model="activeTab"
        >
          <v-tab-item :eager="true">
            <v-row>
              <v-col cols="12" md="5">
                <v-text-field
                  v-model="searchedText"
                  label="Label"
                  placeholder="Label of configuration"
                  hint="Please enter at least 3 characters"
                  @keydown.enter="basicSearch"
                />
              </v-col>
              <v-col
                cols="12"
                md="7"
                align-self="center"
              >
                <v-btn
                  color="primary"
                  small
                  @click="basicSearch"
                >
                  Search
                </v-btn>
                <v-btn
                  text
                  small
                  @click="clearBasicSearch"
                >
                  Clear
                </v-btn>
              </v-col>
            </v-row>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="searchedText"
                  label="Label"
                  placeholder="Label of configuration"
                  hint="Please enter at least 3 characters"
                  @keydown.enter="extendedSearch"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="3">
                <ManufacturerSelect v-model="selectedManufacturers" label="Select a manufacturer" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="3">
                <StatusSelect v-model="selectedStates" label="Select a status" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="3">
                <PlatformTypeSelect v-model="selectedPlatformTypes" label="Select a platform type" />
              </v-col>
            </v-row>
            <v-row v-if="$auth.loggedIn">
              <v-col cols="12" md="3">
                <v-checkbox v-model="selectOnlyOwnPlatforms" label="Only own platforms" />
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
                  @click="extendedSearch"
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
          </v-tab-item>
        </v-tabs-items>
      </v-container>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
import { mapActions, mapGetters, mapState } from 'vuex'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
@Component({
  components: { ProgressIndicator, PlatformTypeSelect, StatusSelect, ManufacturerSelect },
  computed: {
    ...mapState('vocabulary',['platformtypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('platforms',['selectedSearchManufacturers','selectedSearchStates','selectedSearchPlatformTypes','onlyOwnPlatforms','searchText']),
    ...mapGetters('platforms',['searchParams'])
  },
  methods:{
    ...mapActions('vocabulary',['loadEquipmentstatus', 'loadPlatformtypes', 'loadManufacturers']),
    ...mapActions('platforms',[
      'searchPlatformsPaginated',
      'setPageNumber',
      'setSelectedSearchManufacturers',
      'setSelectedSearchStates',
      'setSelectedSearchPlatformTypes',
      'setOnlyOwnPlatforms',
      'setSearchText'
    ])
  }
})
export default class PlatformSearch extends Vue {
  private activeTab=0
  // private selectedSearchManufacturers: Manufacturer[] = []
  // private selectedStates: Status[] = []
  // private selectedPlatformTypes: PlatformType[] = []
  // private selectOnlyOwnPlatforms: boolean = false

  // private searchText: string | null = null

  private isLoading = false

  get selectedManufacturers(){
    return this.selectedSearchManufacturers
  }
  set selectedManufacturers(newVal){
    this.setSelectedSearchManufacturers(newVal)
  }
  get selectedStates(){
    return this.selectedSearchStates
  }
  set selectedStates(newVal){
    this.setSelectedSearchStates(newVal)
  }

  get selectedPlatformTypes(){
    return this.selectedSearchPlatformTypes
  }
  set selectedPlatformTypes(newVal){
    this.setSelectedSearchPlatformTypes(newVal)
  }

  get selectOnlyOwnPlatforms(){
    return this.onlyOwnPlatforms
  }

  set selectOnlyOwnPlatforms(newVal){
    this.setOnlyOwnPlatforms(newVal)
  }

  get searchedText(){
    return this.searchText
  }
  set searchedText(newVal){
    this.setSearchText(newVal)
  }

  async created(){
    try {
      this.isLoading = true
      await this.loadEquipmentstatus()
      await this.loadPlatformtypes()
      await this.loadManufacturers()
      await this.initSearchQueryParams()
      // await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
    }
  }

  // get searchParams () {
  //   return {
  //     searchText: this.searchedText,
  //     manufacturer: this.selectedManufacturers,
  //     states: this.selectedStates,
  //     types: this.selectedPlatformTypes,
  //     onlyOwnPlatforms: this.selectOnlyOwnPlatforms && this.$auth.loggedIn
  //   }
  // }

  basicSearch(){
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectOnlyOwnPlatforms = false
    this.$emit('basic-search')
    this.runSearch()
  }
  clearBasicSearch(){
    this.searchedText = null
    this.$emit('clear-basic-search')
  }
  extendedSearch(){
    this.$emit('extended-search')
    this.runSearch()
  }
  clearExtendedSearch(){
    this.clearBasicSearch()
    this.selectedManufacturers = []
    this.selectedStates = []
    this.selectedPlatformTypes = []
    this.selectOnlyOwnPlatforms = false
    this.$emit('clear-extended-search')
  }

  async runSearch () {
    try {
      this.isLoading = true
      this.setPageNumber(1) // important for query
      this.initUrlQueryParams()
      // await this.searchPlatformsPaginated(this.searchParams(this.$auth.loggedIn))
      await this.searchPlatformsPaginated()
      // this.setPageInUrl() // todo muss das eigentlich rein?
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new PlatformSearchParamsSerializer({
      states: this.equipmentstatus,
      platformTypes: this.platformtypes,
      manufacturer: this.manufacturers
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchedText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnPlatforms) {
      this.selectOnlyOwnPlatforms = searchParamsObject.onlyOwnPlatforms
    }
    if (searchParamsObject.manufacturer) {
      this.selectedManufacturers = searchParamsObject.manufacturer
    }
    if (searchParamsObject.types) {
      this.selectedPlatformTypes = searchParamsObject.types
    }
    if (searchParamsObject.states) {
      this.selectedStates = searchParamsObject.states
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new PlatformSearchParamsSerializer()).toQueryParams(this.searchParams(this.$auth.loggedIn)),
      hash: this.$route.hash
    })
  }

}
</script>

<style scoped>

</style>
