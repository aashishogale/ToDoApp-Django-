var toDo = angular.module('Todo');
toDo.controller('loginController', function($scope, loginService,
		$location) {
	$scope.loginUser = function() {
		console.log($scope.user);
		var service = loginService.service('POST','userlogin',$scope.user);
		service.then(function(response) {

			console.log(response.data);
			console.log("this is "+response.data.auth_token)
			localStorage.setItem("Token",response.data.auth_token)
	        $location.path('/home');

		}, function(response) {
			$scope.error = response.data;
		});
	}
})