var toDo = angular.module('Todo');

toDo.factory('loginService', function($http, $location) {

	var details = {};
	
	details.service = function(method, url, user) {
		var httpobj={
			method : method,
			url : url,
		
			headers:{
				token:localStorage.getItem('token')
			}
		}
		if(method=='get'||method=='GET'){
			httpobj.params=data;
		}
		else
		{
			httpobj.data=data;
		}
		// return $http({
		// 	method : method,
		// 	url : url,
		// 	data : user,
		// 	headers:{
		// 		token:localStorage.getItem('token')
		// 	}
			
		// })

		return $http(httpobj)
    }
    return details
})