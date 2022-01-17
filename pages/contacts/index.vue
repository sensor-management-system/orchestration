<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" md="5">
        <v-text-field v-model="searchText" label="Name" placeholder="Name of contact" @keydown.enter="runSearch" />
      </v-col>
      <v-col
        cols="12"
        md="7"
        align-self="center"
      >
        <v-btn
          color="primary"
          small
          @click="runSearch"
        >
          Search
        </v-btn>
        <v-btn
          text
          small
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>

    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="!totalCount && !loading">
      <p class="text-center">
        There are no contacts that match your search criteria.
      </p>
    </div>

    <div v-if="totalCount">
      <v-subheader>
        <template v-if="totalCount == 1">
          1 contact found
        </template>
        <template v-else>
          {{ totalCount }} contacts found
        </template>
        <!-- No export to pdf due to data privacy reasons -->
      </v-subheader>

      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
      />
      <v-hover
        v-for="result in getSearchResultForPage(page)"
        v-slot="{ hover }"
        :key="result.id"
      >
        <v-card
          :disabled="loading"
          :elevation="hover ? 6 : 2"
          class="ma-2"
        >
          <v-card-text
            @click.stop.prevent="showResultItem(result.id)"
          >
            <v-row
              no.gutters
            >
              <v-col>
                <div class="'text-caption text-disabled">
                  {{ result.email }}
                </div>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <DotMenu>
                  <template #actions>
                    <DotMenuActionDelete
                      :readonly="!$auth.loggedIn"
                      @click="initDeleteDialog(result)"
                    />
                  </template>
                </DotMenu>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                {{ getFullName(result) }}
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <v-btn
                  :to="'/contacts/' + result.id"
                  color="primary"
                  text
                  @click.stop.prevent
                >
                  View
                </v-btn>
                <v-btn
                  icon
                  @click.stop.prevent="showResultItem(result.id)"
                >
                  <v-icon>{{ isResultItemShown(result.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
          <v-expand-transition>
            <v-card
              v-show="isResultItemShown(result.id)"
              flat
              tile
              color="grey lighten-5"
            >
              <v-card-text>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Given name:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ result.givenName }}
                  </v-col>
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Family name:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ result.familyName }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Website:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ result.website }}
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-expand-transition>
        </v-card>
      </v-hover>
      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
      />
    </div>
    <ContacsDeleteDialog
      v-model="showDeleteDialog"
      :contact-to-delete="contactToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <v-btn
      v-if="$auth.loggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/contacts/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Contact } from '@/models/Contact'

import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IContactSearchParams, ContactSearchParamsSerializer } from '@/modelUtils/ContactSearchParams'

type PaginatedResult = {
  [page: number]: Contact[]
}

@Component({
  components: {
    ContacsDeleteDialog,
    DotMenuActionDelete,
    DotMenu
  }
})
export default class SearchContactsPage extends Vue {
  private readonly pageSize: number = 20
  private page: number = 0
  private loading: boolean = true

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Contact> = null

  private searchResults: PaginatedResult = {}
  private searchText: string = ''

  private showDeleteDialog: boolean = false
  private contactToDelete: Contact | null = null
  private searchResultItemsShown: { [id: string]: boolean } = {}

  created () {
    this.initializeAppBar()
  }

  mounted () {
    this.initSearchQueryParams(this.$route.query)
    this.runInitialSearch()
  }

  beforeDestroy () {
    this.unsetResultItemsShown()
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [],
      title: 'Contacts',
      saveBtnHiden: true,
      cancelBtnHidden: true
    })
  }

  clearSearch () {
    this.searchText = ''
  }

  async runInitialSearch (): Promise<void> {
    const page: number | undefined = this.getPageFromUrl()

    await this.search(
      {
        searchText: this.searchText
      },
      page
    )
  }

  runSearch () {
    this.search({
      searchText: this.searchText
    })
  }

  async search (
    searchParameters: IContactSearchParams,
    page: number = 1
  ): Promise<void> {
    this.initUrlQueryParams(searchParameters)

    this.totalCount = 0
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.loader = null
    this.page = 0

    const lastActiveSearcher = this.$api.contacts
      .newSearchBuilder()
      .withText(this.searchText)
      .build()

    try {
      const loader = await lastActiveSearcher.findMatchingAsPaginationLoaderOnPage(page, this.pageSize)
      this.loader = loader
      this.searchResults[page] = loader.elements
      this.totalCount = loader.totalCount
      this.page = page
      this.setPageInUrl(page)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of contacts failed')
    } finally {
      this.loading = false
    }
  }

  async loadPage (pageNr: number, useCache: boolean = true) {
    // use the results that were already loaded if available
    if (useCache && this.searchResults[pageNr]) {
      return
    }
    if (this.loader != null && this.loader.funToLoadPage != null) {
      try {
        this.loading = true
        const loader = await this.loader.funToLoadPage(pageNr)
        this.loader = loader
        this.searchResults[pageNr] = loader.elements
        this.totalCount = loader.totalCount
      } catch (_error) {
        this.$store.commit('snackbar/setError', 'Loading of contacts failed')
      } finally {
        this.loading = false
      }
    }
  }

  get numberOfPages (): number {
    return Math.ceil(this.totalCount / this.pageSize)
  }

  async setPage (page: number) {
    await this.loadPage(page)
    this.page = page
    this.setPageInUrl(page, false)
  }

  getSearchResultForPage (pageNr: number): Contact[] | undefined {
    return this.searchResults[pageNr]
  }

  getAllResults (): Contact[] {
    let result: Contact[] = []
    Object.entries(this.searchResults).map(i => i[1]).forEach((i: Contact[]) => {
      result = [...result, ...i]
    })
    return result
  }

  initDeleteDialog (contact: Contact) {
    this.showDeleteDialog = true
    this.contactToDelete = contact
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.contactToDelete = null
  }

  deleteAndCloseDialog (id: string) {
    this.showDeleteDialog = false
    if (this.contactToDelete === null) {
      return
    }

    this.$api.contacts.deleteById(id).then(() => {
      // if we know that the deleted device was the last of the page, we
      // decrement the page by one
      if (this.getSearchResultForPage(this.page)?.length === 1) {
        this.page = this.page > 1 ? this.page - 1 : 1
      }
      this.loadPage(this.page, false)
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    }).finally(() => {
      this.contactToDelete = null
    })
  }

  showResultItem (id: string) {
    const show = !!this.searchResultItemsShown[id]
    Vue.set(this.searchResultItemsShown, id, !show)
  }

  isResultItemShown (id: string): boolean {
    return this.searchResultItemsShown[id]
  }

  unsetResultItemsShown (): void {
    this.searchResultItemsShown = {}
  }

  getFullName (contact: Contact) : string {
    return contact.givenName + ' ' + contact.familyName
  }

  initSearchQueryParams (params: QueryParams): void {
    const searchParamsObject = new ContactSearchParamsSerializer().toSearchParams(params)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
  }

  initUrlQueryParams (params: IContactSearchParams): void {
    this.$router.push({
      query: (new ContactSearchParamsSerializer()).toQueryParams(params),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 0
    }
  }

  setPageInUrl (page: number, preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(page)
      }
    } else {
      // remove page from the current url params
      const {
        // eslint-disable-next-line
        page,
        ...params
      } = this.$route.query
      query = params
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
.progress-spinner {
  position: absolute;
  top: 40vh;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 32px;
  z-index: 99;
}
</style>
