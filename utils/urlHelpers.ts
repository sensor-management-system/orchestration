export function removeBaseUrl (url: string, baseUrl: string | undefined): string {
  if (!baseUrl) {
    return url
  }
  const splitted = url.split(baseUrl)
  const canditate = splitted[splitted.length - 1]

  // now also remove a first slash if necessary, as well as a trailing slash
  return removeFirstSlash(removeTrailingSlash(canditate))
}

export function removeFirstSlash (str: string): string {
  if (str.startsWith('/')) {
    return str.substring(1)
  }
  return str
}

export function removeTrailingSlash (str: string): string {
  if (str.endsWith('/')) {
    return str.substring(0, str.length - 1)
  }
  return str
}
