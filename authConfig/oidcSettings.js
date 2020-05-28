import {WebStorageStateStore} from "oidc-client";

export default {
  userStore: new WebStorageStateStore({store: window.localStorage}),
  authority: 'https://webapp.ufz.de/idp/oidc/v1',
  client_id: 'oidc-test-implicit-flow-client-1',
  redirect_uri: 'https://localhost.localdomain:3000/login-callback',
  response_type: 'id_token',
  scope: 'openid profile email',
  post_logout_redirect_uri: 'https://localhost.localdomain:3000/logout-callback',
  filterProtocolClaims: 'true',
  automaticSilentRenew: 'false',
  silent_redirect_uri: 'https://localhost.localdomain:3000/silent-callback',
  includeIdTokenInSilentRenew: 'false',
  popupWindowFeatures: 'location=no,toolbar=no,width=500,height=600,left=100,top=100' //adjusted height
};

