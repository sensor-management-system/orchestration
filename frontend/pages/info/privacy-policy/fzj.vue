<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Rubankumar Moorthy <r.moorthy@fz-juelich.de>
- Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <section>
    <h1 class="mb-3">
      Privacy policy
    </h1>
    <p>We reserve the right to update or modify this Privacy policy for the demo version at any time. Any changes will be posted on this page, and it is your responsibility to review this Privacy policy periodically.</p>
    <p>Please refer to the <a href="https://www.fz-juelich.de/en/privacy-policy" target="_blank"> FZJ General Data Privacy Statement</a>.</p>
    <h2 class="mb-1">
      Addendum to general data privacy statement
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
        <li>Organization</li>
        <li>Website (if available)</li>
        <li>ORCID (if available)</li>
      </ul>
    </p>
    <p>
      For certain actions, the application also stores information on which user performed the respective action and when.<br>
      Data about times and users are stored when setting up/modifying the following:
      <ul class="mt-2">
        <li>Devices</li>
        <li>Platforms</li>
        <li>Configurations</li>
        <li>Sites</li>
      </ul>
    </p>
    <p>Persons are still assigned to the devices as contacts for the purpose of mapping responsibilities and facilitating consultations in the event of questions about the devices.</p>

    <p>
      To register persistent identifiers for the instruments we provide <a href="https://doi.org/10.15497/RDA00070" target="_blank">PIDINST metadata</a>
      to the <a href="https://b2inst.gwdg.de/" target="_blank">B2INST portal</a>.
      The PIDINST data contain the following personal information of the associated contacts:
    </p>
    <ul class="mt-2 mb-4">
      <li>Given name, surname</li>
      <li>E-mail address</li>
      <li>ORCID (if available)</li>
    </ul>

    <p>The application cannot be used to analyse user behaviour.</p>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class FzjPrivacyPolicyPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Privacy Policy' })
  }
}
</script>
