/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *  (UFZ, https://www.ufz.de)
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
