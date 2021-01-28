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
        <v-text-field v-model="searchText" label="Name" placeholder="Name of contact" @keydown.enter="search" />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn
          color="primary"
          @click="search"
        >
          Search
        </v-btn>
        <v-btn
          text
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
    </v-row>
    <div v-if="loading">
      <div class="text-center pt-2">
        <v-progress-circular indeterminate />
      </div>
    </div>
    <div v-if="searchResults.length == 0 && !loading">
      <v-card>
        <v-card-text>
          <p class="text-center">
            There are no contacts that match your search criteria.
          </p>
        </v-card-text>
      </v-card>
    </div>
    <div v-if="searchResults.length && !loading">
      <v-subheader>
        <template v-if="totalCount == 1">
          1 contact found
        </template>
        <template v-else>
          {{ totalCount }} contacts found
        </template>
        <!-- No export to pdf due to data privacy reasons -->
      </v-subheader>
      <v-hover
        v-for="result in searchResults"
        v-slot:default="{ hover }"
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
                <v-menu
                  close-on-click
                  close-on-content-click
                  offset-x
                  left
                  z-index="999"
                >
                  <template v-slot:activator="{ on }">
                    <v-btn
                      data-role="property-menu"
                      icon
                      small
                      v-on="on"
                    >
                      <v-icon
                        dense
                        small
                      >
                        mdi-dots-vertical
                      </v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      dense
                      @click="showDeleteDialogFor(result.id)"
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          class="red--text"
                        >
                          <v-icon
                            left
                            small
                            color="red"
                          >
                            mdi-delete
                          </v-icon>
                          Delete
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-menu>
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
          <v-dialog v-model="showDeleteDialog[result.id]" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete contact
              </v-card-title>
              <v-card-text>
                Do you really want to delete the contact <em>{{ getFullName(result) }}</em>?
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="hideDeleteDialogFor(result.id)"
                >
                  No
                </v-btn>
                <v-spacer />
                <v-btn
                  color="error"
                  text
                  @click="deleteAndCloseDialog(result.id)"
                >
                  <v-icon left>
                    mdi-delete
                  </v-icon>
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-hover>
    </div>
    <v-btn
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/contacts"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Contact } from '@/models/Contact'

@Component({
})
export default class SearchContactsPage extends Vue {
  private readonly pageSize: number = 20
  private loading: boolean = true

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Contact> = null

  private searchResults: Contact[] = []
  private searchText: string = ''

  private showDeleteDialog: { [id: string]: boolean} = {}
  private searchResultItemsShown: { [id: string]: boolean } = {}

  created () {
    this.initializeAppBar()
  }

  mounted () {
    this.search()
    window.onscroll = () => {
      // from https://www.digitalocean.com/community/tutorials/vuejs-implementing-infinite-scroll
      const isOnBottom = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight

      if (isOnBottom && this.canLoadNext()) {
        this.loadNext()
      }
    }
  }

  beforeDestroy () {
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
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

  search () {
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
    const lastActiveSearcher = this.$api.contacts
      .newSearchBuilder()
      .withText(this.searchText)
      .build()
    lastActiveSearcher
      .findMatchingAsPaginationLoader(this.pageSize)
      .then(this.loadUntilWeHaveSomeEntries).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of contacts failed')
      })
  }

  loadUntilWeHaveSomeEntries (loader: IPaginationLoader<Contact>) {
    this.loader = loader
    this.loading = false
    this.searchResults = [...this.searchResults, ...loader.elements]
    this.totalCount = loader.totalCount

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader)
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of contacts failed')
      })
    }
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
        this.totalCount = nextLoader.totalCount
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional contacts failed')
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  deleteAndCloseDialog (id: string) {
    this.$api.contacts.deleteById(id).then(() => {
      this.showDeleteDialog = {}

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
        this.totalCount -= 1
      }

      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    }).catch((_error) => {
      this.showDeleteDialog = {}
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    })
  }

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
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
}
</script>
