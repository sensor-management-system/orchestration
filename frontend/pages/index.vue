<!--
SPDX-FileCopyrightText: 2020 - 2025
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-container class="mx-0 px-0 pt-0 grey lighten-5" fluid>
    <v-parallax
      id="parallax-bg"
      height="350"
      src="banner_sensor.jpg"
      alt="A measuring device with water hoses connected to it"
    >
      <v-row
        align="center"
        justify="center"
        class="mb-n10 pb-0"
        no-gutters
      >
        <v-col
          class="text-left"
          cols="8"
        >
          <h1 class="text-h5">
            Welcome to the<br>
          </h1>
          <v-img
            style="margin-left: -40px; margin-top: -20px; margin-bottom: -40px;"
            contain
            position="center left"
            height="10em"
            src="logos/ufz-sms_logo_weiss-transparent.svg"
          />
        </v-col>
      </v-row>
      <v-container class="mt-n20 px-12 pb-16">
        <v-row justify="center" class="mt-0">
          <!-- <v-spacer /> -->
          <v-col cols="3" class="d-flex flex-column align-center">
            <div class="counter-number">
              {{ stats.devices }}
            </div>
            <div>Devices</div>
          </v-col>
          <v-col cols="3" class="d-flex flex-column align-center">
            <div class="counter-number">
              {{ stats.platforms }}
            </div>
            <div>Platforms</div>
          </v-col>
          <v-col cols="3" class="d-flex flex-column align-center">
            <div class="counter-number">
              {{ stats.configurations }}
            </div>
            <div>Configurations</div>
          </v-col>
          <v-col cols="3" class="d-flex flex-column align-center">
            <div class="counter-number">
              {{ stats.sites }}
            </div>
            <div>Sites & Labs</div>
          </v-col>
        <!-- <v-spacer /> -->
        </v-row>
      </v-container>
    </v-parallax>

    <v-container class="mt-n14 px-12">
      <v-row justify="center">
        <v-col cols="12" md="3" sm="12">
          <basic-overview-card
            :entity-name="deviceInfo.name"
            :entity-name-plural="deviceInfo.name + 's'"
            :description="deviceInfo.description"
            :url="deviceInfo.url"
            :icon="deviceInfo.icon"
          />
        </v-col>

        <v-col cols="12" md="3" sm="12">
          <basic-overview-card
            :entity-name="platformInfo.name"
            :entity-name-plural="platformInfo.name + 's'"
            :description="platformInfo.description"
            :url="platformInfo.url"
            :icon="platformInfo.icon"
          />
        </v-col>

        <v-col cols="12" md="3" sm="12">
          <basic-overview-card
            :entity-name="configurationInfo.name"
            :entity-name-plural="configurationInfo.name + 's'"
            :description="configurationInfo.description"
            :url="configurationInfo.url"
            :icon="configurationInfo.icon"
          />
        </v-col>

        <v-col cols="12" md="3" sm="12">
          <basic-overview-card
            :entity-name="siteInfo.name"
            :entity-name-plural="siteInfo.namePlural"
            :description="siteInfo.description"
            :url="siteInfo.url"
            :icon="siteInfo.icon"
          />
        </v-col>
      </v-row>

      <v-row v-if="!isLoggedIn" justify="center" align="stretch">
        <v-alert color="warning">
          You are are currently not logged in. You can not create or edit any data.
        </v-alert>
      </v-row>

      <v-row class="d-flex">
        <v-col cols="12" :md="showReleaseNotes ? 8 : 12">
          <v-row>
            <v-col cols="12">
              <v-card>
                <v-row no-gutters class="d-flex flex-no-wrap justify-space-between">
                  <v-col cols="8">
                    <div class="primary white--text rounded rounded-b-0 rounded-tr-0">
                      <v-card-title class="text-h5 font-weight-bold">
                        SMS - Introduction
                      </v-card-title>

                      <v-card-subtitle>Sensor Management System</v-card-subtitle>
                    </div>
                    <v-divider />

                    <v-card-text class="primary_text--text">
                      <p>
                        The purpose of this application is to help scientists and technicians to manage sensors,
                        measurement setups and campaigns.
                      </p>
                      <p>
                        If you don't have an account, you can browse and view all datasets.<br>
                        If you're already registered, you can login above.
                      </p>
                      <p>
                        Good places to get started are our
                        <a
                          href="https://codebase.helmholtz.cloud/hub-terra/sms/service-desk/-/wikis/home"
                          target="_blank"
                          style="text-decoration: none"
                        >Wiki Page</a>
                        and the <a
                          href="https://codebase.helmholtz.cloud/hub-terra/sms/service-desk/-/wikis/SMS%20Tutorial%20Videos"
                          target="_blank"
                          style="text-decoration: none"
                        >Tutorial Videos</a>.
                      </p>
                    </v-card-text>
                  </v-col>
                  <v-col cols="4">
                    <v-img class="rounded rounded-l-0" height="100%" width="100%" src="UFZ_Standort-7.jpg" />
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>

          <v-row v-if="isMobileView && showReleaseNotes" justify="center" align="stretch">
            <v-col cols="12">
              <ReleaseNotes
                :link-to-release-notes="linkToReleaseNotes"
                @close="showReleaseNotes = false"
              />
            </v-col>
          </v-row>

          <v-row v-if="isLoggedIn" justify="center" align="stretch">
            <v-col cols="12">
              <recent-activity-overview-card
                :amount-of-recents="5"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col
          v-if="isDesktopView && showReleaseNotes"
          class="d-flex"
          cols="12"
          md="4"
          style="align-self: start; min-height: 25vh"
        >
          <ReleaseNotes
            :link-to-release-notes="linkToReleaseNotes"
            @close="showReleaseNotes = false"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import BasicOverviewCard from '@/components/overview/BasicOverviewCard.vue'
