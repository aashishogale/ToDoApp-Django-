var toDo = angular.module('Todo');
toDo.controller('homeController', function ($scope, restService,
	$location, $state, $uibModalStack, $uibModal,Upload) {

	//$scope.isGrid=localStorage.getItem("Grid")
	$scope.class = localStorage.getItem("Grid");
	$scope.gridlist = function () {



		if ($scope.class == 'list') {
			//$scope.width="32%"
			$scope.class = 'grid'
			//$('.card').css("width", "32%");
			//$scope.isGrid = false;
			localStorage.setItem("Grid", "grid")
		} else {

			//$scope.width="100%"
			$scope.class = 'list'
			//$('.card').css("width", "100%");
			//$scope.isGrid = true;
			localStorage.setItem("Grid", "list")
		}
	}


	$scope.Notelist = [];
	$scope.pinned = '';
	$scope.others = '';
	

	$scope.collaborator = [];

	$scope.getallcollaborators = function (note) {


		var service2 = restService.service('GET', 'collaborator', null, note.id);

		service2.then(function (response) {
			$scope.collaborators = [];
			$scope.collaborator = [];
			$scope.owner = ''
			$scope.collaborators = response.data

			for (i in $scope.collaborators) {
				$scope.user = $scope.collaborators[i];


				$scope.getuser($scope.user.shareduser)


			}

		})


	}



	$scope.getuser = function (user) {


		var url = "getuser/" + user;
		var service2 = restService.service('GET', url);
		service2.then(function (response) {

			$scope.collaborator.push(response.data)



		})

	}



	var getallnotes = function () {
		id = localStorage.getItem("id");
		var service = restService.service('GET', 'notes');
		service.then(function (response) {
			console.log(response.data)
			$scope.Notelist = response.data;
			for (i in $scope.Notelist) {
				$scope.note = $scope.Notelist[i];

				if ($scope.note.isPinned) {
					$scope.pinned = 'Pinned';
					$scope.others = 'Others';
				}


			}
		})
	};

	$scope.collabuser = {};
	$scope.addCollaborator = function (note) {
		var collaborator = {};

		collaborator.owner = note.owner;
		collaborator.note = note.id;
		console.log("user" + $scope.collabuser.username)
		var url = "getuserbyusername/" + $scope.collabuser.username
		var service2 = restService.service('GET', url);
		service2.then(function (response) {
			console.log("response" + response.data)
			user = {}
			user = response.data
			console.log(user)
			collaborator.shareduser = user.id
			savecollaborator(collaborator)
		})

	}

	$scope.deleteCollaborator = function (note,user) {
		var collaborator = {};
        console.log(note)
		collaborator.owner = note.owner;
		collaborator.note = note.id;
		console.log("user" + $scope.collabuser.username)
		var url = "getuserbyusername/" + user.username
		var service2 = restService.service('GET', url);
		service2.then(function (response) {
			console.log("response" + response.data)
			user = {}
			user = response.data
			console.log(user)
			collaborator.shareduser = user.id
			removeCollaborator(collaborator)

		})
	}


	var removeCollaborator = function (collaborator) {
		var url = "deletecollaborator/" + collaborator.owner + "/" + collaborator.note + "/" + collaborator.shareduser
		var service2 = restService.service('GET', url);
		service2.then(function(response){
			$state.reload()
			console.log("deleted successfully")
		})
	}
	var savecollaborator = function (collaborator) {
		console.log(collaborator)
		var service2 = restService.service('POST', "collaborator", collaborator);
		service2.then(function (response) {
			console.log("collab added successfully")
		})
	}

	getallnotes();
	$scope.createNote = function (note) {
		note.owner = localStorage.getItem("id")

		note.description = $("#description").html();
		console.log(note)
		var service = restService.service('POST', 'createnote', note);
		service.then(function (response) {

			$state.reload();
		})
	};

	$scope.checked = "col-md-3"

	

	$scope.archiveurl = "/static/Todo/img/archive.svg";
	$scope.trashurl = "/static/Todo/img/trash.svg";
	$scope.moreurl = "/static/Todo/img/threedots.svg";
	$scope.pinurl = "/static/Todo/img/pin.svg";
	$scope.collaburl = "/static/Todo/img/colloborator.svg";
	$scope.dropdown = false;
	$scope.changeClass = function () {
		$scope.showdropdown = !$scope.showdropdown;
	};


	$scope.changeClass1 = function () {
		$scope.showdropdown2 = !$scope.showdropdown2;
	}

	$scope.logout = function () {
		var service = restService.service('GET', 'userlogout');
		service.then(function (response) {
			localStorage.clear();
			$state.reload();
		})

	};
	$scope.editNote = function (note) {
		note.title = $(".title").html();
		note.description = $(".description").html();
		var url = "note/" + note.id
		console.log(url)
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			$state.reload();
		})

	}
	$scope.archiveNote = function (note) {
		note.isArchived = !note.isArchived
		$scope.editNote(note)
	}
	$scope.pinNote = function (note) {
		note.isPinned = !note.isPinned
		$scope.editNote(note)
	}

	$scope.trashNote = function (note) {
		note.isTrashed = !note.isTrashed
		$scope.editNote(note)
	}

	$scope.openCustomModal = function (note) {
		console.log("inside modal")
		$scope.note = note

		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/EditNote.html',
			scope: $scope,




		}).result.then(function () {
		}, function (res) {
		});

	}


	$scope.opencollaborators = function (note) {
		console.log("inside modal")
		$scope.note = note

		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/collabmodal.html',
			scope: $scope,






		}).result.then(function () {
		}, function (res) {
		});

	}


	var trigger = $('.hamburger'),
		overlay = $('.overlay'),
		isClosed = false;

	trigger.click(function () {
		hamburger_cross();
	});

	function hamburger_cross() {

		if (isClosed == true) {
			overlay.hide();
			trigger.removeClass('is-open');
			trigger.addClass('is-closed');
			isClosed = false;
		} else {
			overlay.show();
			trigger.removeClass('is-closed');
			trigger.addClass('is-open');
			isClosed = true;
		}
	}

	$('[data-toggle="offcanvas"]').click(function () {
		$('#wrapper').toggleClass('toggled');
	});

	// 
	// 
	// 

	$scope.upload = function (file) {
		Upload.upload({
			
			url: 'addimage',
			data: { file: file ,owner:localStorage.getItem('id'),
				headers:{
				token:localStorage.getItem('token'),
				id:localStorage.getItem('id'),
				
				'Cache-Control' : 'no-cache'
				
			
			}
		}

		}).then(function (resp) {
			console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
		
    //  data={
	// 	 'image':file,
	// 	 'owner':localStorage.getItem('id')
	//  }
	// var service=restService.service('POST','addimage',data);
	// 	service.then(function(response){
	// 	console.log(response.data)
    //     console.log("this is done")
	// })
	
	
		});

	};


	$scope.getImage =function(){
		var url="getimage/"+localStorage.getItem("id")
		var service=restService.service('GET',url)
		service.then(function(response){
			console.log(response.data)
			var image=response.data
			console.log(image)
			$scope.imageurl = 'file://'+image.image
			console.log($scope.imageurl)
		})
	}
   $scope.getImage();
});
