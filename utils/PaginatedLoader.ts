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

  get elements () : E[] {
    return this.innerLoader.elements.filter(this.filterFunc)
  }

  get totalCount (): number {
    const countThatDoesNotFulfillFilterFunc = this.innerLoader.elements.length - this.elements.length
    return this.innerLoader.totalCount - countThatDoesNotFulfillFilterFunc
  }

  get funToLoadNext () : null | PaginationLoaderFunction<E> {
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
