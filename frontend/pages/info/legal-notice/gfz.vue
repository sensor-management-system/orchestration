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
      <p>Imprint according to § 5 DDG (German Digital Services Act) and § 18 (2) of the State Media Treaty (Medienstaatsvertrag, MstV)</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Provider
      </h2>
      <p>
        The <a href="https://www.gfz.de" target="_blank">GFZ Helmholtz Centre for Geosciences</a> is the provider of this website <a href="https://sensors.gfz-potsdam.de">sensors.gfz-potsdam.de</a>.
        This internet presence was developed within the DataHub initiative of the Helmholtz Association of German Research Centres.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Address
      </h2>
      <p>
        GFZ Helmholtz Centre for Geosciences<br>
        Telegrafenberg<br>
        14473 Potsdam, Germany<br>
        Tel.: +49 331 6264 0<br>
        Website: <a href="https://www.gfz.de" target="_blank">www.gfz.de</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Legal form
      </h2>
      <p>The GFZ Helmholtz Centre for Geosciences is a foundation under public law of the State of Brandenburg. The GFZ is member of the <a href="https://www.helmholtz.de" target="_blank">Helmholtz Association of German Research Centres</a>.</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Representatives
      </h2>
      <p>The GFZ is legally represented by Prof. Dr. Susanne Buiter (Scientific Executive Director and Chair of the Board) and Marco Kupzig (Administrative Executive Director (ad interim)).</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        VAT ID
      </h2>
      <p>VAT identification number according to § 27a of the Value Added Tax Act: DE138407750.</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Editorial responsibility
      </h2>
      <p>
        Editorial responsibility for this website in accordance with § 18 (2) of the State Media Treaty:<br>
        Marc Hanisch (Head of <a href="https://www.gfz.de/en/section/escience-centre" target="_blank">eScience-Centre</a>)<br>
        Phone: +49 331 6264-28929<br>
        E-Mail: <a href="mailto:marc.hanisch@gfz.de">marc.hanisch@gfz.de</a>
      </p>
      <p>
        Editor, conception, coordination (<a href="https://sensors.gfz-potsdam.de">sensors.gfz-potsdam.de</a>)<br>
        Nils Brinckmann (<a href="https://www.gfz.de/en/section/escience-centre" target="_blank">eScience-Centre</a>)<br>
        Tel.: +49 331 6264-28940<br>
        E-Mail: <a href="mailto:nils.brinckmann@gfz.de">nils.brinckmann@gfz.de</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Technical implementation and support
      </h2>
      <p>
        The organisational unit responsible for the technical implementation is the <a href="https://www.gfz.de/en/section/escience-centre" target="_blank">eScience-Centre</a>.<br>
        E-Mail: <a href="mailto:datahub-support@gfz.de">datahub-support@gfz.de</a>
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
        Texts and photos on the GFZ website are protected by copyright. Copying these files or printing these files is only permitted for private use.
      </p>
      <p>
        All other forms of use, such as the reproduction, modification or use of graphics, audio documents, video sequences and texts on the websites and in other electronic or printed publications for non-commercial or commercial purposes — even if they are not expressly marked as copyright-protected documents — are not permitted without the prior written consent of the copyright holder.
      </p>
      <p>
        Content published under special licences is identified as such. It may be used in accordance with the terms of the specific licence.
      </p>
      <p>
        Some of the data on this data portal originates from other sources. If you wish to use this data, please contact the owner of the data for the terms of use/see the respective terms of use on the websites.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Disclaimer
      </h2>
      <p>
        The GFZ checks and updates the information available on the GFZ website at regular intervals. Despite all due care, information, data or links may have changed in the meantime. Therefore, no liability or guarantee is assumed for the validity, correctness and completeness of the information provided.
      </p>
      <p>
        The same applies to all other websites to which reference is made via hyperlinks. The GFZ is not responsible for the content of websites accessed via such links. The respective operator is always responsible for the content of the linked pages. When the links were first created, the GFZ checked the sites to ensure that they were free of illegal content at the time of linking.
      </p>
      <p>
        If you discover any errors of a content-related or technical nature, please let us know.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        Data protection and IT security
      </h2>
      <p>
        You can find information on data protection in our
        <!-- eslint-disable-next-line vue/singleline-html-element-content-newline -->
        <NuxtLink to="/info/privacy-policy/">Privacy policy</NuxtLink>.<br>
        Should you have any further questions about data protection, please contact our <a href="mailto:Datenschutz@gfz.de">Data Protection Officer</a>.
        If you would like to find out more about the concepts and technical implementation of our IT security, please contact our <a href="mailto:itsec-web@gfz.de">Information Security Officer</a>.
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
