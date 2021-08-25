<!--<template v-if="lastActiveSearcher != null">-->
<template>
  <v-menu
    close-on-click
    close-on-content-click
    offset-x
    left
    z-index="999"
  >
    <template #activator="{ on }">
      <v-btn
        icon
        v-on="on"
      >
        <v-icon
          dense
        >
          mdi-file-download
        </v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item
        dense
        @click.prevent="exportCsv"
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-icon
              left
            >
              mdi-table
            </v-icon>
            CSV
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import { ConfigurationSearcher } from '@/services/sms/ConfigurationApi'

@Component
export default class ConfigurationsDownloader extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly lastActiveSearcher!: ConfigurationSearcher;

  exportCsv () { // TODO lastActiveSearcher ist nur noch in der ConfigurationsSearch
    this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
      saveAs(blob, 'configurations.csv')
    }).catch((_err) => {
      this.$store.commit('snackbar/setError', 'CSV export failed')
    })
  }
}
</script>

<style scoped>

</style>
