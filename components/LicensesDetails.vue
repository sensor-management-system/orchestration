<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
