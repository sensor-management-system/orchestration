<!--
SPDX-FileCopyrightText: 2020 - 2023
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
        :to="'/platforms/' + platformId + '/basic/edit'"
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
            :path="'/platforms/copy/' + platformId"
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
    <PlatformBasicData
      v-if="platform"
      v-model="platform"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
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
            :path="'/platforms/copy/' + platformId"
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
    <DeleteDialog
      v-if="platform"
      v-model="showDeleteDialog"
      title="Delete Platform"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the platform <em>{{ platform.shortName }}</em>?
    </DeleteDialog>
    <PlatformArchiveDialog
      v-if="platform"
      v-model="showArchiveDialog"
      :platform-to-archive="platform"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="platformSensorMLFilename"
      :url="platformSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { PlatformsState, DeletePlatformAction, ArchivePlatformAction, LoadPlatformAction, RestorePlatformAction, ExportAsSensorMLAction, GetSensorMLUrlAction } from '@/store/platforms'

import PlatformBasicData from '@/components/PlatformBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import PlatformArchiveDialog from '@/components/platforms/PlatformArchiveDialog.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { Visibility } from '@/models/Visibility'

@Component({
  components: {
    DeleteDialog,
    DotMenuActionDelete,
    DotMenuActionSensorML,
    DotMenuActionCopy,
    DotMenu,
    DownloadDialog,
    PlatformBasicData,
    DotMenuActionArchive,
    DotMenuActionRestore,
    PlatformArchiveDialog
  },
  computed: {
    ...mapState('platforms', ['platform']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['deletePlatform', 'loadPlatform', 'archivePlatform', 'restorePlatform', 'exportAsSensorML', 'getSensorMLUrl']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformShowBasicPage extends Vue {
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
  platform!: PlatformsState['platform']
  loadPlatform!: LoadPlatformAction
  deletePlatform!: DeletePlatformAction
  archivePlatform!: ArchivePlatformAction
  restorePlatform!: RestorePlatformAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  get platformId () {
    return this.$route.params.platformId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  openSensorMLDialog () {
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
  }

  get platformSensorMLFilename (): string {
    if (this.platform != null) {
      return `${this.platform.shortName}.xml`
    }
    return 'platform.xml'
  }

  async platformSensorMLUrl (): Promise<string | null> {
    if (!this.platform) {
      return null
    }
    if (this.platform?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.platform.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.platform!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Platform could not be exported as SensorML')
        return null
      }
    }
  }

  async deleteAndCloseDialog () {
    if (this.platform === null || this.platform.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deletePlatform(this.platform.id)
      this.$router.push('/platforms')
      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    } finally {
      this.setLoading(false)
      this.showDeleteDialog = false
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
    if (this.platform === null || this.platform.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archivePlatform(this.platform.id)
      await this.loadPlatform({
        platformId: this.platformId,
        includeContacts: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.$store.commit('snackbar/setSuccess', 'Platform archived')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Platform could not be archived')
    } finally {
      this.setLoading(false)
      this.showArchiveDialog = false
    }
  }

  async runRestore () {
    if (this.platform === null || this.platform.id === null) {
      return
    }
    this.setLoading(true)
    try {
      await this.restorePlatform(this.platform.id)
      await this.loadPlatform({
        platformId: this.platformId,
        includeContacts: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.$store.commit('snackbar/setSuccess', 'Platform restored')
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Platform could not be restored')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
