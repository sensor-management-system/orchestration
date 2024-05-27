<!--
 SPDX-FileCopyrightText: 2020 - 2023

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
          <TsmLinkingBasicDataTableEntry entity-name="Datasource" :entity="datasource" />
          <TsmLinkingBasicDataTableEntry entity-name="Thing" :entity="thing" />
          <TsmLinkingBasicDataTableEntry entity-name="Datastream" :entity="datastream" />
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

@Component({
  components: { TsmLinkingBasicDataTableEntry },
  methods: {
    ...mapActions('tsmLinking', ['loadOneDatasource', 'loadOneThing', 'loadOneDatastream'])
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

  // vuex definition for typescript check
  loadOneDatasource!: LoadOneDatasourceAction
  loadOneThing!: LoadOneThingAction
  loadOneDatastream!: LoadOneDatastreamAction

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
      } catch (_e) {
        this.$store.commit('snackbar/setError', _e)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style>

</style>
