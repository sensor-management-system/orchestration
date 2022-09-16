<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
  <div>
    <ProgressIndicator
      v-model="isLoading"
    />
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
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import StaticLocationView from '@/components/configurations/StaticLocationView.vue'
import { ConfigurationsState, LoadStaticLocationActionAction } from '@/store/configurations'
@Component({
  components: { StaticLocationView, ProgressIndicator },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['staticLocationAction'])
  },
  methods: {
    ...mapActions('configurations', ['loadStaticLocationAction'])
  }
})
export default class StaticLocationActionView extends Vue {
  @InjectReactive()
    editable!: boolean

  private isLoading = false

  // vuex definition for typescript check
  staticLocationAction!: ConfigurationsState['staticLocationAction']
  loadStaticLocationAction!: LoadStaticLocationActionAction

  async created () {
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
      this.isLoading = true
      await this.loadStaticLocationAction(this.actionId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading failed')
    } finally {
      this.isLoading = false
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
