<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
  <div>
    <v-card flat>
      <nuxt-child
        v-if="manufacturerModel"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { LoadManufacturerModelAction, ManufacturermodelsState } from '@/store/manufacturermodels'
import { SetLoadingAction } from '@/store/progressindicator'
import { SetShowBackButtonAction, SetTabsAction, SetTitleAction } from '@/store/appbar'

@Component({
  computed: {
    ...mapState('manufacturermodels', ['manufacturerModel'])
  },
  methods: {
    ...mapActions('manufacturermodels', ['loadManufacturerModel']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ManufacturerModelPage extends Vue {
  // vuex definition for typescript check
  manufacturerModel!: ManufacturermodelsState['manufacturerModel']
  loadManufacturerModel!: LoadManufacturerModelAction
  setLoading!: SetLoadingAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setShowBackButton!: SetShowBackButtonAction

  mounted () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadManufacturerModel({ manufacturerModelId: this.manufacturerModelId })

      if (this.isBasePath()) {
        this.$router.replace('/manufacturer-models/' + this.manufacturerModelId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of manufacturer model failed')
    } finally {
      this.setLoading(false)
    }
  }

  get manufacturerModelId () {
    return this.$route.params.manufacturerModelId
  }

  isBasePath () {
    return this.$route.path === '/manufacturer-models/' + this.manufacturerModelId || this.$route.path === '/manufacturer-models/' + this.manufacturerModelId + '/'
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([
      {
        to: '/manufacturer-models/' + this.manufacturerModelId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/manufacturer-models/' + this.manufacturerModelId + '/devices',
        name: 'Search Devices'
      },
      {
        to: '/manufacturer-models/' + this.manufacturerModelId + '/platforms',
        name: 'Search Platforms'
      },
      {
        to: '/manufacturer-models/' + this.manufacturerModelId + '/export-control',
        name: 'Export Control'
      }
    ])
    if (this.manufacturerModel) {
      this.setTitle(`${this.manufacturerModel.manufacturerName} - ${this.manufacturerModel.model}`)
    }
  }

  @Watch('manufacturerModel', { immediate: true, deep: true })
  onManufacturerModelChange (val: ManufacturermodelsState['manufacturerModel']) {
    if (val) {
      this.setTitle(`${val.manufacturerName} - ${val.model}`)
    }
  }
}
</script>
