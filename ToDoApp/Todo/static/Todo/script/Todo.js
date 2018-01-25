var app=angular.module('Todo',['ui.router'])
console.log("entered module")
app.config([ '$stateProvider', '$urlRouterProvider',
		function($stateProvider, $urlRouterProvider) {
                  
    $stateProvider
    .state('register', {
        url: '/register',
        templateUrl:'/static/Todo/templates/register.html' ,
        controller:'registrationController'
    })
    .state('login', {
        url: '/login',
        templateUrl: '/static/Todo/templates/login.html',
        controller:'loginController'
    })
    
    .state('home', {
        url: '/home',
        templateUrl: '/static/Todo/templates/home.html',
        controller:'homeController'
    });

    $urlRouterProvider.otherwise('/login') 
        }
    ])