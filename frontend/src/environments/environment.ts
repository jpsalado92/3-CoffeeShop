export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'toblerone.eu', // the auth0 domain prefix
    audience: 'CShop', // the audience set for the auth0 app
    clientId: 'shxcb6XA4Z0XKQ0K6S7Qc6ajCkQSKD3L', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
