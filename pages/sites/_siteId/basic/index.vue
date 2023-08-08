<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/sites/' + siteId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu>
        <template #actions>
          <DotMenuActionSensorML
            @click="openSensorMLDialog"
          />
          <DotMenuActionCopy
            v-if="$auth.loggedIn"
            :path="'/sites/copy/' + siteId"
          />
          <DotMenuActionArchive
            :readonly="!archivable"
            @click="initArchiveDialog"
          />
          <DotMenuActionRestore
            :readonly="!restoreable"
            @click="runRestore"
          />
          <DotMenuActionDelete
            v-if="$auth.loggedIn"
            :readonly="!deletable"
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <SiteBasicData
      v-if="site"
      v-model="site"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/sites/' + siteId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu>
        <template #actions>
          <DotMenuActionSensorML
            @click="openSensorMLDialog"
          />
          <DotMenuActionCopy
            v-if="$auth.loggedIn"
            :path="'/sites/copy/' + siteId"
          />
          <DotMenuActionArchive
            :readonly="!archivable"
            @click="initArchiveDialog"
          />
          <DotMenuActionRestore
            :readonly="!restoreable"
            @click="runRestore"
          />
          <DotMenuActionDelete
            v-if="$auth.loggedIn"
            :readonly="!deletable"
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <SiteDeleteDialog
      v-if="site"
      v-model="showDeleteDialog"
      :site-to-delete="site"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <SiteArchiveDialog
      v-if="site"
      v-model="showArchiveDialog"
      :site-to-archive="site"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="siteSensorMLFilename"
      :url="siteSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import SiteDeleteDialog from '@/components/sites/SiteDeleteDialog.vue'
import SiteArchiveDialog from '@/components/sites/SiteArchiveDialog.vue'
import SiteBasicData from '@/components/sites/SiteBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import { ArchiveSiteAction, DeleteSiteAction, ExportAsSensorMLAction, GetSensorMLUrlAction, LoadSiteAction, RestoreSiteAction, SitesState } from '@/store/sites'
import { Visibility } from '@/models/Visibility'

@Component({
  components: {
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenuActionSensorML,
    DotMenu,
    SiteBasicData,
    DotMenuActionRestore,
    DotMenuActionArchive,
    SiteDeleteDialog,
    SiteArchiveDialog,
    DownloadDialog
  },

  computed: mapState('sites', ['site']),
  methods: {
    ...mapActions('sites', [
      'loadSite',
      'deleteSite',
      'archiveSite',
      'restoreSite',
      'exportAsSensorML',
      'getSensorMLUrl'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteShowBasicPage extends Vue {
  @InjectReactive()
    editable!: boolean

  @InjectReactive()
    deletable!: boolean

  @InjectReactive()
    archivable!: boolean

  @InjectReactive()
    restoreable!: boolean

  private showDeleteDialog: boolean = false
  private showArchiveDialog: boolean = false
  private showDownloadDialog: boolean = false

  // vuex definition for typescript check
  site!: SitesState['site']
  loadSite!: LoadSiteAction
  deleteSite!: DeleteSiteAction
  archiveSite!: ArchiveSiteAction
  restoreSite!: RestoreSiteAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction
  setLoading!: SetLoadingAction

  get siteId () {
    return this.$route.params.siteId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.site === null || this.site.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteSite(this.site.id)
      this.$store.commit('snackbar/setSuccess', 'Site / Lab deleted')
      this.$router.push('/sites')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Site / Lab could not be deleted')
    } finally {
      this.setLoading(false)
    }
  }

  initArchiveDialog () {
    this.showArchiveDialog = true
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
  }

  async archiveAndCloseDialog () {
    this.showArchiveDialog = false
    if (this.site === null || this.site.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archiveSite(this.site.id)
      await this.loadSite({
        siteId: this.siteId
      })
      this.$store.commit('snackbar/setSuccess', 'Site / Lab archived')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Site / Lab could not be archived')
    } finally {
      this.setLoading(false)
      this.showArchiveDialog = false
    }
  }

  async runRestore () {
    if (this.site === null || this.site.id === null) {
      return
    }
    this.setLoading(true)
    try {
      await this.restoreSite(this.site.id)
      await this.loadSite({
        siteId: this.siteId
      })
      this.$store.commit('snackbar/setSuccess', 'Site / Lab restored')
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Site / Lab could not be restored')
    } finally {
      this.setLoading(false)
    }
  }

  openSensorMLDialog () {
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
  }

  get siteSensorMLFilename (): string {
    if (this.site != null) {
      return `${this.site.label}.xml`
    }
    return 'site.xml'
  }

  async siteSensorMLUrl (): Promise<string | null> {
    if (!this.site) {
      return null
    }
    if (this.site?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.site.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.site!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Site could not be exported as SensorML')
        return null
      }
    }
  }
}
</script>
