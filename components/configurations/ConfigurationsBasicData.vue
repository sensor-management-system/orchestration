<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-row>
      <v-col cols="12">
        <label>Visibility / Permissions</label>
        <VisibilityChip
          v-model="value.visibility"
        />
        <PermissionGroupChips
          :value="value.permissionGroup ? [value.permissionGroup] : []"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Label</label>
        {{ value.label }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Status</label>
        {{ value.status | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Persistent identifier (PID)</label>
        <v-tooltip
          :disabled="!value.persistentIdentifier"
          :color="pidTooltipColor"
          bottom
        >
          <template #activator="{ on, attrs }">
            <span
              :class="value.persistentIdentifier ? 'clickable' : ''"
              v-bind="attrs"
              v-on="on"
              @click="copyPidToClipboard"
              @mouseenter="resetPidTooltip"
            >{{ value.persistentIdentifier | orDefault }}</span>
          </template>
          <span>{{ pidTooltipText }}</span>
        </v-tooltip>
        <a
          v-if="value.persistentIdentifier"
          :href="persistentIdentifierUrl"
          target="_blank"
          class="text-decoration-none"
        >
          <v-icon small>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Start date</label>
        <span v-if="value.startDate">
          {{ value.startDate | dateToDateTimeString | orDefault }}
          <span class="text-caption text--secondary">(UTC)</span>
        </span>
        <span v-else>
          {{ null | orDefault }}
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <label>End date</label>
        <span v-if="value.endDate">
          {{ value.endDate | dateToDateTimeString | orDefault }}
          <span class="text-caption text--secondary">(UTC)</span>
        </span>
        <span v-else>
          {{ null | orDefault }}
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <label>Project</label>
        {{ value.project | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Site / Lab</label>
        <span v-if="value.siteId && site">
          <nuxt-link :to="'/sites/' + value.siteId" target="_blank">{{ site.label }}</nuxt-link><v-icon small>mdi-open-in-new</v-icon>
        </span>
        <span v-else>
          {{ null | orDefault }}
        </span>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Configuration } from '@/models/Configuration'

import { dateToDateTimeString } from '@/utils/dateHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import { LoadSiteAction, SitesState } from '@/store/sites'

@Component({
  components: {
    PermissionGroupChips,
    VisibilityChip,
    DateTimePicker
  },
  filters: {
    dateToDateTimeString
  },
  computed: mapState('sites', ['site']),
  methods: mapActions('sites', ['loadSite'])
})
export default class ConfigurationsBasicDataForm extends Vue {
  private pidTooltipColor: string = 'default'
  private pidTooltipText: string = 'Copy PID-URL'

  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

  // vuex definition for typescript check
  site!: SitesState['site']
  loadSite!: LoadSiteAction

  async mounted () {
    try {
      await this.$store.dispatch('configurations/loadConfigurationsStates')
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load configuration states')
    }

    if (this.value.siteId !== '') {
      try {
        await this.loadSite({
          siteId: this.value.siteId
        })
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Failed to load site / lab')
      }
    }
  }

  get configurationStates () { return this.$store.state.configurations.configurationStates }
  // @ts-ignore
  update (key: string, value: any) {
    // @ts-ignore
    if (typeof this.value[key] !== 'undefined') {
      const newObj = Configuration.createFromObject(this.value)
      // @ts-ignore
      newObj[key] = value
      this.$emit('input', newObj)
    }
  }

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }

  /**
   * copies the PID-URL to the clipboard and changes the tooltip's text and color
   *
   * @returns {void}
   */
  copyPidToClipboard (): void {
    if (!this.value.persistentIdentifier) { return }
    navigator.clipboard.writeText(this.persistentIdentifierUrl)
    this.pidTooltipText = 'Copied!'
    this.pidTooltipColor = 'green'
  }

  get persistentIdentifierUrl (): string {
    if (!this.value.persistentIdentifier) {
      return ''
    }
    const pidBaseUrl = process.env.pidBaseUrl
    if (!pidBaseUrl) {
      return ''
    }
    return pidBaseUrl + '/' + this.value.persistentIdentifier
  }

  /**
   * resets the PID tooltip's color and text
   *
   * @returns {void}
   */
  resetPidTooltip (): void {
    this.pidTooltipText = 'Click to copy PID-URL'
    this.pidTooltipColor = 'default'
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
