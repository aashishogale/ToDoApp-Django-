var toDo = angular.module('Todo');
toDo.controller('homeController', function($scope,restService,
		$location,$state) {

    $scope.createNote=function(note){
		note.owner=localStorage.getItem("id")
		console.log(note)
		var service=restService.service('POST','createnote',note);
		service.then(function(response){
			console.log(response.data);
		    $state.reload();

		})
	};
	var getallnotes=function(){
	    id=localStorage.getItem("id");
		var service=restService.service('GET','notes');
		service.then(function(response){
			console.log(response.data)
			$scope.Notelist=response.data;

		})

	
	};

	getallnotes();

	$scope.imageurl="/static/Todo/img/polar.jpg";


	$scope.dropdown = false;
	$scope.changeClass = function(){
		$scope.showdropdown = !$scope.showdropdown;
	};

	$scope.logout=function(){
		localStorage.clear();
		$state.reload();
	};
 
})