<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <v-card
    class="mx-auto"
    tile
    transition="slide-x-transition"
  >
    <v-list shaped>
      <v-subheader>Recent Activity</v-subheader>
      <v-list-item-group
        color="primary"
      >
        <div v-if="loading">
          <v-skeleton-loader
            v-for="i in amountCopy"
            :key="i"
            max-width="400"
            type="list-item-avatar-two-line"
          />
        </div>
        <v-list-item
          v-for="(entity, i) in recentEntities"
          :key="i"
        >
          <v-list-item-icon>
            <v-icon v-if="entity.type === 'device'">
              mdi-network
            </v-icon>
            <v-icon v-else-if="entity.type === 'platform'">
              mdi-rocket
            </v-icon>
            <v-icon v-else-if="entity.type === 'configuration'">
              mdi-file-cog
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <nuxt-link
              :to="getEntityURL(entity)"
              style="text-decoration: none;"
            >
              <v-list-item-title v-if="entity.type === 'device' || entity.type === 'platform'" v-text="entity.shortName" />
              <v-list-item-title v-else-if="entity.type === 'configuration'" v-text="entity.label" />
              <v-list-item-subtitle v-text="getEntitySubtitle(entity)" />
            </nuxt-link>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
      <v-list-item class="justify-center" @click="amountCopy+=amountOfRecents">
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              v-on="on"
            >
              mdi-chevron-down
            </v-icon>
          </template>
          <span>Load more</span>
        </v-tooltip>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'
import { Configuration } from '@/models/Configuration'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

@Component
export default class RecentActivityOverviewCard extends Vue {
  @Prop({
    type: Number,
    default: 5
  })
  private readonly amountOfRecents!: number

  private amountCopy = this.amountOfRecents

  private loading: boolean = false
  private recentDevices: Device[] = []
  private recentPlatforms: Platform[] = []
  private recentConfigurations: Configuration[] = []

  created () {
    this.loadRecentEntities()
  }

  async loadRecentEntities () {
    try {
      this.loading = true
      const result = await Promise.all([
        this.$api.devices.searchRecentlyUpdated(this.amountCopy),
        this.$api.platforms.searchRecentlyUpdated(this.amountCopy),
        this.$api.configurations.searchRecentlyUpdated(this.amountCopy)
      ])
      this.recentDevices = result[0]
      this.recentPlatforms = result[1]
      this.recentConfigurations = result[2]
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of recent activity failed')
    } finally {
      this.loading = false
    }
  }

  get isLoggedIn () {
    return this.$auth.loggedIn
  };

  get recentEntities (): Array<Device | Platform | Configuration> {
    return [...this.recentDevices, ...this.recentPlatforms, ...this.recentConfigurations].sort((a, b) => {
      if (a.updatedAt && b.updatedAt) {
        return b.updatedAt.toUnixInteger() - a.updatedAt.toUnixInteger()
      } else {
        return 0
      }
    }).splice(0, this.amountCopy)
  }

  getEntityURL = (entity: Device | Platform | Configuration): string => {
    const entityType = entity.type
    switch (entityType) {
      case 'device':
        return '/devices/' + entity.id
      case 'platform':
        return '/platforms/' + entity.id
      case 'configuration':
        return '/configurations/' + entity.id
      default:
        return '/'
    }
  }

  getEntitySubtitle = (entity: Device | Platform | Configuration): string => {
    const modifiedAtMessage = dateToDateTimeStringHHMM(entity.updatedAt)
    const description = this.getUpdateDescription(entity.updateDescription)
    let entityText = ''
    if (description.action.toLowerCase() === 'create' && description.field.toLowerCase() === 'basic data') {
      entityText = `${description.action}d a new ${entity.type}`
    } else if (description.action === '') {
      entityText = `updated the ${entity.type}`
    } else {
      entityText = `${description.action}d the ${entity.type}'s "${description.field.toLowerCase()}"`
    }
    const subtitle = `${modifiedAtMessage}: ${entity.updatedBy} ${entityText}`
    return subtitle
  }

  getUpdateDescription = (description: string): { action: string, field: string} => {
    const descriptionObject = {
      action: '',
      field: ''
    }
    const splitted = description.split(';')
    let action: string
    let field: string
    if (splitted.length > 1) {
      action = splitted[0]
      field = splitted[1]
    } else {
      action = ''
      field = ''
    }
    descriptionObject.action = action
    descriptionObject.field = field

    return descriptionObject
  }

  @Watch('amountCopy')
  onAmountChanged () {
    this.loadRecentEntities()
  }
}
</script>

<style scoped>

</style>
