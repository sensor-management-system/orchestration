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
  <div>
    <section class="mb-6">
      <h1 class="mb-3">
        Legal information / provider identification
      </h1>
      <p>This instance of the Sensor Management System is for internal testing purposes only. The user has no right of availability or functionality of the system as well as no right of correctness or completeness of the data provided. The data-management team always aims to provide a highly available and functioning system, though.</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Provider
      </h2>
      <p>
        The provider of the internet presence <a href="https://ibg3sms.ibg.kfa-juelich.de/">ibg3sms.ibg.kfa-juelich.de</a> is the <a href="https://www.fz-juelich.de/en" target="_blank">Forschungszentrum Jülich</a>. This internet presence was developed within the DataHub initiative of the Helmholtz Association of German Research Centres.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Address
      </h2>
      <p>
        Forschungszentrum Jülich GmbH<br>
        Wilhelm-Johnen-Straße<br>
        52428 Jülich, Germany<br>
        Tel.:  +49 2461 61 0<br>
        Website: <a href="https://www.fz-juelich.de/en/ibg/ibg-3" target="_blank">www.fz-juelich.de/en/ibg/ibg-3</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Technical realization and support
      </h2>
      <p>
        Responsible for the technical implementation is the  <a href="https://www.fz-juelich.de/en/ibg/ibg-3"> Institute of Bio- and Geosciences - Agrosphere (IBG-3).</a>
      </p>
      <p>
        E-Mail: <a href="mailto:ibg3sms@fz-juelich.de">ibg3sms@fz-juelich.de</a>
      </p>
    </section>
    <section>
      <h2>
        Software licenses
      </h2>
      <p>
        This software uses third-party software components. You can find a list of licenses
        <NuxtLink to="/info/licenses/">
          here.
        </NuxtLink>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Copyright
      </h2>
      <p>
        The texts and images on this website are protected by copyright. Copying these files or printing the publications is only permitted for private use.
        All other uses, such as duplication, alteration or use of these graphics, recordings, video sequences or texts on this websites in further electronic or printed publications for non-commercial and commercial purposes are not permitted without the explicit consent of the copyright holder - even if they are not labelled as a copyright protected document.
      </p>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class FzjImprintPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Legal Notice' })
  }
}
</script>
