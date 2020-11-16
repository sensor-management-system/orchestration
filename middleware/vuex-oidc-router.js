export default function (context) {
  return new Promise((resolve) => {
    context.store.dispatch('oidc/oidcCheckAccess', context.route)
      .then((hasAccess) => {
        if (hasAccess) {
          resolve()
        }
      }).catch((_error) => {
      })
  })
}
