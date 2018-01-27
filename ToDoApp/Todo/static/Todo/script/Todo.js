var app=angular.module('Todo',['ui.router','satellizer'])
console.log("entered module")
app.config([ '$stateProvider', '$urlRouterProvider',
		function($stateProvider, $urlRouterProvider,stateService) {

            var skipIfLoggedIn = ['$q', '$auth', function($q, $auth) {
                var deferred = $q.defer();
                if ($auth.isAuthenticated()) {
                  deferred.reject();
                } else {
                  deferred.resolve();
                }
                return deferred.promise;
              }];
          
              var loginRequired = ['$q', '$location', '$auth', function($q, $location, $auth) {
                var deferred = $q.defer();
                if ($auth.isAuthenticated()) {
                  deferred.resolve();
                } else {
                  $location.path('/login');
                }
                return deferred.promise;
              }];
                  
     
    $stateProvider
    .state('register', {
        url: '/register',
        templateUrl:'/static/Todo/templates/register.html' ,
        controller:'registrationController',
        resolve: {
            skipIfLoggedIn: skipIfLoggedIn
          }
    })
    .state('login', {
        url: '/login',
        templateUrl: '/static/Todo/templates/login.html',
        controller:'loginController',
        resolve: {
            skipIfLoggedIn: skipIfLoggedIn
          }
    })
    
    .state('home', {
        url: '/home',
        templateUrl: '/static/Todo/templates/home.html',
        controller:'homeController',   resolve: {
            loginRequired: loginRequired
          }
    })

    .state('/', {
        url: '/',
         resolve: {
        skipIfLoggedIn: skipIfLoggedIn
          }
    });


   $urlRouterProvider.otherwise('/home') 
        }
    ])