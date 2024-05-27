/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export const getParentByClass = (elem: Element, classNames: string[]): Element | null => {
  const parentElem: Element | null = elem.parentElement
  if (!parentElem) {
    return null
  }
  if (classNames.every(className => parentElem.classList.contains(className))) {
    return parentElem
  }
  if (parentElem.tagName.toUpperCase() === 'DOCUMENT') {
    return null
  }
  return getParentByClass(parentElem, classNames)
}
