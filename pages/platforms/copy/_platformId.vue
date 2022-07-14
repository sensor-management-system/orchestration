<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :disabled="!canModifyEntity(platformToCopy)"
          :to="'/platforms'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            Please note: Actions will not be copied.
          </v-col>
        </v-row>
      </v-alert>

      <PlatformBasicDataForm
        ref="basicForm"
        v-model="platformToCopy"
        :persistent-identifier-placeholder="persistentIdentifierPlaceholder"
        :serial-number-placeholder="serialNumberPlaceholder"
        :inventory-number-placeholder="inventoryNumberPlaceholder"
      />
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
        class="mt-2"
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            Please note: Actions will not be copied.
          </v-col>
        </v-row>
      </v-alert>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :disabled="!canModifyEntity(platformToCopy)"
          :to="'/platforms'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanModifyEntityGetter, UserGroupsGetter } from '@/store/permissions'
import { PlatformsState, LoadPlatformAction, CopyPlatformAction } from '@/store/platforms'

import { Platform } from '@/models/Platform'

import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    PlatformBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'userGroups']),
    ...mapState('platforms', ['platform'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatform', 'copyPlatform']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])
  }
})
// @ts-ignore
export default class PlatformCopyPage extends Vue {
  private platformToCopy: Platform = new Platform()
  private isSaving = false
  private isLoading = false

  private copyContacts: boolean = true
  private copyAttachments: boolean = false

  private persistentIdentifierPlaceholder: string | null = null
  private serialNumberPlaceholder: string | null = null
  private inventoryNumberPlaceholder: string | null = null

  // vuex definition for typescript check
  platform!: PlatformsState['platform']
  loadPlatform!: LoadPlatformAction
  copyPlatform!: CopyPlatformAction
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  userGroups!: UserGroupsGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction

  created () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await this.loadPlatform({
        platformId: this.platformId,
        includeContacts: true,
        includePlatformAttachments: true
      })

      if (!this.platform || !this.canAccessEntity(this.platform)) {
        this.$router.replace('/platforms/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to copy this platform.')
        return
      }

      const platformCopy = this.getPreparedPlatformForCopy()
      if (platformCopy) {
        this.platformToCopy = platformCopy
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading platform failed')
    } finally {
      this.isLoading = false
    }
  }

  get platformId () {
    return this.$route.params.platformId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  getPreparedPlatformForCopy (): Platform | null {
    if (!this.platform) {
      return null
    }
    const platformToEdit = Platform.createFromObject(this.platform)
    // Unset the fields that are very device specific
    // (we need other PIDs, serial numbers and inventory numbers)
    // For the moment we just unset them completely, but there may be
    // some more logic in those numbers.
    // For example the serial numbers could just be something like 'XXXX-1'
    // and for the next device 'XXXX-2'.
    // For the inventory numbers the same.
    platformToEdit.id = null
    if (platformToEdit.persistentIdentifier) {
      this.persistentIdentifierPlaceholder = platformToEdit.persistentIdentifier
    }
    platformToEdit.persistentIdentifier = ''
    if (platformToEdit.serialNumber) {
      this.serialNumberPlaceholder = platformToEdit.serialNumber
    }
    platformToEdit.serialNumber = ''
    if (platformToEdit.inventoryNumber) {
      this.inventoryNumberPlaceholder = platformToEdit.inventoryNumber
    }
    platformToEdit.inventoryNumber = ''
    platformToEdit.permissionGroups = this.userGroups.filter(userGroup => this.platform?.permissionGroups.filter(group => userGroup.equals(group)).length)
    return platformToEdit
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.isSaving = true
      const savedPLatformId = await this.copyPlatform({
        platform: this.platformToCopy,
        copyContacts: this.copyContacts,
        copyAttachments: this.copyAttachments,
        originalPlatformId: this.platformId
      })
      this.$store.commit('snackbar/setSuccess', 'Platform copied')
      this.$router.push('/platforms/' + savedPLatformId)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Copy failed')
    } finally {
      this.isSaving = false
    }
  }

  initializeAppBar () {
    this.setTabs([
      {
        to: '/platform/copy/' + this.platformId,
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      }
    ])
    this.setTitle('Copy Platform')
  }

  @Watch('platform', { immediate: true, deep: true })
  onDeviceChanged (val: PlatformsState['platform']) {
    if (val && val.id) {
      this.setTitle('Copy ' + val.shortName)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
