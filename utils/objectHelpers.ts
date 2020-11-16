type IObject = {[idx: string]: any}

// normally we would just the spread operator
export function mergeObjectsAndMaybeOverwrite (objects: IObject[]): IObject {
  return objects.reduce(function (r: IObject, o: IObject) {
    Object.keys(o || {}).forEach(function (k) {
      r[k] = o[k]
    })
    return r
  }, {})
}
