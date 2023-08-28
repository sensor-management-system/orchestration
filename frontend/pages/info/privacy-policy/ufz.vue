<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <p>Please refer to the <a href="https://www.ufz.de/index.php?en=44326" target="_blank">UFZ Data Privacy Statement</a>.</p>
    <h2 class="mb-1">
      Addendum to UFZ Data Privacy Statement
    </h2>
    <h3 class="mb-2">
      III. General information on data processing
    </h3>
    <h4 class="mb-2">
      1. Scope of processing of personal data
    </h4>
    <p>The purpose of this application is to help scientists and technicans to manage sensors, measurement setups and campaigns.</p>
    <p>In this context, the data will not be provided to third parties. The data is processed exclusively within the scope of the specified purpose. The legal basis for the processing of the data transmitted is the consent you have given us in accordance with Article 6 para. 1 lit. a) GDPR.</p>
    <p>Your personal data will always be deleted as soon as they are no longer required to achieve the purpose for which they were collected. The personal data collected for managing sensor and measurement campaign informations will be deleted as soon as linked entity has been deleted. Continued processing will only take place if you have given us your consent to continued processing. You can revoke your consent at any time for the future. In addition, the following user-related data is processed when contact is made via e-mail or the web forms:</p>
    <p>
      Users are authenticated using the IdP of their respective institute. Passwords are not stored in the database.<br>
      The user-related data collected for the purpose of running the application encompasses the following:
    </p>
    <p>
      <ul>
        <li>First name, last name;</li>
        <li>E-mail address;</li>
        <li>Organization;</li>
        <li>Website (if available);</li>
        <li>ORCID (if available).</li>
      </ul>
    </p>
    <p>
      In case of using the actions forms, the application also stores information about which user performed the respective action and when.<br>
      Data about times and users is stored when setting up/modifying the following:
    </p>
    <p>
      <ul>
        <li>Devices;</li>
        <li>Platforms;</li>
        <li>Configurations;</li>
        <li>Sites.</li>
      </ul>
    </p>
    <p>Furthermore, persons are assigned to the devices as contact persons for the purpose of mapping responsibilities and facilitating consultations in the event of questions about the devices.</p>
    <p>The application cannot be used to analyse user behaviour.</p>
    <h4 class="mb-2">
      2. Legal basis for the data processing
    </h4>
    <p>We process your personal data in compliance with the provisions of the General Data Protection Regulations (GDPR). The processing of the personal data provided in this context is base on Article 6 par. 1 lit. a) GDPR.</p>
    <h4 class="mb-2">
      3. Purpose of the data processing
    </h4>
    <p>The purpose of processing your personal data is to managing sensor and measurement campaign informations.</p>
    <h4 class="mb-2">
      4. Storage period
    </h4>
    <p>The above mentioned data will only be stored as long as it is necessary. It is necessary to store the data until the related entity or user account has been deleted.</p>
    <h4 class="mb-2">
      5. Right to withdrawal your consent
    </h4>
    <p>Furthermore you can withdrawn your given consent at any time without given a reasons and with effect for the future. The withdrawal does not affect the lawfulness of the processing of your data on the basis of your consent, which took place before this withdrawal. You can withdrawal you consent by sending an e-mail to <a href="mailto:sms-administration@ufz.de">sms-administration@ufz.de</a>.</p>
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
