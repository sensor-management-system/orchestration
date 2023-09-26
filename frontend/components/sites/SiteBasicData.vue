<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
      <v-col cols="12">
        <label>Visibility / Permissions</label>
        <VisibilityChip
          v-model="value.visibility"
        />
        <PermissionGroupChips
          v-model="value.permissionGroups"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>Label</label>
        {{ value.label }}
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row>
      <v-col cols="12" md="6">
        <label>Usage</label>
        {{ value.siteUsageName }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Type</label>
        {{ value.siteTypeName }}
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
    <v-row v-if="value.geometry.length != 0">
      <v-col cols="12">
        <SiteMap :value="value.geometry" :readonly="true" />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <label>This site / lab does not have location data.</label>
        <v-subheader>
          Edit the site / lab to add coordinates.
        </v-subheader>
        <v-divider class="my-4" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Street</label>
        {{ value.address.street | orDefault }} {{ value.address.streetNumber }}
      </v-col>
      <v-col cols="12" md="3">
        <label>City</label>
        {{ value.address.zipCode }} {{ value.address.city | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Country</label>
        {{ value.address.country | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Building - Room</label>
        {{ value.address.building }} - {{ value.address.room }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <label>Configurations on site / lab</label>
        <div v-if="siteConfigurations.length>0">
          <BaseList
            :list-items="siteConfigurations"
          >
            <template #list-item="{item}">
              <ConfigurationsListItem
                :configuration="item"
              />
            </template>
          </BaseList>
        </div>
        <div v-else>
          <v-subheader>
            There are no configurations on this site / lab.
          </v-subheader>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import { Site } from '@/models/Site'
import SiteMap from '@/components/sites/SiteMap.vue'

import VisibilityChip from '@/components/VisibilityChip.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'

import { SitesState } from '@/store/sites'

@Component({
  components: {
    VisibilityChip,
    PermissionGroupChips,
    SiteMap,
    BaseList,
    ConfigurationsListItem
  },
  computed: mapState('sites', ['siteConfigurations'])

})
export default class SiteBasicData extends Vue {
  @Prop({
    default: () => new Site(),
    required: true,
    type: Site
  })
  readonly value!: Site

  // vuex definition for typescript check
  siteConfigurations!: SitesState['siteConfigurations']
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
