/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Martin Abbrent (UFZ, martin.abbrent@ufz.de)
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { WebStorageStateStore } from 'oidc-client'

export default {
  userStore: new WebStorageStateStore({ store: window.localStorage }),
  authority: process.env.NUXT_ENV_AUTHORITY,
  client_id: process.env.NUXT_ENV_CLIENT_ID,
  redirect_uri: process.env.NUXT_ENV_REDIRECT_URI,
  response_type: process.env.NUXT_ENV_RESPONSE_TYPE,
  scope: process.env.NUXT_ENV_SCOPE,
  post_logout_redirect_uri: process.env.NUXT_ENV_POST_LOGOUT_REDIRECT_URI,
  filterProtocolClaims: process.env.NUXT_ENV_FILTER_PROTOCOL_CLAIMS === 'true',
  automaticSilentRenew: process.env.NUXT_ENV_AUTOMATIC_SILENT_RENEW === 'true',
  silent_redirect_uri: process.env.NUXT_ENV_SILENT_REDIRECT_URI,
  popupWindowFeatures: 'location=no,toolbar=no,width=500,height=600,left=100,top=100', // adjusted height
  loadUserInfo: process.env.NUXT_ENV_LOAD_USER_INFO === 'true',
  renewIntervall: process.env.NUXT_ENV_SILENT_RENEW_INTERVAL
}
