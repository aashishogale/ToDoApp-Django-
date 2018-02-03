var toDo = angular.module('Todo');

toDo.factory('restService', function($http, $location) {

	var details = {};
	
	details.service = function(method, url, data) {
		console.log("this url is hit" +url);
		console.log(data)
	
		var httpobj={
			method : method,
			url : url,
		
			headers:{
				token:localStorage.getItem('token'),
				id:localStorage.getItem('id'),
				'Cache-Control' : 'no-cache'
				
			
			}
		}
		if(method=='get'||method=='GET'){
			console.log("inside here");
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