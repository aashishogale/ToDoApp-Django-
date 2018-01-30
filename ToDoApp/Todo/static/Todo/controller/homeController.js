var toDo = angular.module('Todo');
toDo.controller('homeController', function($scope, homeService,
		$location) {
	var getUser = function() {
		//console.log($scope.user);
		var service = homeService.service('POST','getuser');
		service.then(function(response) {

			console.log(response.data);
		

	        

		}, function(response) {
			$scope.error = response.data;
		});
	}
	$scope.imageurl="/static/Todo/img/polar.jpg"
	getUser()
})