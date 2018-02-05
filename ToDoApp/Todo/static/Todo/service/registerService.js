
var toDo = angular.module('Todo');

toDo.factory('registerService', function($http, $location) {

	var details = {};
	details.registerUser = function(user) {
		return $http({
			method : 'POST',
			url : 'userregister',
			data : user
		})
	}
	return details;

});