<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <DotMenu>
          <template #actions>
            <DotMenuActionSensorML
              @click="openSensorMLDialog"
            />
            <DotMenuActionDelete
              v-if="$auth.loggedIn"
              :readonly="!deletable"
              @click="initDeleteDialog"
            />
            <DotMenuActionArchive
              :readonly="!archivable"
              @click="initArchiveDialog"
            />
            <DotMenuActionRestore
              :readonly="!restoreable"
              @click="runRestore"
            />
          </template>
        </DotMenu>
      </v-card-actions>

      <ConfigurationsBasicData
        v-if="configuration"
        v-model="configuration"
        :readonly="true"
      />

      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <DotMenu>
          <template #actions>
            <DotMenuActionSensorML
              @click="openSensorMLDialog"
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
        v-model="showDeleteDialog"
        title="Delete Configuration"
        :disabled="isLoading"
        @cancel="closeDialog"
        @delete="deleteAndCloseDialog"
      >
        Do you really want to delete the configuration <em>{{ configuration.label }}</em>?
      </DeleteDialog>
      <ConfigurationArchiveDialog
        v-if="configuration"
        v-model="showArchiveDialog"
        :configuration-to-archive="configuration"
        @cancel-archiving="closeArchiveDialog"
        @submit-archiving="archiveAndCloseDialog"
      />
      <download-dialog
        v-model="showDownloadDialog"
        :filename="configurationSensorMLFilename"
        :url="configurationSensorMLUrl"
        @cancel="closeDownloadDialog"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import ConfigurationsBasicData from '@/components/configurations/ConfigurationsBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ConfigurationArchiveDialog from '@/components/configurations/ConfigurationArchiveDialog.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import { IConfiguration } from '@/models/Configuration'
import { Visibility } from '@/models/Visibility'
import { ArchiveConfigurationAction, LoadConfigurationAction, RestoreConfigurationAction, ExportAsSensorMLAction, GetSensorMLUrlAction } from '@/store/configurations'

@Component({
  components: {
    DeleteDialog,
    DotMenuActionDelete,
    DotMenuActionSensorML,
    DotMenu,
    ConfigurationsBasicData,
    ConfigurationArchiveDialog,
    DotMenuActionArchive,
    DotMenuActionRestore,
    DownloadDialog
  },
  computed: {
    ...mapState('configurations', ['configuration']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', [
      'deleteConfiguration',
      'loadConfiguration',
      'archiveConfiguration',
      'restoreConfiguration',
      'exportAsSensorML',
      'getSensorMLUrl'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationShowBasicPage extends Vue {
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
  configuration!: IConfiguration
  deleteConfiguration!: (id: string) => void
  loadConfiguration!: LoadConfigurationAction
  archiveConfiguration!: ArchiveConfigurationAction
  restoreConfiguration!: RestoreConfigurationAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction
  setLoading!: SetLoadingAction

  get configurationId () {
    return this.$route.params.configurationId
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

  get configurationSensorMLFilename (): string {
    if (this.configuration != null) {
      return `${this.configuration.label}.xml`
    }
    return 'configuration.xml'
  }

  async configurationSensorMLUrl (): Promise<string | null> {
    if (!this.configuration) {
      return null
    }
    if (this.configuration?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.configuration.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.configuration!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Configuration could not be exported as SensorML')
        return null
      }
    }
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.configuration === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteConfiguration(this.configuration.id)
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
      this.$router.push('/configurations')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
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
    if (this.configuration === null || this.configuration.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archiveConfiguration(this.configuration.id)
      await this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Configuration archived')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Configuration could not be archived')
    } finally {
      this.setLoading(false)
      this.showArchiveDialog = false
    }
  }

  async runRestore () {
    if (this.configuration === null || this.configuration.id === null) {
      return
    }
    this.setLoading(true)
    try {
      await this.restoreConfiguration(this.configuration.id)
      await this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Configuration restored')
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Configuration could not be restored')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
