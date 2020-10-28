export default function (context) {
  return new Promise((resolve, reject) => {
    context.store.dispatch('oidc/oidcCheckAccess', context.route)
           .then((hasAccess) => {
             console.log('hasAccess',hasAccess);
             if (hasAccess) {
               resolve()
             }
           })
           .catch(() => {
           })
  })
}

