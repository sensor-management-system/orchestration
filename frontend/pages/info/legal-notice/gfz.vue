<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <section class="mb-6">
      <h1 class="mb-3">
        Legal information / Provider Identification
      </h1>
      <p>Imprint according to § 5 TMG (Tele Media Act) and § 55 RStV (German Interstate Treaty on Broadcasting)</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Provider
      </h2>
      <p>
        The provider of the internet presence <a href="https://sensors.gfz-potsdam.de">sensors.gfz-potsdam.de</a> is the <a href="https://www.gfz-potsdam.de/en/" target="_blank">Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ</a>. This internet presence was developed within the DataHub initiative of the Helmholtz Association of German Research Centres.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Address
      </h2>
      <p>
        Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ<br>
        Telegrafenberg<br>
        14473 Potsdam, Germany<br>
        Tel.: +49 331 6264 0<br>
        Website: <a href="https://www.gfz-potsdam.de" target="_blank">www.gfz-potsdam.de</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Legal form
      </h2>
      <p>The Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ is a Public Law Foundation. The GFZ is member of the <a href="https://www.helmholtz.de" target="_blank">Helmholtz-Gemeinschaft Deutscher Forschungszentren e.V. (Helmholtz Association of German Research Centres)</a>.</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Authorized representatives
      </h2>
      <p>The GFZ is legally represented by Prof. Dr. Susanne Buiter (Scientific Executive Director and Spokesperson of the Executive Board) and Marco Kupzig (Administrative Executive Director, ad interim).</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Value Added Tax ID
      </h2>
      <p>VAT Identification Number according to § 27a VAT Tax Act: DE138407750</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Editorial Staff
      </h2>
      <p>
        Responsible editor for the contents of this internet presence with regard to media law is<br>
        Martin Hammitzsch (Head of <a href="https://www.gfz-potsdam.de/en/section/escience-centre" target="_blank">eScience-Centre</a>)<br>
        Phone: +49 331 6264-1717<br>
        E-Mail: <a href="mailto:martin.hammitzsch@gfz-potsdam.de">martin.hammitzsch@gfz-potsdam.de</a>
      </p>
      <p>
        Editor, conception, coordination (<a href="https://sensors.gfz-potsdam.de">sensors.gfz-potsdam.de</a>)<br>
        Nils Brinckmann (<a href="https://www.gfz-potsdam.de/en/section/escience-centre" target="_blank">eScience-Centre</a>)<br>
        Tel.: +49 331 6264-28940<br>
        E-Mail: <a href="mailto:nils.brinckmann@gfz-potsdam.de">nils.brinckmann@gfz-potsdam.de</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Technical Realization and support
      </h2>
      <p>
        Responsible for the technical implementation is the <a href="https://www.gfz-potsdam.de/en/section/escience-centre" target="_blank">eScience-Centre</a><br>
        E-Mail: <a href="mailto:datahub-support@gfz-potsdam.de">datahub-support@gfz-potsdam.de</a>
      </p>
    </section>
    <section>
      <h2>
        Software licenses
      </h2>
      <p>
        The following third-party software is used within the scope of this web application <br>
        <!-- eslint-disable-next-line vue/singleline-html-element-content-newline -->
        <NuxtLink to="/info/licenses/">Licenses</NuxtLink>.
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
export default class GfzImprintPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Legal Notice' })
  }
}
</script>
