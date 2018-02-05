// import { setTimeout } from "timers";

// import { request } from "http";

var toDo = angular.module('Todo');

// var sum = function(a,b,myCallback){
// 	 setTimeout(() => {
// 		if(typeof myCallback == "function")
// 			myCallback(null,a+b);
// 		else
// 			return a+b;
// 	}, 500);
// }
// var result = sum(10,20);
// console.log(result);
// sum(10,20,function(err,data){
// 	console.log(data);
// });
toDo.controller('loginController', function($scope, restService,
		$location,$auth) {
	$scope.loginUser = function() {
		console.log($scope.user);
		var service = $auth.login($scope.user) 
		//loginService.service('POST','userlogin',$scope.user);
		service.then(function(response) {

			console.log(response);
			$auth.setToken(response.data)
			// //console.log("this is "+response.data.auth_token)
			//localStorage.setItem("Token",response.data)
			localStorage.setItem("token",response.data.token)
			localStorage.setItem("Grid","grid")
			localStorage.setItem("id",response.data.id)
			localStorage.setItem("name",response.data.username)
	        $location.path('/home');

		}, function(response) {
			$scope.error = response.data;
		});
	}

	$scope.generateOtp = function() {
		console.log($scope.user);
		
		var service=restService.service('POST','generateOTP',$scope.user);
		service.then(function(response) {

			console.log(response);
			//$auth.setToken(response.data)
			// //console.log("this is "+response.data.auth_token)
			localStorage.setItem("token",response.data)
		
	        $location.path('/enterotp');

		}, function(response) {
			$scope.error = response.data;
		});
	}

	$scope.checkOtp = function() {
//		console.log($scope.user);
		
		var service=restService.service('POST','checkOTP',$scope.user);
		service.then(function(response) {

			console.log(response);
			//$auth.setToken(response.data)
			// //console.log("this is "+response.data.auth_token)
			//localStorage.setItem("token",response.data)
	        $location.path('/changepassword');

		}, function(response) {
			$scope.error = response.data;
		});
	}


	$scope.changepassword = function() {
				console.log($scope.user);
				
		var service=restService.service('POST','changepassword',$scope.user);
				service.then(function(response) {
		
					console.log(response);
					//$auth.setToken(response.data)
					// //console.log("this is "+response.data.auth_token)
					//localStorage.setItem("token",response.data)
					$location.path('/home');
		
				}, function(response) {
					$scope.error = response.data;
				});
			}
	
})