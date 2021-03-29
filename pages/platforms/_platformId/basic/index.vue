<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
    <PlatformBasicData
      v-model="platform"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'
import PlatformBasicData from '@/components/PlatformBasicData.vue'

@Component({
  components: {
    PlatformBasicData
  }
})
export default class PlatformShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Platform

  get platform (): Platform {
    return this.value
  }

  set platform (value: Platform) {
    this.$emit('input', value)
  }

  get platformId () {
    return this.$route.params.platformId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
