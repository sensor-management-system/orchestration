<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
  <div>
    <section class="mb-6">
      <h1 class="mb-3">
        Terms of Use for Sensor Management System
      </h1>
      <p>
        By using the offered services at <a href="https://sensors.gfz-potsdam.de">sensors.gfz-potsdam.de</a>
        (“Services”) you agree to the following terms of use of Helmholtz Centre Potsdam – GFZ German Research
        Centre for Geosciences (“GFZ”), a Public Law Foundation under the laws of the Federal State of
        Brandenburg/Germany, Telegrafenberg, 14473 Potsdam, Germany,
        Mail: <a href="mailto:datahub-support@gfz-potsdam.de">datahub-support@gfz-potsdam.de</a>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        I. Scope of licenses and usage
      </h2>
      <h3 class="mb-2">
        (1) Allowed Use
      </h3>
      <p>
        The Services provide data and information supplied by GFZ as well as obtained on the basis of data and software
        provided by third parties (“third party material”). When using the Services, you always have to observe the
        licenses of the third party material as given by the third parties and give the according Copyright Contribution
        (see Art. II). In case of doubt about the allowed use, you must contact the copyright holder directly.
      </p>
      <p>
        As far as it would not be in contrast to the licenses of used third party material, the Services and provided
        data can be used for scientific, educational, informational and research purposes. Within this purpose, you
        are requested not to make the data available for download elsewhere.
      </p>
      <p>
        A commercial use is explicitly forbidden and would request a separate agreement; please contact GFZ or – if
        there is - named the separate copyright holder of the data, information or Services.
      </p>
      <p>
        The Services rendered in connection with the sensor management system encompass the storage of data
        and information previously collected by the user group. Data may only be read, modified, recreated and
        stored by persons with authorised access.
      </p>
      <p>
        The data may only be used for work purposes, i.e. for the GFZ directly and for projects, initiatives and
        systems associated with the GFZ.
      </p>
      <h3 class="mb-2">
        (2) Unacceptable Use
      </h3>
      <p>The following uses of the Services are strictly forbidden and can lead to IP blocking when doing so:</p>
      <p>
        <ul>
          <li>
            heavy use of the Services from an application or individual person;
            examples for heavy use are:
            using our Services as a fallback for your own services,
            more than 500 requests within one minute,
            more than 5000 requests within one hour
          </li>
          <li>seeding or crawling the Services</li>
          <li>sending the same request multiple times in a short amount of time</li>
          <li>monitoring the Services in a periodically manner</li>
          <li>bulk downloading, if not explicitly permitted (see next paragraph I. (3))</li>
          <li>attempting to circumvent administrative authorisations and security mechanisms</li>
        </ul>
      </p>
      <p>
        Furthermore, the following conditions must be complied with when using the Services. The respective
        home institution will be notified in the event of any of these conditions being breached. The
        institution will then decide on any legal action that may be necessary.
      </p>
      <p>
        <ul>
          <li>No uploading of private content </li>
          <li>No uploading of illegal content</li>
          <li>
            No uploading of content that breaches copyright regulations, personality rights, or confidentiality
            undertakings signed in connection with your work
          </li>
        </ul>
      </p>
      <h3 class="mb-2">
        (3) Bulk Downloading
      </h3>
      <p>
        As a general rule, bulk downloading of larger amounts of data is not allowed. Smaller one-time bulk
        downloads may be possible if you ask the system administrators for permission to do so. For those
        bulk downloads following additional rules apply:
      </p>
      <p>
        <ul>
          <li>limit your request to a single thread</li>
          <li>request from one machine only, no distributed scripts (for example a cluster or cloud service)</li>
          <li>results must be cached on your side, so clients sending repeatedly the same request may be blocked</li>
        </ul>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        II. Copyright Attribution
      </h2>
      <p>
        You have to give copyright attribution accordingly when using a Service and publishing the contents
        in public or even for further internal use.
        You are not allowed to remove any copyright marks.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        III. Citation
      </h2>
      <p>
        If You use the Services and/or data sets in a presentation or publication, for instance by linking in your
        website, then You have to acknowledge the Sercvies as the source of the material.
        The Services or data sources can be cited as defined by the copyright attributions of the metadata
        of the Service or underlying datasets.
        You may not use the Services in a way that suggests any official status or that GFZ endorses any particular
        application of the Services by You.
        You may not mislead others or misrepresent the Services and its sources.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        IV. Interface for Websites and Applications
      </h2>
      <p>
        (1) You can access the data or integrate the data via the interfaces provided by the Service. You use the
        Services at your own risk and under your own responsibility.
      </p>
      <p>
        (2) When calling the Services from a web application or by programmatic script (like Shell, Python or R)
        please be sure to provide a valid HTTP referer and/or user agent identifying the application or client.
        The HTTP requests should contain at least one of the headers “Referer” or “User-Agent” as it is shown in
        the following examples:
      </p>
      <p>
        <ul>
          <li>in case of a request from a web application: Referer: example.org</li>
          <li>in case of a script (for example a request from cURL): User-Agent: curl/7.37.0</li>
        </ul>
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        V. No Warranty, Disclaimer
      </h2>
      <p>
        (1) GFZ does not warrant that the Services will function without errors or interruptions. GFZ reserves
        the right at any time to change or discontinue any aspect or feature of the offered Services,
        including, without limitation, the content, hours of availability, and equipment needed for accessing
        or using the services, as well as to terminate the Services themselves.
      </p>
      <p>
        (2) The Services are provided “as is” without warranty or representation of any kind, either expressed or implied,
        including, but not limited to, the implied warranties of accuracy, completeness, quality, topicality,
        fitness for a particular purpose or the absence of any infringement of any proprietary rights of third parties.
      </p>
      <p>
        (3) Therefore You shall in all cases be entirely and solely liable for the use to which You put such
        information and material. GFZ shall not be held responsible for the performance of or output obtained
        from the Services nor for any liability to any party arising out of use of the Services.
      </p>
      <p>
        (4) GFZ shall only be liable for willful misconduct and gross negligence. For slight negligence, GFZ
        shall only be liable in the event of breach of a material contractual obligation (cardinal obligation),
        the fulfilment of which is essential for the proper performance of the contract and on the enhancement
        of which You may regularly rely, as well as in the event of damage resulting from injury to life, limb
        or health or statutory liability.
      </p>
      <p>
        (5) In no event GFZ shall be liable to You for any incidental, consequential or indirect damages (including,
        but not limited to, damages for loss of data, cost of procurement of substitute services or service
        interruptions) arising out of the use or inability to use the Services.
      </p>
      <p>
        (6) If instruments are provided free of charge in case of academic and non-profit projects. The provision
        to industry and commercial projects is subject of a separate Contract and payment. The use of the instruments
        is at users own risk. The GFZ does assume no liability of the general suitability of the instruments for the
        intended purposes. GFZ is not responsible for any kind of damages resulting from the use of the instruments.
        Furthermore, GFZ is not responsible for the accuracy and correctness of the data.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        VI. Applicable Law
      </h2>
      <p>
        The Laws of the Federal Republic of Germany apply to these Terms of Use, under exception of the regulations
        of the Convention of International Sales of Goods.
      </p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        VII. Privacy Notice
      </h2>
      <!-- eslint-disable-next-line -->
      <p>See <nuxt-link to="/info/privacy-policy">Privacy Policy</nuxt-link>.</p>
    </section>
    <section class="mb-6">
      <h2 class="mb-1">
        VIII. Changes to these Terms of Use
      </h2>
      <p>
        Please be aware that these terms of use may change without notice. In particular, the definition of
        heavy use may need to be modified in the future and You might have to change your access to those services.
        Applications using the Services should keep that in mind.
      </p>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class GfzTermsOfUsePage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Terms of Use' })
  }
}
</script>
