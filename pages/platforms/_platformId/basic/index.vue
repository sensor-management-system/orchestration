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
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionCopy
            :path="'/platforms/copy/' + platformId"
          />
          <DotMenuActionDelete
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <PlatformBasicData
      v-if="platform"
      v-model="platform"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionCopy
            :path="'/platforms/copy/' + platformId"
          />
          <DotMenuActionDelete
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <PlatformDeleteDialog
      v-if="platform"
      v-model="showDeleteDialog"
      :platform-to-delete="platform"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import PlatformBasicData from '@/components/PlatformBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import PlatformDeleteDialog from '@/components/platforms/PlatformDeleteDialog.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Platform } from '@/models/Platform'

@Component({
  components: {
    ProgressIndicator,
    PlatformDeleteDialog,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenu,
    PlatformBasicData
  },
  computed: mapState('platforms', ['platform']),
  methods: mapActions('platforms', ['deletePlatform'])
})
export default class PlatformShowBasicPage extends Vue {
  private isSaving = false

  private showDeleteDialog: boolean = false

  // vuex definition for typescript check
  platform!:Platform
  deletePlatform!:(id: string)=>void

  get platformId () {
    return this.$route.params.platformId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.platform === null || this.platform.id ===null) {
      return
    }

    try {
      this.isSaving = true
      await this.deletePlatform(this.platform.id)
      this.$router.push('/platforms')
      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
