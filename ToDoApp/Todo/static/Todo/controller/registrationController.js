var toDo = angular.module('Todo');
toDo.controller('registrationController', function($scope, registerService,
		$location) {
	$scope.registerUser = function() {
		console.log($scope.user);
		var a = registerService.registerUser($scope.user);
		a.then(function(response) {

			console.log(response.data);

			$location.path('/login');

		}, function(response) {
			$scope.error = response.data;
		});
	}
})