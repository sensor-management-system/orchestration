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
