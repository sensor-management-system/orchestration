/*
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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

const matomoModule = []
if (process.env.NUXT_ENV_MATOMO_SITE_ID) {
  const config = {
    siteId: process.env.NUXT_ENV_MATOMO_SITE_ID
  }
  if (process.env.NUXT_ENV_MATOMO_URL) {
    config.matomoUrl = process.env.NUXT_ENV_MATOMO_URL
  }
  if (process.env.NUXT_ENV_MATOMO_TRACKER_URL) {
    config.trackerUrl = process.env.NUXT_ENV_MATOMO_TRACKER_URL
  }
  if (process.env.NUXT_ENV_MATOMO_SCRIPT_URL) {
    config.scriptUrl = process.env.NUXT_ENV_MATOMO_SCRIPT_URL
  }
  matomoModule.push([
    'nuxt-matomo', config
  ])
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
    version: process.env.npm_package_version,
    basePath: process.env.BASE_URL || '/',
    smsBackendUrl: process.env.SMS_BACKEND_URL || 'http://localhost:5000/rdm/svm-api/v1',
    cvBackendUrl: process.env.CV_BACKEND_URL || 'http://localhost:5001/api',
    idlSyncUrl: process.env.IDL_SYNC_URL || '',
    institute: process.env.INSTITUTE || '',
    pidBaseUrl: process.env.NUXT_ENV_PID_BASE_URL || ''
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
    '@mdi/font/css/materialdesignicons.min.css',
    '@/assets/leaflet-geosearch@2.6.0.css'
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
    'nuxt-leaflet',
    // Can be empty depending on the config
    ...matomoModule
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
  babel: {
    presets (_env, [_preset, _options]) {
      return [
        ['@nuxt/babel-preset-app', {
          loose: true,
          decoratorsBeforeExport: true
        }]
      ]
    }
  },
  /*
  ** Build configuration
  */
  build: {
  },
  router: {
    base: process.env.BASE_URL || '/',
    middleware: [
      'institute-pages',
      'login-success'
    ]
  },
  auth: {
    // load all plugins, that require the $auth instance from context
    plugins: [],
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
