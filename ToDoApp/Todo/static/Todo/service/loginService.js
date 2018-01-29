var toDo = angular.module('Todo');

toDo.factory('loginService', function($http, $location) {

	var details = {};

	details.service = function(method, url, user) {
	
		return $http({
			method : method,
			url : url,
			data : user,
			headers:{
				token:localStorage.getItem('token')
			}
			
		})
    }
    return details
})