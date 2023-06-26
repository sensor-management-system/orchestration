<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
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
