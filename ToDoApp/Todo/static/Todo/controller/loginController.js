var toDo = angular.module('Todo');
toDo.controller('loginController', function($scope, loginService,
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
	        $location.path('/home');

		}, function(response) {
			$scope.error = response.data;
		});
	}

	$scope.generateOtp = function() {
		console.log($scope.user);
		
		var service=loginService.service('POST','generateOTP',$scope.user);
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
		
		var service=loginService.service('POST','checkOTP',$scope.user);
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
				
		var service=loginService.service('POST','changepassword',$scope.user);
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