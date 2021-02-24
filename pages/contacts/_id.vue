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
    <v-card outlined>
      <v-form ref="basicForm">
        <v-card flat>
          <v-card-title>
            {{ title }}
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="contact.givenName"
                  label="Given name"
                  :readonly="readonly"
                  :disabled="readonly"
                />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="contact.familyName"
                  label="Family name"
                  :readonly="readonly"
                  :disabled="readonly"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="9">
                <v-text-field
                  v-model="contact.email"
                  label="E-mail"
                  type="email"
                  :readonly="readonly"
                  :disabled="readonly"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="9">
                <v-text-field
                  v-if="readonly"
                  v-model="contact.website"
                  label="Website"
                  placeholder="https://"
                  type="url"
                  :readonly="true"
                  :disabled="true"
                >
                  <template slot="append">
                    <a v-if="contact.website.length > 0" :href="contact.website" target="_blank">
                      <v-icon>
                        mdi-open-in-new
                      </v-icon>
                    </a>
                  </template>
                </v-text-field>
                <v-text-field
                  v-else
                  v-model="contact.website"
                  label="Website"
                  placeholder="https://"
                  type="url"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-form>
      <v-btn
        v-if="!editMode && isLoggedIn"
        fab
        fixed
        bottom
        right
        color="secondary"
        @click="onEditButtonClick"
      >
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </v-card>
  </div>
</template>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, Watch, Vue } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

@Component
export default class ContactIdPage extends Vue {
  private contact: Contact = Contact.createEmpty()
  private contactBackup: Contact | null = null

  private editMode: boolean = false

  created () {
    this.initializeAppBar()
    this.registerButtonActions()
  }

  mounted () {
    this.loadContact().then((contact) => {
      if (contact === null) {
        this.$store.commit('appbar/setTitle', 'Add Contact')
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading contact failed')
    })
  }

  beforeDestroy () {
    this.unregisterButtonActions()
    this.$store.dispatch('appbar/setDefaults')
  }

  registerButtonActions () {
    this.$nuxt.$on('AppBarEditModeContent:save-btn-click', () => {
      this.save().then(() => {
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      }).catch(() => {
        this.$store.commit('snackbar/setError', 'Save failed')
      })
    })
    this.$nuxt.$on('AppBarEditModeContent:cancel-btn-click', () => {
      this.cancel()
    })
  }

  unregisterButtonActions () {
    this.$nuxt.$off('AppBarEditModeContent:save-btn-click')
    this.$nuxt.$off('AppBarEditModeContent:cancel-btn-click')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [],
      title: 'Contacts',
      saveBtnHidden: true,
      cancelBtnHidden: true
    })
  }

  loadContact (): Promise<Contact|null> {
    return new Promise((resolve, reject) => {
      const contactId = this.$route.params.id
      if (!contactId) {
        this.createBackup()
        this.editMode = true && this.isLoggedIn
        resolve(null)
        return
      }
      this.editMode = false
      this.$api.contacts.findById(contactId).then((foundContact) => {
        this.contact = foundContact
        resolve(foundContact)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  createBackup () {
    this.contactBackup = Contact.createFromObject(this.contact)
  }

  restoreBackup () {
    if (!this.contactBackup) {
      return
    }
    this.contact = this.contactBackup
    this.contactBackup = null
  }

  save (): Promise<Contact|null> {
    return new Promise((resolve, reject) => {
      this.$api.contacts.save(this.contact).then((savedContact) => {
        this.contact = savedContact
        this.contactBackup = null
        this.editMode = false
        if (!this.$route.params.id && savedContact.id) {
          this.setUrlWithNewId(savedContact.id)
          // and we set the parameter so that we don't and up with
          // multiple ids in the url
          this.$route.params.id = savedContact.id
        }
        resolve(savedContact)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  setUrlWithNewId (id: string) {
    const oldUrl = this.$route.path
    const newUrl = oldUrl + (oldUrl.endsWith('/') ? '' : '/') + id

    history.pushState({}, '', newUrl)
  }

  cancel () {
    this.restoreBackup()
    if (this.contact.id) {
      this.editMode = false
    } else {
      this.$router.push('search/contacts')
    }
  }

  onEditButtonClick () {
    this.createBackup()
    this.editMode = true && this.isLoggedIn
  }

  get readonly () {
    return !this.editMode
  }

  @Watch('contact', { immediate: true, deep: true })
  onContactChanged (val: Contact) {
    if (val.id) {
      const fullName = this.getFullName(val)
      this.$store.commit('appbar/setTitle', fullName || 'Add contact')
    }
  }

  @Watch('editMode', { immediate: true, deep: true })
  onEditModeChange (editMode: boolean) {
    this.$store.commit('appbar/setSaveBtnHidden', !editMode)
    this.$store.commit('appbar/setCancelBtnHidden', !editMode)
  }

  getFullName (contact: Contact) : string {
    return contact.givenName + ' ' + contact.familyName
  }

  get title () : string {
    const fullName = this.getFullName(this.contact).trim()
    if (fullName) {
      return 'Contact: ' + fullName
    }
    return 'Contact'
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
