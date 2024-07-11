/*
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
/* eslint-disable @typescript-eslint/no-var-requires */
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
      path.join(__dirname, 'config/styleguidist/global.styles.scss'),
      path.join(__dirname, 'config/styleguidist/css/materialdesignicons@5.9.55.min.css')
    ],
    renderRootJsx: resolve(__dirname, 'config/styleguidist/styleguide.root.js'),
    webpackConfig,
    usageMode: 'expand',
    styleguideDir: 'dist',
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
