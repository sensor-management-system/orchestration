<!--
SPDX-FileCopyrightText: 2020 - 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-container class="text-left">
    <v-skeleton-loader
      v-if="isLoading"
      type="table"
    />
    <v-simple-table
      v-else
    >
      <template #default>
        <thead>
          <tr>
            <th class="text-left" />
            <th class="text-left">
              STA
              <v-tooltip
                bottom
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle
                  </v-icon>
                </template>
                Links to respective SensorThings API-resources
              </v-tooltip>
            </th>
            <th class="text-left">
              Name
            </th>
            <th class="text-left">
              Description
            </th>
            <th class="text-left">
              Properties
            </th>
          </tr>
        </thead>
        <tbody>
          <TsmLinkingBasicDataTableEntry
            entity-name="Datasource"
            :entity="datasource"
            :is-loading="isLoadingStaLinks"
            :missing-sta-link-hint="missingDatasourceLinkHint"
          />
          <TsmLinkingBasicDataTableEntry
            entity-name="Thing"
            :entity="thing"
            :is-loading="isLoadingStaLinks"
            :missing-sta-link-hint="missingThingLinkHint"
          />
          <TsmLinkingBasicDataTableEntry
            entity-name="Datastream"
            :entity="datastream"
            :is-loading="isLoadingStaLinks"
            :missing-sta-link-hint="missingDatastreamLinkHint"
          />
        </tbody>
      </template>
    </v-simple-table>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions } from 'vuex'
import { Prop } from 'nuxt-property-decorator'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import TsmLinkingBasicDataTableEntry from '@/components/configurations/tsmLinking/TsmLinkingBasicDataTableEntry.vue'
import { LoadOneDatasourceAction, LoadOneDatastreamAction, LoadOneThingAction } from '@/store/tsmLinking'
import { LoadStaDatastreamsAction, LoadStaThingsAction } from '@/store/sta'

@Component({
  components: { TsmLinkingBasicDataTableEntry },
  methods: {
    ...mapActions('tsmLinking', ['loadOneDatasource', 'loadOneThing', 'loadOneDatastream']),
    ...mapActions('sta', ['loadStaThings', 'loadStaDatastreams'])
  }
})
export default class TsmLinkingBasicDataTable extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private linking!: TsmLinking

  private datasource: TsmdlDatasource = new TsmdlDatasource()
  private thing: TsmdlThing = new TsmdlThing()
  private datastream: TsmdlDatastream = new TsmdlDatastream()

  private isLoading = false
  private isLoadingStaLinks = false
  private errorLoadingStaLinks = false

  // vuex definition for typescript check
  loadOneDatasource!: LoadOneDatasourceAction
  loadOneThing!: LoadOneThingAction
  loadOneDatastream!: LoadOneDatastreamAction
  loadStaThings!: LoadStaThingsAction
  loadStaDatastreams!: LoadStaDatastreamsAction

  async created () {
    if (this.linking) {
      try {
        this.isLoading = true

        try {
          this.datasource = await this.loadOneDatasource({
            endpoint: this.linking.tsmEndpoint!,
            datasourceId: this.linking.datasource!.id
          }) ?? this.datasource
        } catch (e) {
          throw new Error('Failed to load datasource')
        }

        try {
          this.thing = await this.loadOneThing({
            endpoint: this.linking.tsmEndpoint!,
            datasource: this.linking.datasource!,
            thingId: this.linking.thing!.id
          }) ?? this.thing
        } catch (e) {
          throw new Error('Failed to load thing')
        }

        try {
          this.datastream = await this.loadOneDatastream({
            endpoint: this.linking.tsmEndpoint!,
            datasource: this.linking.datasource!,
            thing: this.linking.thing!,
            datastreamId: this.linking.datastream!.id
          }) ?? this.datastream
        } catch (e) {
          throw new Error('Failed to load datastream')
        }

        this.loadStaLinks()
      } catch (_e) {
        this.$store.commit('snackbar/setError', _e)
      } finally {
        this.isLoading = false
      }
    }
  }

  async loadStaLinks () {
    if (!this.datasource.staLink) {
      return
    }
    this.isLoadingStaLinks = true
    this.errorLoadingStaLinks = false
    try {
      await Promise.all([this.loadStaLinkForThing(), this.loadStaLinkForDatastream()])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Error while fetching STA links')
      this.errorLoadingStaLinks = true
    } finally {
      this.isLoadingStaLinks = false
    }
  }

  async loadStaLinkForThing (): Promise<void> {
    this.thing.staLink = await this.$api.staThings.findeSelfLinkByConfigurationId(this.datasource.staLink, this.configurationId)
  }

  async loadStaLinkForDatastream (): Promise<void> {
    this.datastream.staLink = await this.$api.staDatastreams.findSelfLinkByLinkingId(this.datasource.staLink, this.linking.id)
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get missingDatasourceLinkHint (): string | null {
    if (this.datasource.staLink) {
      return null
    }
    return 'No link available because the datasource has no information about the linked STA.'
  }

  get missingThingLinkHint (): string | null {
    if (this.thing.staLink || this.isLoadingStaLinks) {
      return null
    }
    if (this.errorLoadingStaLinks) {
      return 'An error occurred while fetching STA links'
    }
    if (!this.datasource.staLink) {
      return this.missingDatasourceLinkHint
    }
    return 'No link available because the thing was not found in the respective STA.'
  }

  get missingDatastreamLinkHint (): string | null {
    if (this.datastream.staLink || this.isLoadingStaLinks) {
      return null
    }
    if (this.errorLoadingStaLinks) {
      return 'An error occurred while fetching STA links'
    }
    if (!this.datasource.staLink) {
      return this.missingDatasourceLinkHint
    }
    return 'No link available because the datastream was not found in the respective STA.'
  }
}
</script>

<style>

</style>
