/*
Web client of the Sensor Management System software developed within
the Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Wilhelm Becker (GFZ, wilhelm.becker@gfz-potsdam.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
*/

// eslint-disable-next-line
import colors from 'vuetify/es5/util/colors'
import fs from 'fs'
import path from 'path'

const server = {
  port: 3000,
  host: '0.0.0.0'
}

const oidcEndpoints = {
  configuration: process.env.NUXT_ENV_OIDC_WELL_KNOWN,
  logout: false
}

const oAuthEndpoints = {
  authorization: process.env.NUXT_ENV_AUTHORITY,
  token: process.env.NUXT_ENV_OIDC_TOKEN,
  userInfo: process.env.NUXT_ENV_OIDC_USER_INFO,
  logout: undefined
}

if (!process.env.STAY_WITH_HTTP || process.env.STAY_WITH_HTTP !== 'true') {
  server.https = {
    key: fs.readFileSync(path.resolve(__dirname, 'server.key')),
    cert: fs.readFileSync(path.resolve(__dirname, 'server.crt'))
  }
}

export default {
  server,
  ssr: false,
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  env: {
    smsBackendUrl: process.env.SMS_BACKEND_URL || 'http://localhost:5000/rdm/svm-api/v1',
    cvBackendUrl: process.env.CV_BACKEND_URL || 'http://localhost:5001/api',
    institute: process.env.INSTITUTE || ''
  },
  /*
  ** Headers of the page
  */
  head: {
    title: 'Sensor Management System',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    '@/assets/Roboto.css',
    '@mdi/font/css/materialdesignicons.min.css'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~/plugins/fullContext.ts',
    '~/plugins/api.ts',
    '~/plugins/filters.ts'
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxt/typescript-build',
    '@nuxtjs/vuetify'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/auth-next',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv',
    'nuxt-leaflet'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
  },
  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en'
    }
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    optionsPath: '~/config/vuetify/vuetify.options.js',
    // needed to include own fonts
    defaultAssets: false
  },
  /*
  ** Build configuration
  */
  build: {
    babel: {
      // due to a bug with nuxtjs and babel we have to explictly set 'loose' to true
      // see https://github.com/nuxt/nuxt.js/issues/9224#issuecomment-893289291
      plugins: [['@babel/plugin-proposal-private-property-in-object', { loose: true }]]
    }
  },
  router: {
    base: process.env.BASE_URL || '/',
    middleware: ['institute-pages']
  },
  auth: {
    cookie: false,
    redirect: {
      login: '/',
      home: '/login-success',
      callback: '/login-callback'
    },
    strategies: {
      customStrategy: {
        // ToDo: Set customOIDCScheme as default, when every deployment uses the customOIDCScheme
        scheme: process.env.NUXT_ENV_OIDC_SCHEME ? '~/config/auth/schemes/customOIDCScheme' : '~/config/auth/schemes/customScheme',
        // ToDo: Remove the oAuth endpoint configuration, when every deployment uses the customOIDCScheme
        endpoints: process.env.NUXT_ENV_OIDC_SCHEME ? oidcEndpoints : oAuthEndpoints,
        token: {
          // ToDo: Set Access token as default, when every deployment uses the customOIDCScheme
          property: process.env.NUXT_ENV_OIDC_SCHEME ? 'access_token' : 'id_token',
          type: 'Bearer',
          maxAge: 3600
        },
        refreshToken: {
          property: process.env.NUXT_ENV_OIDC_REFRESH_TOKEN || false,
          // GFZ Refresh token refresh time is not fetched from the server response.
          // This leads us into setting this time via env variable
          maxAge: process.env.NUXT_ENV_OIDC_REFRESH_EXPIRE || 60 * 60 * 24 * 30
        },
        responseType: process.env.NUXT_ENV_OIDC_RESPONSE_TYPE || 'id_token',
        grantType: process.env.NUXT_ENV_OIDC_GRANT_TYPE || 'implicit',
        accessType: undefined,
        logoutRedirectUri: undefined,
        clientId: process.env.NUXT_ENV_CLIENT_ID,
        scope: process.env.NUXT_ENV_SCOPE ? process.env.NUXT_ENV_SCOPE.split(' ') : [],
        state: 'UNIQUE_AND_NON_GUESSABLE',
        codeChallengeMethod: process.env.NUXT_ENV_OIDC_CHALLANGE || '',
        responseMode: '',
        acrValues: ''
      }
    }
  }
}
