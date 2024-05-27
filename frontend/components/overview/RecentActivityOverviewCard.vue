<!--
SPDX-FileCopyrightText: 2022 - 2023
- Erik Pongratz <erik.pongratz@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
            <v-icon v-else-if="entity.type === 'site'">
              mdi-map-marker-radius
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <nuxt-link
              :to="getEntityURL(entity)"
              style="text-decoration: none;"
            >
              <v-list-item-title v-if="entity.type === 'device' || entity.type === 'platform'">
                {{ entity.shortName }}
              </v-list-item-title>
              <v-list-item-title v-else-if="entity.type === 'configuration' || entity.type === 'site'">
                {{ entity.label }}
              </v-list-item-title>
              <v-list-item-subtitle>{{ getEntitySubtitle(entity) }}</v-list-item-subtitle>
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
import { Site } from '@/models/Site'

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
  private recentSites: Site[] = []

  created () {
    this.loadRecentEntities()
  }

  async loadRecentEntities () {
    try {
      this.loading = true
      const result = await Promise.all([
        this.$api.devices.searchRecentlyUpdated(this.amountCopy),
        this.$api.platforms.searchRecentlyUpdated(this.amountCopy),
        this.$api.configurations.searchRecentlyUpdated(this.amountCopy),
        this.$api.sites.searchRecentlyUpdated(this.amountCopy)
      ])
      this.recentDevices = result[0]
      this.recentPlatforms = result[1]
      this.recentConfigurations = result[2]
      this.recentSites = result[3]
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of recent activity failed')
    } finally {
      this.loading = false
    }
  }

  get isLoggedIn () {
    return this.$auth.loggedIn
  };

  get recentEntities (): Array<Device | Platform | Configuration | Site> {
    return [...this.recentDevices, ...this.recentPlatforms, ...this.recentConfigurations, ...this.recentSites].sort((a, b) => {
      if (a.updatedAt && b.updatedAt) {
        return b.updatedAt.toUnixInteger() - a.updatedAt.toUnixInteger()
      } else {
        return 0
      }
    }).splice(0, this.amountCopy)
  }

  getEntityURL = (entity: Device | Platform | Configuration | Site): string => {
    const entityType = entity.type
    switch (entityType) {
      case 'device':
        return '/devices/' + entity.id
      case 'platform':
        return '/platforms/' + entity.id
      case 'configuration':
        return '/configurations/' + entity.id
      case 'site':
        return '/sites/' + entity.id
      default:
        return '/'
    }
  }

  getEntitySubtitle = (entity: Device | Platform | Configuration | Site): string => {
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
