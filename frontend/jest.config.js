/*
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
module.exports = {
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^~/(.*)$': '<rootDir>/$1',
    '^vue$': 'vue/dist/vue.common.js'
  },
  moduleFileExtensions: [
    'ts',
    'js',
    'vue',
    'json'
  ],
  transform: {
    '^.+\\.ts$': 'ts-jest',
    '^.+\\.js$': 'babel-jest',
    '.*\\.(vue)$': 'vue-jest'
  },
  // coverage is now off by default but can be collected by using:
  // --collectCoverage
  collectCoverage: false,
  collectCoverageFrom: [
    '<rootDir>/components/**/*.vue',
    '<rootDir>/mixins/**/*.vue',
    '<rootDir>/models/**/*.ts',
    '<rootDir>/modelUtils/**/*.ts',
    '<rootDir>/serializers/**/*.ts',
    '<rootDir>/utils/**/*.ts',
    '<rootDir>/devtools/**/*.ts',
    '<rootDir>/viewmodels/**/*.ts'
  ],
  testEnvironment: 'jsdom',
  // from the documentation:
  //
  // "After the worker has executed a test the memory usage of it is checked. If
  // it exceeds the value specified the worker is killed and restarted."
  // so we restrict the memory usage of a worker to maximum 20% of system RAM
  //
  // before it is restarted:
  workerIdleMemoryLimit: 0.2,
  // just use one worker to avoid memory problems
  maxWorkers: 1,
  verbose: true
}
