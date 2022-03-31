<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/platforms"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
      <PlatformBasicDataForm
        ref="basicForm"
        v-model="platform"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/platforms"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Platform } from '@/models/Platform'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'

@Component({
  components: {
    PlatformBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth']
})
// @ts-ignore
export default class PlatformNewPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private platform: Platform = new Platform()
  private isLoading: boolean = false

  mounted () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  onSaveButtonClicked (): void {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    if (!this.$auth.loggedIn) {
      this.$store.commit('snackbar/setError', 'You need to be logged in to save the platform')
      return
    }
    this.isLoading = true
    this.$api.platforms.save(this.platform).then((savedPlatform) => {
      this.isLoading = false
      this.$store.commit('snackbar/setSuccess', 'Platform created')
      this.$router.push('/platforms/' + savedPlatform.id + '')
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/platforms/new',
          name: 'Basic Data'
        },
        {
          name: 'Contacts',
          disabled: true
        },
        {
          name: 'Attachments',
          disabled: true
        }
      ],
      title: 'Add Platform'
    })
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
