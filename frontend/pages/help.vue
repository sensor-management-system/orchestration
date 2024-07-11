<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-title>Help</v-card-title>
      <v-card-text>
        <p>
          Information on how to use this application can be found on our <a href="https://codebase.helmholtz.cloud/hub-terra/sms/service-desk/-/wikis/home" target="_blank" style="text-decoration: none">
            <strong>Wiki Page</strong>
          </a>.
        </p>
      </v-card-text>
      <v-card flat>
        <v-card-title>Support</v-card-title>
        <v-card-text>
          <p>
            If you require technical support or have any questions or suggestions, please send an e-mail to our <a href="mailto:gitlab-incoming+hub-terra-sms-orchestration-3268-issue-@hzdr.de" style="text-decoration: none">
              <strong>Help Desk <v-icon>mdi-message-question-outline</v-icon></strong>
            </a>
          </p>
        </v-card-text>
      </v-card>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class HelpPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Help' })
  }
}
</script>
