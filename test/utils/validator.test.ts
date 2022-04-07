/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021, 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
import Validator from '@/utils/validator'

const isValidEmailAddress = Validator.isValidEmailAddress

describe('#isValidEmailAddress()', () => {
  it('should return true with an valid email address', () => {
    const email = 'john.doe@gfz-potsdam.de'
    expect(isValidEmailAddress(email)).toBeTruthy()
  })
  it('should return true with some more interesting email addresses', () => {
    // bob@⚔️.gg
    const email1 = 'xn--bob@-y13b.gg'
    expect(isValidEmailAddress(email1)).toBeTruthy()

    // max@müller.de
    const email2 = 'xn--max@mller-u9a.de'
    expect(isValidEmailAddress(email2)).toBeTruthy()
  })
  it('should return true with an valid email address with subdomains', () => {
    const email = 'john.doe@mail.gfz-potsdam.de'
    expect(isValidEmailAddress(email)).toBeTruthy()
  })
  it('should return false with invalid TLD', () => {
    const email1 = 'john.doe@gfz-potsdam'
    expect(typeof isValidEmailAddress(email1)).toBe('string')

    const email2 = 'john.doe@gfz-potsdam.'
    expect(typeof isValidEmailAddress(email2)).toBe('string')

    const email3 = 'john.doe@gfz-potsdam.d'
    expect(typeof isValidEmailAddress(email3)).toBe('string')
  })
  it('should return false with invalid domain', () => {
    const email1 = 'john.doe@.de'
    expect(typeof isValidEmailAddress(email1)).toBe('string')

    const email2 = 'john.doe@-.de'
    expect(typeof isValidEmailAddress(email2)).toBe('string')
  })
  it('should return false with no recipent', () => {
    const email1 = '@gfz-potsdam.de'
    expect(typeof isValidEmailAddress(email1)).toBe('string')
  })
})
