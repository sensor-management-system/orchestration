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
    <DynamicLocationView
      v-if="dynamicLocationAction"
      :action="dynamicLocationAction"
      :configuration-id="configurationId"
      :editable="editable"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, InjectReactive } from 'nuxt-property-decorator'
import * as VueRouter from 'vue-router'
import { mapActions, mapState } from 'vuex'
import { SetLoadingAction } from '@/store/progressindicator'
import {
  ConfigurationsState,
  LoadDynamicLocationActionAction,
  SetSelectedLocationDateAction,
  SetSelectedTimepointItemAction,
  LoadDeviceMountActionsIncludingDeviceInformationAction
} from '@/store/configurations'

import DynamicLocationView from '@/components/configurations/dynamicLocation/DynamicLocationView.vue'

@Component({
  components: { DynamicLocationView },
  computed: {
    ...mapState('configurations',
      [
        'dynamicLocationAction',
        'configurationLocationActionTimepoints',
        'selectedTimepointItem',
        'selectedLocationDate'
      ]
    )
  },
  methods: {
    ...mapActions('configurations',
      [
        'loadDynamicLocationAction',
        'loadDeviceMountActionsIncludingDeviceInformation',
        'setSelectedTimepointItem',
        'setSelectedLocationDate'
      ]
    ),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DynamicLocationActionView extends Vue {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  dynamicLocationAction!: ConfigurationsState['dynamicLocationAction']
  loadDynamicLocationAction!: LoadDynamicLocationActionAction
  selectedTimepointItem!: ConfigurationsState['selectedTimepointItem']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  setSelectedTimepointItem!: SetSelectedTimepointItemAction
  setSelectedLocationDate!: SetSelectedLocationDateAction
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
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

      await Promise.all([
        this.loadDynamicLocationAction(this.actionId),
        this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId)
      ])

      // set the date field and the date select to the correct values
      if (this.dynamicLocationAction) {
        const currentItem = this.selectedTimepointItem
        if (!currentItem || (currentItem.id !== this.dynamicLocationAction.id || currentItem.type !== 'configuration_dynamic_location_end')) {
          // date field
          if (!this.selectedLocationDate) {
            this.setSelectedLocationDate(this.dynamicLocationAction.beginDate)
          }

          // select the corresponding timepoint item
          const item = this.configurationLocationActionTimepoints.find((item) => {
            if (item.type !== 'configuration_dynamic_location_begin') {
              return false
            }
            if (item.id !== this.dynamicLocationAction!.id) {
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
