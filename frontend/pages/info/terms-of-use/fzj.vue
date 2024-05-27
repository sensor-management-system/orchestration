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
        Terms of use for Sensor Management System
      </h1>
      <p class="block">
        This version of the sensor management system is provided as a demonstration for testing purposes only. Users are granted access to explore and evaluate the functionalities and user experience.
      </p>
    </section>
    <section class="mb-6">
      <h3 class="mb-1">
        I. Usage guidelines:
      </h3>
      <ul>
        <li>This is a demo version intended solely for testing and evaluation purposes.</li>
        <li>The system may contain limited features and data.</li>
        <li>Users can experiment with functionality but should not rely on the data or system stability.</li>
        <li>Any data entered or generated within the demo version may be reset or deleted without notice.</li>
        <li>Users are prohibited from using this demo version for production</li>
      </ul>

      <h4 class="mb-1">
        II. Disclaimer:
      </h4>
      <p class="block">
        <ul>
          <li>The demo version may not represent the final version's features, accuracy, or performance.</li>
          <li>We do not guarantee the security, reliability, or availability of the system</li>
          <li>All data inputted or generated within the demo version is done at the user's own risk.</li>
        </ul>
      </p>
      <p class="block">
        By accessing and using this demo version, you agree to abide by these terms and conditions. Any unauthorized use beyond the scope of testing is prohibited.
      </p>
    </section>
    <section class="mb-6">
      <h3 class="mb-1">
        IX. Privacy notice
      </h3>
      <!-- eslint-disable-next-line -->
      <p class="block">See <nuxt-link to="/info/privacy-policy">Privacy policy</nuxt-link>.</p>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class FzjTermsOfUsePage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Terms of Use' })
  }

  get citation (): string {
    return 'Sensor Management System, https://ibg3sms.ibg.kfa-juelich.de, <date of access>'
  }
}
</script>

<style scoped>
.block {
  text-align: justify
}
</style>
