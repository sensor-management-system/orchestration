<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <StaticLocationView
      v-if="staticLocationAction"
      :action="staticLocationAction"
      :configuration-id="configurationId"
      :editable="editable"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import * as VueRouter from 'vue-router'

import {
  ConfigurationsState,
  LoadStaticLocationActionAction,
  SetSelectedLocationDateAction,
  SetSelectedTimepointItemAction
} from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'
import StaticLocationView from '@/components/configurations/StaticLocationView.vue'

@Component({
  components: { StaticLocationView },
  computed: {
    ...mapState('configurations',
      [
        'staticLocationAction',
        'configurationLocationActionTimepoints',
        'selectedTimepointItem',
        'selectedLocationDate'
      ]
    )
  },
  methods: {
    ...mapActions('configurations',
      [
        'loadStaticLocationAction',
        'setSelectedTimepointItem',
        'setSelectedLocationDate'
      ]
    ),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class StaticLocationActionView extends Vue {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  staticLocationAction!: ConfigurationsState['staticLocationAction']
  loadStaticLocationAction!: LoadStaticLocationActionAction
  selectedTimepointItem!: ConfigurationsState['selectedTimepointItem']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  setSelectedTimepointItem!: SetSelectedTimepointItemAction
  setSelectedLocationDate!: SetSelectedLocationDateAction
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  setLoading!: SetLoadingAction

  async fetch () {
    await this.loadLocationAction()
  }

  get actionId () {
    return this.$route.params.actionId
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async loadLocationAction () {
    try {
      this.setLoading(true)
      await this.loadStaticLocationAction(this.actionId)

      // set the date field and the date select to the correct values
      if (this.staticLocationAction) {
        const currentItem = this.selectedTimepointItem
        // if we already have a timepoint item for the end action, don't overwrite it
        if (!currentItem || (currentItem.id !== this.staticLocationAction.id || currentItem.type !== 'configuration_static_location_end')) {
          // date field
          if (!this.selectedLocationDate) {
            this.setSelectedLocationDate(this.staticLocationAction.beginDate)
          }

          // select the corresponding timepoint item
          const item = this.configurationLocationActionTimepoints.find((item) => {
            if (item.type !== 'configuration_static_location_begin') {
              return false
            }
            if (item.id !== this.staticLocationAction!.id) {
              return false
            }
            return true
          })
          if (item) {
            // date select
            this.setSelectedTimepointItem(item)
          }
        }
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading failed')
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('$route')
  async onRouteChange (newRoute: VueRouter.Route, oldRoute: VueRouter.Route) {
    if (newRoute.params.actionId !== oldRoute.params.actionId) {
      await this.loadLocationAction()
    }
  }
}
</script>

<style scoped>

</style>
