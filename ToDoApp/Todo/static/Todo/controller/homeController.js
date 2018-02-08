var toDo = angular.module('Todo');
toDo.controller('homeController', function ($scope, restService,
	$location, $state, $uibModalStack, $uibModal,Upload,$interval,$filter,toastr) {

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


	$scope.class1 = localStorage.getItem("archiveGrid");
	$scope.archivegridlist = function () {



		if ($scope.class1 == 'list') {
			//$scope.width="32%"
			$scope.class1 = 'grid'
		
			//$('.card').css("width", "32%");
			//$scope.isGrid = false;
			localStorage.setItem("archiveGrid", "grid")
		} else {

			//$scope.width="100%"
			$scope.class1 = 'list'
			

			
			//$('.card').css("width", "100%");
			//$scope.isGrid = true;
			localStorage.setItem("archiveGrid", "list")
		}
	}
	$scope.options = ['#FFFFFF','#FF8A80', '#FFD180', '#FFFF8D', '#CFD8DC', '#80D8FF', '#A7FFEB', '#CCFF90'];
	$scope.Notelist = [];
	$scope.pinned = '';
	$scope.others = '';
	$scope.color = '';

    $scope.colorChanged = function(newColor, oldColor,note) {
		console.log('from ', oldColor, ' to ', newColor);
		note.color=newColor

		var url = "note/" + note.id
		var service = restService.service('PUT', url,note);
		service.then(function (response) {
			$state.reload();
		})
		
    }



	$scope.getallcollaborators = function (note) {
	
		var service2 = restService.service('GET', 'collaborator', null, note.id);
		$scope.collaborators = [];
		$scope.collaborator = [];
		service2.then(function (response) {
		
			
			
			
			$scope.collaborators = response.data
		
			$scope.user={};
			for (i in $scope.collaborators) {
				$scope.user = $scope.collaborators[i];

				$scope.owner = $scope.user.owner
				console.log("owner"+$scope.owner)
				
				$scope.getuser($scope.user.shareduser)


			}
			$scope.getuser($scope.owner)

		})


	}
	
  


	$scope.getuser = function (user) {


		var url = "getuser/" + user;
		var service2 = restService.service('GET', url);
		service2.then(function (response) {
            
			$scope.collaborator.push(response.data)
			console.log("collabortorlist"+$scope.collaborator)
			
		  
		

		})

	}
	$scope.getcollabbynote =function(note){

		var id=note.id
		var url='getcollabbynote/'+id
		var service=restService.service('GET',url)
		service.then(function(response){
		note.collab=response.data;
			console.log(note)
		})
	}



	$scope.getownername = function () {
		
		$scope.ownername={}
		var url = "getuser/" + localStorage.getItem("id");
		var service2 = restService.service('GET', url);
		service2.then(function (response) {

			$scope.ownername=response.data
           $scope.note1.ownername=$scope.ownername.username
			console.log("here"+$scope.ownername.username)
		})

	}

	$scope.note={};
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
               $scope.getcollabbynote($scope.note)
			


			}
		})
	};

	$scope.collabuser = {};
	$scope.addCollaborator = function (note) {
		var collaborator = {};

		collaborator.owner = note.owner;
		
		collaborator.note = note.id;
		
		var url = "getuserbyusername/" + $scope.collabuser.username
		var service2 = restService.service('GET', url);
		service2.then(function (response) {
		
			user = {}
			user = response.data
	
			collaborator.shareduser = user.id
			
			savecollaborator(collaborator)
			$state.reload();
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
	$scope.addnote={}

	$scope.createNote = function (addnote) {
	    $scope.note1.ownername=localStorage.getItem("name")
		$scope.note1.owner = localStorage.getItem("id")
		
		$scope.note1.description = $("#description").html();
		console.log($scope.note)
		var service = restService.service('POST', 'createnote', $scope.note1);
		service.then(function (response) {
			note={};
			$state.reload();
		})
	};

	$scope.checked = "col-md-3"

	

	$scope.archiveurl = "/static/Todo/img/archive.svg";
	$scope.trashurl = "/static/Todo/img/trash.svg";
	$scope.moreurl = "/static/Todo/img/threedots.svg";
	$scope.pinurl = "/static/Todo/img/pin.svg";
	$scope.collaburl = "/static/Todo/img/colloborator.svg";
	$scope.reminderurl = "/static/Todo/img/reminder.svg";
	$scope.dropdown = false;
	$scope.changeClass = function () {
		$scope.showdropdown = !$scope.showdropdown;
	};


	$scope.changeClass1 = function () {
		$scope.showdropdown2 = !$scope.showdropdown2;
	}
	$scope.changeClass2 = function () {
		console.log("inside here")
		$scope.showdropdown3 = !$scope.showdropdown3;
	}
	$scope.logout = function () {
		var service = restService.service('GET', 'userlogout');
		service.then(function (response) {
			localStorage.clear();
			$state.reload();
		})

	};
	interVal();
					function interVal() {

						$interval(
								function() {
									var i = 0;
									for (i; i < $scope.Notelist.length; i++) {
										console.log("enter");
										console.log("reminder"
												+ $scope.Notelist[i].reminder)
										if ($scope.Notelist[i].reminder != null) {
											console
													.log("reminder"
															+ $scope.Notelist[i].reminder)
											var reminderdate = $filter('date')
													(
															$scope.Notelist[i].reminder,
															'yyyy-MM-dd HH:mm Z');
											var currentDate = $filter('date')(
													new Date(),
													'yyyy-MM-dd HH:mm Z');
											console.log("current date"
													+ currentDate);
											console.log("reminderdate"
													+ reminderdate);
											if (reminderdate === currentDate) {
												console.log("toaster exeute");
												toastr.success($scope.Notelist[i].title,'Reminder');
												return

											}
										}
									}

								}, 55000);
					}
					;

	$scope.addReminder=function(note){
		console.log(note)
		$scope.editNote(note)
	}
$scope.note={}
	$scope.editNote = function (note) {
		console.log(note)
		$scope.note.collab={}
		$scope.note.title=$(".title").html()
		$scope.note.description = $(".description").html();
		var url = "note/" + $scope.note.id
		console.log(note)
		var service = restService.service('PUT', url,note);
		service.then(function (response) {
			$state.reload();
		})

	}
	$scope.archiveNote = function (note) {
		note.isArchived = !note.isArchived
		console.log(note)
	
		var url = "note/" + note.id
		var service = restService.service('PUT', url,note);
		service.then(function (response) {
			$state.reload();
		})
	}
	$scope.pinNote = function (note) {
		note.isPinned = !note.isPinned
		$scope.editNote(note)
	}
$scope.addLabel=function(label){
	

}
$scope.getLabelForUser=function(){

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
			$scope.imageurl = 'http://127.0.0.1:8000/media/'+image.image
			console.log($scope.imageurl)
		})
	}
   $scope.getImage();
});
