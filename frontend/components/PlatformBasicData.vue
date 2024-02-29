<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
vuex
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
    <v-row align="center">
      <v-col>
        <v-row>
          <v-col cols="12">
            <label>Visibility / Permissions</label>
            <visibility-chip
              v-model="value.visibility"
            />
            <permission-group-chips
              v-model="value.permissionGroups"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" :md="platformImagesShouldBeRendered ? 12 : 6">
            <label>URN</label>
            {{ platformURN }}
          </v-col>
          <v-col cols="12" :md="platformImagesShouldBeRendered ? 12 : 6">
            <label>Persistent identifier (PID)</label>
            <pid-tooltip
              :value="value.persistentIdentifier"
              show-button
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" :md="platformImagesShouldBeRendered ? 12 : 6">
            <label>Short name</label>
            {{ value.shortName | orDefault }}
          </v-col>
          <v-col cols="12" :md="platformImagesShouldBeRendered ? 12 : 6">
            <label>Long name</label>
            {{ value.longName | orDefault }}
          </v-col>
        </v-row>
      </v-col>
      <v-col v-if="platformImagesShouldBeRendered" cols="12" md="6">
        <AttachmentImagesCarousel
          :value="value.images"
          :download-attachment="downloadAttachment"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Platform type</label>
        {{ platformTypeName | orDefault }}
        <v-tooltip v-if="platformTypeDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ platformTypeDefinition }}</span>
        </v-tooltip>
      </v-col>
      <v-col cols="12" md="3">
        <label>Manufacturer</label>
        {{ platformManufacturerName | orDefault }}
        <v-tooltip v-if="platformManufacturerDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ platformManufacturerDefinition }}</span>
        </v-tooltip>
      </v-col>
      <v-col cols="12" md="3">
        <label>Model</label>
        {{ value.model | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Country of origin</label>
        {{ value.country | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Status</label>
        {{ platformStatusName | orDefault }}
        <v-tooltip v-if="platformStatusDefinition" right>
          <template #activator="{ on, attrs }">
            <v-icon
              color="primary"
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>{{ platformStatusDefinition }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row>
      <v-col cols="12" md="9">
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Website</label>
        {{ value.website | orDefault }}
        <a v-if="value.website.length > 0" :href="value.website" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row>
      <v-col cols="12" md="3">
        <label>Serial number</label>
        {{ value.serialNumber | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Inventory number</label>
        {{ value.inventoryNumber | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="value.keywords">
      <v-col>
        <label>Keywords</label>
        <v-chip-group v-if="value.keywords.length">
          <v-chip v-for="keyword, idx in value.keywords" :key="idx" small>
            {{ keyword }}
          </v-chip>
        </v-chip-group>
        <span v-else>
          {{ '' | orDefault }}
        </span>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import {
  VocabularyState,
  GetEquipmentstatusByUriGetter,
  GetPlatformTypeByUriGetter,
  GetManufacturerByUriGetter,
  LoadManufacturersAction,
  LoadPlatformtypesAction,
  LoadEquipmentstatusAction
} from '@/store/vocabulary'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

import { DownloadAttachmentAction } from '@/store/platforms'
import { createPlatformUrn } from '@/modelUtils/urnBuilders'

import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import AttachmentImagesCarousel from '@/components/shared/AttachmentImagesCarousel.vue'
import QrCodeDialog from '@/components/QrCodeDialog.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'

@Component({
  components: {
    PermissionGroupChips,
    PidTooltip,
    QrCodeDialog,
    VisibilityChip,
    AttachmentImagesCarousel
  },
  computed: {
    ...mapState('vocabulary', ['platformtypes']),
    ...mapGetters('vocabulary', ['getEquipmentstatusByUri', 'getPlatformTypeByUri', 'getManufacturerByUri'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadManufacturers', 'loadPlatformtypes', 'loadEquipmentstatus']),
    ...mapActions('platforms', ['downloadAttachment'])
  }
})
export default class PlatformBasicData extends Vue {
  public readonly NO_TYPE: string = 'Unknown type'

  @Prop({
    default: () => new Platform(),
    required: true,
    type: Platform
  })
  readonly value!: Platform

  // vuex definition for typescript check
  loadEquipmentstatus!: LoadEquipmentstatusAction
  loadPlatformtypes!: LoadPlatformtypesAction
  loadManufacturers!: LoadManufacturersAction
  getManufacturerByUri!: GetManufacturerByUriGetter
  getPlatformTypeByUri!: GetPlatformTypeByUriGetter
  getEquipmentstatusByUri!: GetEquipmentstatusByUriGetter
  platformtypes!: VocabularyState['platformtypes']
  downloadAttachment!: DownloadAttachmentAction

  async mounted () {
    try {
      await this.loadEquipmentstatus()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of states failed')
    }
    try {
      await this.loadPlatformtypes()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platform types failed')
    }
    try {
      await this.loadManufacturers()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    }
  }

  get platformManufacturerName (): string {
    if (this.value.manufacturerName) {
      return this.value.manufacturerName
    }
    if (this.getManufacturerByUri(this.value.manufacturerUri)) {
      const manufacturer: Manufacturer|undefined = this.getManufacturerByUri(this.value.manufacturerUri)
      return manufacturer!.name
    }
    return ''
  }

  get platformManufacturerDefinition (): string {
    if (this.getManufacturerByUri(this.value.manufacturerUri)) {
      const manufacturer: Manufacturer|undefined = this.getManufacturerByUri(this.value.manufacturerUri)
      return manufacturer!.definition
    }
    return ''
  }

  get platformTypeName (): string {
    if (this.value.platformTypeName) {
      return this.value.platformTypeName
    }

    if (this.getPlatformTypeByUri(this.value.platformTypeUri)) {
      const platformType: PlatformType|undefined = this.getPlatformTypeByUri(this.value.platformTypeUri)
      return platformType!.name
    }
    return this.NO_TYPE
  }

  get platformTypeDefinition (): string {
    if (this.getPlatformTypeByUri(this.value.platformTypeUri)) {
      const platformType: PlatformType|undefined = this.getPlatformTypeByUri(this.value.platformTypeUri)
      return platformType!.definition
    }
    return ''
  }

  get platformStatusName (): string {
    if (this.value.statusName) {
      return this.value.statusName
    }
    if (this.getEquipmentstatusByUri(this.value.statusUri)) {
      const platformStatus: Status|undefined = this.getEquipmentstatusByUri(this.value.statusUri)
      return platformStatus!.name
    }
    return ''
  }

  get platformStatusDefinition (): string {
    if (this.getEquipmentstatusByUri(this.value.statusUri)) {
      const platformStatus: Status|undefined = this.getEquipmentstatusByUri(this.value.statusUri)
      return platformStatus!.definition
    }
    return ''
  }

  get platformURN () {
    return createPlatformUrn(this.value, this.platformtypes)
  }

  get platformImagesShouldBeRendered () {
    return this.value.images.length > 0
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
