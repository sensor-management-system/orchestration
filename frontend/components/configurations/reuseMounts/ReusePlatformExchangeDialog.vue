<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="50vw"
    @click:outside="$emit('cancel')"
  >
    <ProgressIndicator
      :value="isLoading"
    />
    <v-card>
      <v-card-title>
        Select entity
      </v-card-title>
      <v-card-text>
        <v-card flat>
          <v-tabs v-model="tab">
            <v-tab>Basic Search</v-tab>
            <v-tab>Extended Search</v-tab>
            <v-tabs-items v-model="tab">
              <v-tab-item>
                <PlatformBasicSearch
                  ref="platformBasicSearch"
                  @search-finished="checkPlatformAvailabilities"
                />
              </v-tab-item>
              <v-tab-item>
                <PlatformExtendedSearch
                  ref="platformExtendedSearch"
                  @search-finished="checkPlatformAvailabilities"
                />
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>

          <v-row
            no-gutters
            class="mt-10"
          >
            <v-col
              cols="12"
              md="3"
            >
              <PlatformFoundEntries />
            </v-col>
            <v-spacer />
            <v-col
              cols="12"
              md="6"
            >
              <PlatformPagination
                ref="platformPagination"
                @input="updateSearch"
              />
            </v-col>
            <v-col
              cols="12"
              md="3"
              class="flex-grow-1 flex-shrink-0"
            >
              <v-subheader>
                <PlatformPageSizeSelect
                  @input="setPageAndUpdateSearch"
                />
              </v-subheader>
            </v-col>
          </v-row>
          <ReusePlatformExchangeList
            v-show="availabilitiesChecked"
            :platforms-used-in-tree="platformsUsedInTree"
            @selected="emitSelectedPlatform"
          />
        </v-card>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          @click="showDialog=false"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { DateTime } from 'luxon'
import PlatformBasicSearch from '@/components/platforms/PlatformBasicSearch.vue'
import PlatformPageSizeSelect from '@/components/platforms/PlatformPageSizeSelect.vue'
import PlatformPagination from '@/components/platforms/PlatformPagination.vue'
import { Platform } from '@/models/Platform'
import ReusePlatformExchangeList from '@/components/configurations/reuseMounts/ReusePlatformExchangeList.vue'
import { LoadPlatformAvailabilitiesAction, PlatformsState } from '@/store/platforms'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import PlatformFoundEntries from '@/components/platforms/PlatformFoundEntries.vue'
import PlatformExtendedSearch from '@/components/platforms/PlatformExtendedSearch.vue'

@Component({
  components: {
    PlatformExtendedSearch,
    PlatformFoundEntries,
    ProgressIndicator,
    ReusePlatformExchangeList,
    PlatformPagination,
    PlatformPageSizeSelect,
    PlatformBasicSearch
  },
  computed: {
    ...mapState('platforms', ['platforms']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatformAvailabilities'])
  }
})
export default class ReusePlatformExchangeDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: true,
    type: Object
  })
  readonly beginDate!: DateTime

  @Prop({
    required: true
  })
  readonly platformsUsedInTree!: Platform[]

  @Prop({
    required: false,
    type: Object,
    default: null
  })
  readonly endDate!: DateTime | null

  private tab = 0
  private availabilitiesChecked = false

  platforms!: PlatformsState['platforms']
  loadPlatformAvailabilities!: LoadPlatformAvailabilitiesAction

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async checkPlatformAvailabilities () {
    try {
      const ids = this.platforms.filter((platform) => {
        const found = this.platformsUsedInTree.find(el => el.id === platform.id)
        return !found
      }).map(entity => entity.id)

      await this.loadPlatformAvailabilities({ ids, from: this.beginDate, until: this.endDate })
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of availabilities failed')
    } finally {
      this.availabilitiesChecked = true
    }
  }

  updateSearch () {
    if (this.tab === 0) {
      (this.$refs.platformBasicSearch as Vue & { search: () => void }).search()
    } else if (this.tab === 1) {
      (this.$refs.platformExtendedSearch as Vue & { search: () => void }).search()
    }
  }

  setPageAndUpdateSearch () {
    (this.$refs.platformPagination as Vue & { setPage: (val: number) => void }).setPage(1)
    this.updateSearch()
  }

  emitSelectedPlatform (platform: Platform) {
    this.$emit('selected', platform)
  }

  @Watch('showDialog')
  async onShowDialogChanged () {
    if (this.showDialog) {
      this.availabilitiesChecked = false
      await this.$nextTick()
      this.updateSearch()
    }
  }
}
</script>

<style scoped>

</style>
