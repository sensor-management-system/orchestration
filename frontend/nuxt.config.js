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

// Env variable definition

const NUXT_ENV_OIDC_REFRESH_TOKEN = process.env.NUXT_ENV_OIDC_REFRESH_TOKEN || 'NUXT_ENV_OIDC_REFRESH_TOKEN_ENV_PLACEHOLDER'
const NUXT_ENV_OIDC_REFRESH_EXPIRE = process.env.NUXT_ENV_OIDC_REFRESH_EXPIRE || 'NUXT_ENV_OIDC_REFRESH_EXPIRE_ENV_PLACEHOLDER'
const NUXT_ENV_OIDC_RESPONSE_TYPE = process.env.NUXT_ENV_OIDC_RESPONSE_TYPE || 'NUXT_ENV_OIDC_RESPONSE_TYPE_ENV_PLACEHOLDER'
const NUXT_ENV_OIDC_GRANT_TYPE = process.env.NUXT_ENV_OIDC_GRANT_TYPE || 'NUXT_ENV_OIDC_GRANT_TYPE_ENV_PLACEHOLDER'
const NUXT_ENV_CLIENT_ID = process.env.NUXT_ENV_CLIENT_ID || 'NUXT_ENV_CLIENT_ID_ENV_PLACEHOLDER'
const NUXT_ENV_SCOPE = process.env.NUXT_ENV_SCOPE || 'NUXT_ENV_SCOPE_ENV_PLACEHOLDER'
const NUXT_ENV_OIDC_CHALLANGE = process.env.NUXT_ENV_OIDC_CHALLANGE || 'NUXT_ENV_OIDC_CHALLANGE_ENV_PLACEHOLDER'
const NUXT_ENV_OIDC_WELL_KNOWN = process.env.NUXT_ENV_OIDC_WELL_KNOWN || 'NUXT_ENV_OIDC_WELL_KNOWN_ENV_PLACEHOLDER'

const BASE_URL = process.env.BASE_URL || 'BASE_URL_ENV_PLACEHOLDER'
const SMS_FRONTEND_URL = process.env.SMS_FRONTEND_URL || 'SMS_FRONTEND_URL_ENV_PLACEHOLDER'
const SMS_BACKEND_URL = process.env.SMS_BACKEND_URL || 'SMS_BACKEND_URL_ENV_PLACEHOLDER'
const CV_BACKEND_URL = process.env.CV_BACKEND_URL || 'CV_BACKEND_URL_ENV_PLACEHOLDER'
const IDL_SYNC_URL = process.env.IDL_SYNC_URL || 'IDL_SYNC_URL_ENV_PLACEHOLDER'
const INSTITUTE = process.env.INSTITUTE || 'INSTITUTE_ENV_PLACEHOLDER'
const NUXT_ENV_PID_BASE_URL = process.env.NUXT_ENV_PID_BASE_URL || 'NUXT_ENV_PID_BASE_URL_ENV_PLACEHOLDER'

const NUXT_ENV_MATOMO_SITE_ID = process.env.NUXT_ENV_MATOMO_SITE_ID || 'NUXT_ENV_MATOMO_SITE_ID_ENV_PLACEHOLDER'
const NUXT_ENV_MATOMO_URL = process.env.NUXT_ENV_MATOMO_URL || 'NUXT_ENV_MATOMO_URL_ENV_PLACEHOLDER'
const NUXT_ENV_MATOMO_TRACKER_URL = process.env.NUXT_ENV_MATOMO_TRACKER_URL || 'NUXT_ENV_MATOMO_TRACKER_URL_ENV_PLACEHOLDER'
const NUXT_ENV_MATOMO_SCRIPT_URL = process.env.NUXT_ENV_MATOMO_SCRIPT_URL || 'NUXT_ENV_MATOMO_SCRIPT_URL_ENV_PLACEHOLDER'

const NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME = process.env.NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME || 'NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME_ENV_PLACEHOLDER'

const NUXT_ENV_ALLOWED_MIMETYPES = process.env.NUXT_ENV_ALLOWED_MIMETYPES || 'NUXT_ENV_ALLOWED_MIMETYPES_ENV_PLACEHOLDER'

const server = {
  port: 3000,
  host: '0.0.0.0'
}

const matomoModule = []
if (NUXT_ENV_MATOMO_SITE_ID) {
  const config = {
    siteId: NUXT_ENV_MATOMO_SITE_ID
  }
  if (NUXT_ENV_MATOMO_URL) {
    config.matomoUrl = NUXT_ENV_MATOMO_URL
  }
  if (NUXT_ENV_MATOMO_TRACKER_URL) {
    config.trackerUrl = NUXT_ENV_MATOMO_TRACKER_URL
  }
  if (NUXT_ENV_MATOMO_SCRIPT_URL) {
    config.scriptUrl = NUXT_ENV_MATOMO_SCRIPT_URL
  }
  matomoModule.push([
    'nuxt-matomo', config
  ])
}

let faviconHref = `${BASE_URL + '/'}favicon.ico`
if (BASE_URL && BASE_URL.endsWith('/')) {
  faviconHref = BASE_URL + 'favicon.ico'
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
    basePath: BASE_URL,
    smsFrontendUrl: SMS_FRONTEND_URL,
    smsBackendUrl: SMS_BACKEND_URL,
    cvBackendUrl: CV_BACKEND_URL,
    idlSyncUrl: IDL_SYNC_URL,
    institute: INSTITUTE,
    pidBaseUrl: NUXT_ENV_PID_BASE_URL,
    refreshInterval: NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME,
    allowedMimeTypesString: NUXT_ENV_ALLOWED_MIMETYPES
  },
  /*
  ** Headers of the page
  */
  head: {
    title: 'Sensor Management System',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'An application to help scientists and technicans to manage sensors, measurement setups and campaigns.' },
      { name: 'og:title', property: 'og:title', content: 'Sensor Management System' },
      { name: 'og:site_name', property: 'og:site_name', content: 'Sensor Management System' },
      { name: 'apple-mobile-web-app-title', content: 'Sensor Management System' },
      { name: 'og-image', content: '/logos/ufz-sms_logo_name+abkuerzung_primaer.png' },
      { name: 'og:description', property: 'og:description', content: 'An application to help scientists and technicans to manage sensors, measurement setups and campaigns.' }

    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: faviconHref }
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
    base: BASE_URL,
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
        scheme: '~/config/auth/schemes/customOIDCScheme',
        endpoints: {
          configuration: NUXT_ENV_OIDC_WELL_KNOWN,
          logout: false
        },
        token: {
          property: 'access_token',
          type: 'Bearer',
          maxAge: 3600
        },
        refreshToken: {
          property: NUXT_ENV_OIDC_REFRESH_TOKEN,
          // GFZ Refresh token refresh time is not fetched from the server response.
          // This leads us into setting this time via env variable
          maxAge: NUXT_ENV_OIDC_REFRESH_EXPIRE
        },
        responseType: NUXT_ENV_OIDC_RESPONSE_TYPE,
        grantType: NUXT_ENV_OIDC_GRANT_TYPE,
        accessType: undefined,
        logoutRedirectUri: undefined,
        clientId: NUXT_ENV_CLIENT_ID,
        scope: NUXT_ENV_SCOPE,
        state: 'UNIQUE_AND_NON_GUESSABLE',
        codeChallengeMethod: NUXT_ENV_OIDC_CHALLANGE,
        responseMode: '',
        acrValues: ''
      }
    }
  }
}
