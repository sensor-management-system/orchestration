<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-list>
    <template v-for="(platform, index) in platforms">
      <v-list-item

        :key="platform.id"
      >
        <v-list-item-content>
          <v-list-item-title :class="{'text--disabled': isPlatformUsedInTree(platform)}">
            <extended-item-name :value="platform" />
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action v-if="!isPlatformUsedInTree(platform)">
          <v-btn
            v-if="isAvailable(platform) && canModifyEntity(platform)"
            depressed
            color="primary"
            @click="emitSelectedPlatform(platform)"
          >
            Select
          </v-btn>
          <v-tooltip
            v-else
            top
          >
            <template #activator="{ on }">
              <v-btn icon v-on="on" @click.stop>
                <v-icon color="warning">
                  mdi-alert
                </v-icon>
              </v-btn>
            </template>
            <span v-if="!isAvailable(platform)">{{ availabilityReason(getAvailability(platform)) }}</span>
            <span v-else-if="!canModifyEntity(platform)">No permission to select <em>{{ platform.shortName }}</em>.</span>
          </v-tooltip>
        </v-list-item-action>
      </v-list-item>
      <v-divider
        v-if="index < platforms.length - 1"
        :key="`reuse-platforms-exchange-divider-${index}`"
      />
    </template>
  </v-list>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapGetters, mapState } from 'vuex'
import { Platform } from '@/models/Platform'
import { Availability } from '@/models/Availability'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { CanModifyEntityGetter } from '@/store/permissions'
import { PlatformsState } from '@/store/platforms'
import { availabilityReason } from '@/utils/mountHelper'

@Component({
  methods: { availabilityReason },
  components: { ExtendedItemName },
  computed: {
    ...mapState('platforms', ['platforms', 'platformAvailabilities']),
    ...mapGetters('permissions', ['canModifyEntity'])
  }
})
export default class ReusePlatformExchangeList extends Vue {
  @Prop({
    required: true
  })
  readonly platformsUsedInTree!: Platform[]

  platformAvailabilities!: PlatformsState['platformAvailabilities']
  canModifyEntity!: CanModifyEntityGetter

  isPlatformUsedInTree (platform: Platform) {
    const found = this.platformsUsedInTree.find(el => el.id === platform.id)
    if (found) {
      return true
    }
    return false
  }

  isAvailable (entity: Platform): boolean {
    return this.getAvailability(entity)?.available || false
  }

  getAvailability (entity: Platform): Availability | undefined {
    return this.platformAvailabilities.find(availability => availability.id === entity.id)
  }

  emitSelectedPlatform (platform: Platform) {
    this.$emit('selected', platform)
  }
}
</script>

<style scoped>

</style>
