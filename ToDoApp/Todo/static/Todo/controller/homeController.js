var toDo = angular.module('Todo');
toDo.controller('homeController', function ($scope, restService,
	$location, $state, $uibModalStack, $uibModal) {

		//$scope.isGrid=localStorage.getItem("Grid")
		console.log($scope.isGrid)
		$scope.class=localStorage.getItem("Grid");
	$scope.gridlist = function () {
		
		

		if ($scope.class=='list') {
			console.log("is Grid");
			//$scope.width="32%"
			$scope.class='grid'
			//$('.card').css("width", "32%");
			//$scope.isGrid = false;
			localStorage.setItem("Grid","grid")
		} else {
			console.log("is not Grid");
			//$scope.width="100%"
			$scope.class='list'
			//$('.card').css("width", "100%");
			//$scope.isGrid = true;
			localStorage.setItem("Grid","list")
		}
	}
  
	
	$scope.Notelist = [];
	$scope.pinned='';
	$scope.others='';

	var getallnotes = function () {
		id = localStorage.getItem("id");
		var service = restService.service('GET', 'notes');
		service.then(function (response) {
			console.log(response.data)
			$scope.Notelist = response.data;
			for(i in $scope.Notelist){
		var note=$scope.Notelist[i];
		if(note.isPinned){
			$scope.pinned='Pinned';
			$scope.others='Others';
		}
	
		}
			console.log($scope.Notelist)
		})
	};

	getallnotes();
	$scope.createNote = function (note) {
		note.owner = localStorage.getItem("id")

		note.description = $("#description").html();
		console.log(note)
		var service = restService.service('POST', 'createnote', note);
		service.then(function (response) {
			console.log(response.data);

			$state.reload();
		})
	};

	$scope.checked = "col-md-3"

	$scope.imageurl = "/static/Todo/img/polar.jpg";

	$scope.archiveurl = "/static/Todo/img/archive.svg";
	$scope.trashurl = "/static/Todo/img/trash.svg";
	$scope.moreurl= "/static/Todo/img/threedots.svg";
	$scope.pinurl = "/static/Todo/img/pin.svg";
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
		note.title= $(".title").html();
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
		url: 'upload/url',
		data: {file: file}
	}).then(function (resp) {
		console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
	}, function (resp) {
		console.log('Error status: ' + resp.status);
	}, function (evt) {
		var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
		console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
	});
};





});
