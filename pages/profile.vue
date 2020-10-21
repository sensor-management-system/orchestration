<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
  <div class="user-profile">
    <div class="profile-card">
      <h1 class="profile-card__title">
        {{ userName }}
      </h1>
      <h2>Claims</h2>
      <p v-for="(value,claim) of claims" :key="claim" class="profile-card__subtitle">
        {{ claim }}: {{ value }}
      </p>
      <p>
        exp: {{ claims.exp | timeStampToFormattedGermanDateTime }}
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { timeStampToFormattedGermanDateTime } from '@/utils/dateHelper'

@Component({
  filters: {
    timeStampToFormattedGermanDateTime
  }
})
export default class ProfilePage extends Vue {
  get userName (): string {
    return this.$store.getters['auth/username']
  }

  get claims () {
    return this.$store.getters['auth/allUserClaims']
  }
}

</script>

<style scoped>
.profile-card {
  background-color: #fff;
  color: #000;
  padding: 15vmin 20vmin;
  text-align: center;
}

.profile-card__title {
  margin: 0;
  font-size: 36px;
}

.profile-card__subtitle {
  margin: 0;
  color: #c0c0c0;
  font-size: 18px;
  margin-bottom: 5px;
}
</style>
