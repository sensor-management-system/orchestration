import Vue from 'vue'

/**
 * returns a default string when value is empty
 *
 * @param {string} value - the string
 * @param {string} [defaultValue] - a default string, defaults to '-'
 * @returns {string} the string or the default, if the string is empty
 */
Vue.filter('orDefault', (value: string, defaultValue: string = '—'): string => {
  return value || defaultValue
})
