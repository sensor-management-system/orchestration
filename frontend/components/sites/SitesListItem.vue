<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
  <base-expandable-list-item
    :expandable-color="site.archived ? 'brown lighten-3' : 'grey lighten-5'"
    :background-color="site.archived ? 'brown lighten-4 ' : 'white'"
  >
    <template v-if="!hideHeader" #header>
      <div class="d-flex flex-wrap">
        <div :class="'mr-1 text-caption' + (getType() === NO_TYPE ? ' text--disabled' : '')">
          {{ getType() }}
        </div>
        <visibility-chip
          v-model="site.visibility"
        />
        <permission-group-chips
          v-model="site.permissionGroups"
          collapsible
        />
      </div>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <v-btn
        :to="'/sites/' + site.id"
        color="primary"
        text
        small
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #default>
      <v-tooltip v-if="site.archived" right>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on">
            mdi-archive-lock
          </v-icon>
        </template>
        <span>Archived</span>
      </v-tooltip>
      <span>{{ site.label }}</span>
    </template>
    <template #expandable>
      <v-row
        v-if="site.address"
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          City:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ [site.address.zipCode, site.address.city] | sparseJoin(' ') | orDefault }}
        </v-col>
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Street:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ [site.address.street, site.address.streetNumber] | sparseJoin(' ') | orDefault }}
        </v-col>
      </v-row>
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Building:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ site.address.building | orDefault }}
        </v-col>
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Room:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ site.address.room | orDefault }}
        </v-col>
      </v-row>
      <!-- Counting associated configurations doesn't work at the moment this way.
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Configurations:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="10"
          lg="10"
          xl="11"
          class="nowrap-truncate"
        >
          {{ site.configurationIds.length }}
        </v-col>
      </v-row>
      -->
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Description:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="10"
          lg="10"
          xl="11"
          class="nowrap-truncate"
        >
          {{ site.description | orDefault }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'

import { Site } from '@/models/Site'

import StatusChip from '@/components/shared/StatusChip.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import { SiteUsage } from '@/models/SiteUsage'
import { getSiteTypeByUriGetter, GetSiteUsageByUriGetter } from '@/store/vocabulary'
import { SiteType } from '@/models/SiteType'

@Component({
  components: {
    StatusChip,
    VisibilityChip,
    PermissionGroupChips,
    BaseExpandableListItem
  },
  computed: mapGetters('vocabulary', [
    'getSiteUsageByUri',
    'getSiteTypeByUri'
  ])
})
export default class SitesListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private site!: Site

  @Prop({
    type: Boolean,
    default: false
  })
  private hideHeader!: boolean

  public readonly NO_TYPE: string = 'Unknown type'

  // vuex definition for typescript check
  getSiteUsageByUri!: GetSiteUsageByUriGetter
  getSiteTypeByUri!: getSiteTypeByUriGetter

  getType (): string {
    // This here is a bit more complex, compared to the devive type case.
    // The reason is that it is splitted to two parts: The site usage
    // and then the site type.
    const parts = []
    if (this.site.siteUsageName) {
      parts.push(this.site.siteUsageName)
    } else if (this.getSiteUsageByUri(this.site.siteUsageUri)) {
      const siteUsage: SiteUsage | undefined = this.getSiteUsageByUri(this.site.siteUsageUri)
      const name = siteUsage?.name
      if (name) {
        parts.push(name)
      }
    }

    if (this.site.siteTypeName) {
      parts.push(this.site.siteTypeName)
    } else if (this.getSiteTypeByUri(this.site.siteTypeUri)) {
      const siteType: SiteType | undefined = this.getSiteTypeByUri(this.site.siteTypeUri)
      const name = siteType?.name
      if (name) {
        parts.push(name)
      }
    }

    if (parts.length > 0) {
      return parts.join(': ')
    }
    return this.NO_TYPE
  }
}
</script>

<style scoped>

</style>