import { StatisticsCount } from '@/models/Statistics'
import RecentActivityOverviewCard from '@/components/overview/RecentActivityOverviewCard.vue'

import { SetFullWidthAction, SetDefaultsAction } from '@/store/defaultlayout'
import ReleaseNotes from '@/components/ReleaseNotes.vue'
import { ViewPort } from '@/mixins/ViewportMixin'

@Component({
  components: {
    ReleaseNotes,
    BasicOverviewCard,
    RecentActivityOverviewCard
  },
  methods: {
    ...mapActions('defaultlayout', ['setFullWidth', 'setDefaults'])
  }
})
export default class OverviewIndex extends mixins(ViewPort) {
  setFullWidth!: SetFullWidthAction
  setDefaults!: SetDefaultsAction

  private stats = new StatisticsCount()
  private showReleaseNotes = !!process.env.showReleaseNotes

  private linkToReleaseNotes = 'https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/blob/main/CHANGELOG.md'

  created () {
    this.setFullWidth(true)
    this.$store.dispatch('appbar/setDefaults')
    this.getUsageStatistics()
  }

  async getUsageStatistics (): Promise<void> {
    try {
      const result = await this.$api.statisticsApi.getCounts()
      this.stats = result
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load usage statistics')
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get isLoggedIn () {
    return this.$auth.loggedIn
  }

  deviceInfo = {
    name: 'Device',
    description: `Devices are measuring equipment which record physical measured data. This can for example be complex multi parameter probes or a single sensor.
Metainformation is recorded here, such as the type of device, the measured variables, specific properties, corresponding calibration actions and software updates. The measured quantities of a device should be invariant over the life cycle as far as possible.`,
    url: '/devices',
    icon: 'mdi-network'
  }

  platformInfo = {
    name: 'Platform',
    description: 'A platform is a mechanical device onto which other platforms or devices are mounted (e.g. ship, tower, mounting plate). Platforms themselves do not collect data, but are used to describe the physical structure of an entire measuring setup.',
    url: '/platforms',
    icon: 'mdi-rocket'
  }

  configurationInfo = {
    name: 'Configuration',
    description: 'The configuration brings platforms and devices into a temporal and spatial relationship and thus describes a measurement campaign or experiment. This is also the place to add more information about the measurement itself like the georeference, offsets, measuring periods, the real mounting setup and field activities and any changes during its lifetime.',
    url: '/configurations',
    icon: 'mdi-file-cog'
  }

  siteInfo = {
    name: 'Site / Lab',
    namePlural: 'Sites & Labs',
    description: 'In Sites & Labs you have the possibility to manage sites/laboratories/locations that are attached to a configuration. There are various options here: From a spatial boundary of a region of interest, down to buildings & rooms of laboratory complexes.',
    url: '/sites',
    icon: 'mdi-map-marker-radius'
  }
}
</script>
<style>
#parallax-bg .v-parallax__content {
  background: linear-gradient(45deg, #1e1e1e, transparent);
}

.counter-number {
  font-size: 2.5em;
  font-weight: bold;
  color: #F9BA2E;
}
</style>
