<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
  <section>
    <h1 class="mb-3">
      Privacy Policy
    </h1>
    <p>Please refer to the <a href="https://www.ufz.de/index.php?en=44326" target="_blank">UFZ General Data Privacy Statement</a>.</p>
    <h2 class="mb-1">
      Addendum to General Data Privacy Statement
    </h2>
    <h3 class="mb-2">
      VI. Contact form and e-mail contact
    </h3>
    <h4 class="mb-2">
      1. Description and scope of data processing
    </h4>
    <p>In addition, the following user-related data are processed when contact is made via e-mail or the contact form:</p>
    <p>
      Users are authenticated using the IdP of their respective institute. Passwords are not stored in the database.<br>
      The user-related data collected for the purpose of running the application encompasses the following:
      <ul class="mt-2">
        <li>Given name, surname</li>
        <li>E-mail address</li>
        <li>Website (if available)</li>
      </ul>
    </p>
    <p>
      For certain actions, the application also stores information on which user performed the respective action and when.<br>
      Data about times and users are stored when setting up/modifying the following:
      <ul class="mt-2">
        <li>Devices</li>
        <li>Platforms</li>
        <li>Configurations</li>
      </ul>
    </p>
    <p>Persons are still assigned to the devices as contacts for the purpose of mapping responsibilities and facilitating consultations in the event of questions about the devices.</p>
    <p>The application cannot be used to analyse user behaviour.</p>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class UfzPrivacyPolicyPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Privacy Policy' })
  }
}
</script>
