/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
const { resolve } = require('path')
const path = require('path')
const { getWebpackConfig } = require('nuxt')

const FILTERED_PLUGINS = [
  'WebpackBarPlugin',
  'VueSSRClientPlugin',
  'HotModuleReplacementPlugin',
  'FriendlyErrorsWebpackPlugin',
  'HtmlWebpackPlugin'
]

/** @type import("vue-styleguidist").Config */
module.exports = async () => {
  // get the webpack config directly from nuxt
  const nuxtWebpackConfig = await getWebpackConfig('client', {
    for: 'dev'
  })

  const webpackConfig = {
    module: {
      rules: [
        ...nuxtWebpackConfig.module.rules.filter(
          // remove the eslint-loader
          a => a.loader !== 'eslint-loader'
        )
      ]
    },
    resolve: { ...nuxtWebpackConfig.resolve },
    plugins: [
      ...nuxtWebpackConfig.plugins.filter(
        // And some other plugins that could conflcit with ours
        p => !FILTERED_PLUGINS.includes(p.constructor.name)
      )
    ]
  }

  return {
    require: [
      path.join(__dirname, 'config/styleguidist/global.requires.js'),
      path.join(__dirname, 'config/styleguidist/global.styles.scss')
    ],
    renderRootJsx: resolve(__dirname, 'config/styleguidist/styleguide.root.js'),
    webpackConfig,
    usageMode: 'expand',
    styleguideDir: 'dist',
    template: {
      head: {
        links: [
          {
            rel: 'stylesheet',
            href:
              'https://cdn.jsdelivr.net/npm/@mdi/font@5.9.55/css/materialdesignicons.min.css'
          }
        ]
      }
    },
    sections: [
      {
        name: 'Generic Components',
        description: 'Components that are used throughout the project.',
        components: './components/[A-Z]*.vue'
      },
      {
        name: 'Actions',
        description: 'Action-related components.',
        components: './components/actions/[A-Z]*.vue'
      },
      {
        name: 'Pages',
        description: 'Pages of the application.',
        components: './pages/*.vue',
        sections: [
          {
            name: 'Configurations',
            components: './pages/configurations/*.vue'
          },
          {
            name: 'Contacts',
            components: './pages/contacts/*.vue',
            sections: [{
              name: '_contactId',
              components: './pages/contacts/_contactId/*.vue'
            }]
          },
          {
            name: 'Devices',
            components: './pages/devices/*.vue',
            sections: [{
              name: '_deviceId',
              components: './pages/devices/_deviceId/*.vue',
              sections: [
                {
                  name: 'Actions',
                  components: './pages/devices/_deviceId/actions/*.vue',
                  sections: [
                    {
                      name: 'Edit Device Calibration Actions',
                      components: './pages/devices/_deviceId/actions/device-calibration-actions/_actionId/edit.vue'
                    }, {
                      name: 'Edit Generic Device Actions',
                      components: './pages/devices/_deviceId/actions/generic-device-actions/_actionId/edit.vue'
                    },
                    {
                      name: 'Edit Software Update Actions',
                      components: './pages/devices/_deviceId/actions/software-update-actions/_actionId/edit.vue'
                    }
                  ]
                },
                {
                  name: 'Attachments',
                  components: './pages/devices/_deviceId/attachments/*.vue',
                  sections: [{
                    name: 'Edit Attachments',
                    components: './pages/devices/_deviceId/attachments/_attachmentId/edit.vue'
                  }]
                },
                {
                  name: 'Basic',
                  components: './pages/devices/_deviceId/basic/*.vue'
                },
                {
                  name: 'Contacts',
                  components: './pages/devices/_deviceId/contacts/*.vue'
                },
                {
                  name: 'Custom Fields',
                  components: './pages/devices/_deviceId/customfields/*.vue',
                  sections: [{
                    name: 'Edit Custim Fields',
                    components: './pages/devices/_deviceId/customfields/_customfieldId/edit.vue'
                  }]
                },
                {
                  name: 'Edit Measured Quantities',
                  components: './pages/devices/_deviceId/measuredquantities/_measuredquantityId/edit.vue'
                }
              ]
            }]
          },
          {
            name: 'Platforms',
            components: './pages/platforms/*.vue',
            sections: [
              {
                name: '_platformId',
                components: './pages/platforms/_platformId/*.vue',
                sections: [
                  {
                    name: 'Actions',
                    components: './pages/platforms/_platformId/actions/*.vue',
                    sections: [
                      {
                        name: 'Edit Generic Platform Actions',
                        components: './pages/platforms/_platformId/actions/generic-platform-actions/_actionId/edit.vue'
                      },
                      {
                        name: 'Edit Software Update Actions',
                        components: './pages/platforms/_platformId/actions/software-update-actions/_actionId/edit.vue'
                      }
                    ]
                  },
                  {
                    name: 'Attachments',
                    components: './pages/platforms/_platformId/attachments/*.vue',
                    sections: [{
                      name: 'Edit Attachments',
                      components: './pages/platforms/_platformId/attachments/_attachmentId/edit.vue'
                    }]
                  },
                  {
                    name: 'Basic',
                    components: './pages/platforms/_platformId/basic/*.vue'
                  },
                  {
                    name: 'Contacts',
                    components: './pages/platforms/_platformId/contacts/*.vue'
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
