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

import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

describe('ErrorMessageDispatcher', () => {
  describe('#dispatch', () => {
    it('should return the specific message for the matching case', () => {
      const msg = new ErrorMessageDispatcher()
        .forCase({
          // 409 is a conflict
          status: 409,
          // and a message with mail as source of the error points
          // to our unique constraint
          predicate: sourceLowerCaseIncludes('mail'),
          text: 'User with E-mail exists already'
        })
        .defaultText('Creation of contact failed')
        .dispatch({
          response: {
            status: 409,
            data: {
              errors: [
                {
                  source: 'unqiue mail'
                }
              ]
            }
          }
        })

      expect(msg).toEqual('User with E-mail exists already')
    })

    it('should return the default message for no matching case', () => {
      const msg = new ErrorMessageDispatcher()
        .forCase({
          // 409 is a conflict
          status: 409,
          // and a message with mail as source of the error points
          // to our unique constraint
          predicate: sourceLowerCaseIncludes('mail'),
          text: 'User with E-mail exists already'
        })
        .defaultText('Creation of contact failed')
        .dispatch({
          response: {
            status: 409,
            data: {
              errors: [
                {
                  source: 'something else'
                }
              ]
            }
          }
        })

      expect(msg).toEqual('Creation of contact failed')
    })
  })
})
