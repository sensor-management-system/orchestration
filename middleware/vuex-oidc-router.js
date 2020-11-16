export default function (context) {
  // We call this function every time we change the routes of our pages.
  // We use it here to prevent unauthorized access to our routes.
  // Basically we ask our Open ID Connect store if the user is allowed
  // to access our route.
  // Otherwise we redirect to the a plain page.
  return new Promise((resolve) => {
    const redirect = (textToDisplay) => {
      if (textToDisplay) {
        context.store.commit('snackbar/setError', textToDisplay)
      }
      const indexPage = '/'
      return context.redirect(indexPage)
    }

    const accessPromise = context.store.dispatch('oidc/oidcCheckAccess', context.route)

    accessPromise.then((hasAccess) => {
      if (hasAccess) {
        // ok, we don't need to change anything
        resolve(true)
      } else {
        resolve(redirect('Unauthorized'))
      }
    }).catch((error) => {
      resolve(redirect(error))
    })
  })
}
