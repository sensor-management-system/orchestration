<!--
SPDX-FileCopyrightText: 2025
- Florian Obersteiner <florian.obersteiner@kit.edu>
- Karlsruhe Institute of Technology (KIT, https://www.kit.edu/)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <section>
      <h1>Legal Information / Provider Identification</h1>
      <p>
        Imprint according to Art. 5 of the Digital Services Act and Art. 18, par. 2, State Media Treaty (MStV)
      </p>
    </section>
    <section>
      <h2>Provider</h2>
      <p>
        The provider of the internet presence
        <a href="https://sms.atmohub.kit.edu">sms.atmohub.kit.edu</a>
        (Sensor Management System; SMS) is the
        <a href="https://www.kit.edu/" target="_blank">Karlsruhe Institute of Technology</a>, see also
        <a href="https://www.kit.edu/legals.php" target="_blank">Legals</a>. It
        is operated by the
        <a href="https://www.atmohub.kit.edu/english/index.php" target="_blank">ATMOhub</a>
        and developed within the DataHub initiative of the Helmholtz Association
        of German Research Centres.
      </p>
    </section>
    <section>
      <h2>Address</h2>
      <p>
        Karlsruhe Institute of Technology<br>
        Kaiserstraße 12<br>
        76131 Karlsruhe, Germany<br>
        Tel.: +49 721 608-0<br>
        Website: <a href="https://www.kit.edu/" target="_blank">www.kit.edu</a>
      </p>
    </section>
    <section>
      <h2>Legal Form</h2>
      <p>
        The Karlsruhe Institute of Technology (KIT) is a corporation governed by
        public law (Körperschaft des öffentlichen Rechts). The KIT is member of
        the
        <a href="https://www.helmholtz.de" target="_blank">Helmholtz-Gemeinschaft Deutscher Forschungszentren
          e.V. (Helmholtz
          Association of German Research Centres)</a>.
      </p>
    </section>
    <section>
      <h2>Authorized Representatives</h2>
      <p>
        The KIT is legally represented by Professor Dr. Jan S. Hesthaven (Acting
        President of KIT).
      </p>
    </section>
    <section>
      <h2>Value Added Tax ID</h2>
      <p>
        VAT Identification Number according to § 27a VAT Tax Act: DE266749428
      </p>
    </section>
    <section>
      <h2>Responsibility for the Content of the Website</h2>
      <p>
        Dr. Christof Lorenz (Head of IFU DataInitiative,
        <a href="https://www.imk-ifu.kit.edu/english/datainitiative.php" target="_blank">IMKIFU</a>)<br>
        Phone: +49 8821 183-214<br>
        E-Mail:
        <a href="mailto:christof.lorenz@kit.edu">christof.lorenz@kit.edu</a>
      </p>
    </section>
    <section>
      <h2>Content Management, Conception & Coordination</h2>
      <p>
        Dr. Florian Obersteiner (Data Management & IT,
        <a href="https://www.imk-asf.kit.edu/english/IAS.php" target="_blank">IMKASF</a>)<br>
        Phone: +49 721 608-28353<br>
        E-Mail:
        <a href="mailto:florian.obersteiner@kit.edu">florian.obersteiner@kit.edu</a>
      </p>
    </section>
    <section>
      <h2>Technical Realization and Support</h2>
      <p>
        Responsible for the technical implementation of this SMS instance is the
        data management & IT group
        <a href="https://www.imk-asf.kit.edu/english/IAS.php" target="_blank">at IMKASF</a><br>
        E-Mail:
        <a href="mailto:sms-curator@lists.kit.edu?subject=[SMS]">sms-curator@lists.kit.edu</a>
      </p>
    </section>
    <section>
      <h2>Software Licenses</h2>
      <p>
        The following third-party software is used within the scope of this web
        application: see <NuxtLink to="/info/licenses/">
          Licenses
        </NuxtLink>.
      </p>
    </section>
    <section>
      <h2>Copyright</h2>
      <p>
        The texts and images on this website are protected by copyright. Copying
        these files or printing the publications is only permitted for private
        use. All other uses, such as duplication, alteration or use of these
        graphics, recordings, video sequences or texts on this websites in
        further electronic or printed publications for non-commercial and
        commercial purposes are not permitted without the explicit consent of
        the copyright holder - even if they are not labelled as a copyright
        protected document.
      </p>
      <p>
        This site uses cookies to ensure technical functionality. To read more
        about what we store in the cookies, have a look at our
        <nuxt-link to="/info/privacy-policy">
          Privacy Policy
        </nuxt-link>. By
        using this service, I also accept the
        <nuxt-link to="/info/terms-of-use">
          Terms of Use
        </nuxt-link>.
      </p>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
@Component
export default class KitImprintPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Legal Notice' })
  }
}
</script>
