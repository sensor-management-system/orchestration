/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

type ErrorPredicate = (error: any) => boolean

interface IErrorMessageDispatcherRule {
  status: number
  predicate: ErrorPredicate
  text: string
}

export class ErrorMessageDispatcher {
  private _defaultText: string = ''
  private _rules: IErrorMessageDispatcherRule[] = []

  defaultText (defaultText: string) {
    this._defaultText = defaultText
    return this
  }

  forCase (rule: IErrorMessageDispatcherRule) {
    this._rules.push(rule)
    return this
  }

  dispatch (anError: any): string {
    for (const rule of this._rules) {
      if (anError.response?.status === rule.status) {
        // JSON API error messages have an data attribute that
        // contains all the errors.
        if (anError.response?.data?.errors?.find((err: any) => rule.predicate(err))) {
          return rule.text
        }
      }
    }
    return this._defaultText
  }
}

export function sourceLowerCaseIncludes (text: string): ErrorPredicate {
  return (err: any) => err.source?.toLowerCase().includes(text)
}
