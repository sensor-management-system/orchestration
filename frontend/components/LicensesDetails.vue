<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-col>
    <div v-for="(value, key, index) in licensesList" :key="index">
      <h3>
        {{ key }}
      </h3>
      <div>
        License: {{ value.licenses }}<br>
        Authors: {{ value.publisher }}<br>
        <v-divider />
      </div>
    </div>
  </v-col>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

export interface License {
    id?: string;
    licenses?: string | string[];
    repository?: string;
    publisher?: string;
    url?: string;
    name?: string;
    errno?: number;
    syscall?: string;
    code?: string;
    path: string;
    licenseFile?: string;
    licenseText?: string;
    copyright?: string;
}

@Component
export default class LicensesDetails extends Vue {
  // we have to use require here, because 'import' causes typescript compiler errors
  private json = require('@/generated/licenses.json')

  public licensesList: Record<string, License> = this.json
}

</script>
