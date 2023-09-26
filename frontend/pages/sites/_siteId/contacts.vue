<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import { LoadSiteContactRolesAction } from '@/store/sites'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('sites', ['loadSiteContactRoles']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteContactsPage extends Vue {
  // vuex definition for typescript check
  loadSiteContactRoles!: LoadSiteContactRolesAction
  loadCvContactRoles!: LoadCvContactRolesAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadSiteContactRoles(this.siteId),
        this.loadCvContactRoles()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId (): string {
    return this.$route.params.siteId
  }

  head () {
    return {
      titleTemplate: 'Contacts - %s'
    }
  }
}
</script>
