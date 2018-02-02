var toDo = angular.module('Todo');
toDo.controller('homeController', function($scope,restService,
		$location,$state) {

	$scope.Notelist=[];		
	var getallnotes=function(){
		id=localStorage.getItem("id");
		var service=restService.service('GET','notes');
		service.then(function(response){
			console.log(response.data)
			$scope.Notelist=response.data;
			console.log($scope.Notelist)
		})
	};

    getallnotes();
    $scope.createNote=function(note){
		note.owner=localStorage.getItem("id")
	
		note.description=$("#description").html();
		console.log(note)
		var service=restService.service('POST','createnote',note);
		service.then(function(response){
			console.log(response.data);
			
		    $state.reload();
		})
	};

    $scope.checked="col-md-3"

	$scope.imageurl="/static/Todo/img/polar.jpg";

	$scope.dropdown = false;
	$scope.changeClass = function(){
		$scope.showdropdown = !$scope.showdropdown;
	};

	$scope.logout=function(){
		var service=restService.service('GET','userlogout');
		service.then(function(response){
			localStorage.clear();
			$state.reload();
		})
	
	};

	$scope.openCustomModal = function(note) {
		$scope.note = note
		$uibModal.open({
			scope : $scope,
			state : $state,
			templateUrl : 'template/EditNote.html',
			parent : angular.element(document.body)

		}).result.then(function() {
		}, function(res) {
		});

	}
 
})