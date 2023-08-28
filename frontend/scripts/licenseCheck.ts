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
import * as fs from 'fs'
import * as readline from 'readline'
import { glob } from 'glob'

/*******************************************************************************
 *
 * you can configure all required parameters below
 *
 ******************************************************************************/

/**
 * How many lines to check from the file, 0 means all lines are checked
 */
const MAX_LINES = 50
/**
 * The pattern to search for, must be a RegExp string
 */
const LICENSE_PATTERN = 'Licensed under the HEESIL'
/**
 * One or multiple file pattern which should be checked
 * see https://github.com/isaacs/node-glob#glob-primer
 */
const FILE_PATTERN = [
  './**/*.@(vue|ts|js)'
]
/**
 * One or multiple file pattern of files that should be ignored
 * see https://github.com/isaacs/node-glob#glob-primer
 */
const IGNORE_PATTERN = [
  './coverage/**/*',
  './dist/**/*',
  './doc/**/*',
  './docker/**/*',
  './static/**/*',
  './node_modules/**/*'
]
/**
 * The options for glob, per default only ignore is used
 */
const GLOB_OPTIONS = {
  ignore: IGNORE_PATTERN
}

/*******************************************************************************
 *
 * here we go!
 *
 ******************************************************************************/
;(async () => await main())()

/*******************************************************************************
 *
 * definitions
 *
 ******************************************************************************/

type TCheckResult = {file: string, hasLicense: boolean}

async function main () {
  // get all files that match the file pattern
  const filenameResults: string[][] = await Promise.all(
    FILE_PATTERN.map((pattern: string): Promise<string[]> => {
      // we have to wrap the callback function for glob in a promise to have it
      // under controll when it is called
      return new Promise((resolve, reject) => {
        glob(
          pattern,
          GLOB_OPTIONS,
          (error: Error | null, filenames: string[]) => error === null ? resolve(filenames) : reject(error)
        )
      })
    })
  )

  // flatten the filenames
  const filenames = filenameResults.flat()

  // check those files for the license pattern
  const checkResults: TCheckResult[] = await checkFiles(
    filenames,
    new RegExp(LICENSE_PATTERN),
    MAX_LINES
  )

  // filter only the files that have no matching license
  const results: TCheckResult[] = checkResults.filter((item: TCheckResult) => !item.hasLicense)

  // all is fine
  if (!results.length) {
    process.exit(0)
  }

  // eslint-disable-next-line
  console.info('Missing license in the following files:\n')
  // eslint-disable-next-line
  results.forEach(check => console.log('\x1b[31m', check.file))
  process.exit(1)
}

/**
 * checks a file line by line if it has a matching pattern
 *
 * @async
 * @param {string} filename - the file to check
 * @param {RegExp} searchPattern - the pattern to search for
 * @param {number} [maxLines=0] - the maximum number of lines to check
 * @return {Promise<boolean>} true when the pattern was found, otherwise false
 */
async function checkFileForPattern (filename: string, searchPattern: RegExp, maxLines: number = 0): Promise<boolean> {
  const filestream = fs.createReadStream(filename)
  const lineReader = readline.createInterface({
    input: filestream,
    crlfDelay: Infinity
  })

  let numLines: number = 0
  for await (const line of lineReader) {
    if (line.match(searchPattern)) {
      return true
    }
    numLines++
    if (maxLines && numLines === maxLines) {
      return false
    }
  }
  return false
}

/**
 * checks if a file has a valid license
 *
 * @async
 * @param {string} filename - the filename to check
 * @param {RegExp} searchPattern - the pattern to search for
 * @param {number} [maxLines=0] - the maximum number of lines to check
 * @return {Promise<TCheckResult>} the check result
 */
async function checkFile (filename: string, searchPattern: RegExp, maxLines: number = 0): Promise<TCheckResult> {
  const hasLicense: boolean = await checkFileForPattern(
    filename,
    searchPattern,
    maxLines
  )
  return {
    file: filename,
    hasLicense
  }
}

/**
 * checks if multiple files have a valid license
 * calls {@link checkFile}
 *
 * @async
 * @param {string[]} filenames - the array of filenames to check
 * @param {RegExp} searchPattern - the pattern to search for
 * @param {number} [maxLines=0] - the maximum number of lines to check
 * @return {Promise<TCheckResult[]>} an array of checks
 */
async function checkFiles (filenames: string[], searchPattern: RegExp, maxLines: number = 0): Promise<TCheckResult[]> {
  const promises: Promise<TCheckResult>[] = filenames.map(async (file) => {
    return await checkFile(file, searchPattern, maxLines)
  })
  return await Promise.all(promises)
}
