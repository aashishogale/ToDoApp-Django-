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
})