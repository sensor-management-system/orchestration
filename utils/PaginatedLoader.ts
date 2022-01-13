/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

// We really want to do a recursive function definition here
// eslint-disable-next-line no-use-before-define
export type PaginationLoaderFunction<E> = () => Promise<IPaginationLoader<E>>

export interface IPaginationLoader<E> {
  elements: E[]
  totalCount: number,
  funToLoadNext: null | PaginationLoaderFunction<E>
}

export class FilteredPaginationedLoader<E> implements IPaginationLoader<E> {
  private innerLoader: IPaginationLoader<E>
  private filterFunc: (x: E) => boolean

  constructor (innerLoader: IPaginationLoader<E>, filterFunc: (x: E) => boolean) {
    this.innerLoader = innerLoader
    this.filterFunc = filterFunc
  }

  get elements (): E[] {
    return this.innerLoader.elements.filter(this.filterFunc)
  }

  get totalCount (): number {
    const countThatDoesNotFulfillFilterFunc = this.innerLoader.elements.length - this.elements.length
    return this.innerLoader.totalCount - countThatDoesNotFulfillFilterFunc
  }

  get funToLoadNext (): null | PaginationLoaderFunction<E> {
    const innerPromise: null | PaginationLoaderFunction<E> = this.innerLoader.funToLoadNext
    if (innerPromise === null) {
      return null
    }

    return () => {
      return innerPromise().then((nextLoader: IPaginationLoader<E>) => {
        return new FilteredPaginationedLoader(nextLoader, this.filterFunc)
      })
    }
  }
}
