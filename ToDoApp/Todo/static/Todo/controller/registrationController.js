var toDo = angular.module('Todo');
toDo.controller('registrationController', function($scope, restService,
		$location) {
	$scope.registerUser = function() {
		console.log($scope.user);
		var a = restService.service('POST','userregister',$scope.user);
		a.then(function(response) {

			console.log(response.data);
			console.log("inside register")
			$location.path('/login');

		}, function(response) {
			$scope.error = response.data;
		});
	}
})