var ToDo=angular.module('Todo',['ui-router'])
ToDo.config([ '$stateProvider', '$urlRouterProvider',
		function($stateProvider, $urlRouterProvider) {
            
    $urlRouterProvider.otherwise('login')       
    $stateProvider

    // HOME STATES AND NESTED VIEWS ========================================
    .state('register', {
        url: '/register',
        templateUrl: 'register.html',
        controller:'registrationController'
    })
    .state('login', {
        url: '/login',
        templateUrl: 'login.html',
        controller:'loginController'
    })
        }
    ])