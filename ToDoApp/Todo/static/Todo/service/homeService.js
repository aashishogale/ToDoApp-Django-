var toDo = angular.module('Todo');

toDo.factory('homeService', function($http, $location) {

	var details = {};

	details.service = function(method, url, user) {
		return $http({
			method : method,
			url : url,
			headers:{

			
            token:localStorage.getItem("Token")
			}
			
		})
    }
    return details
})