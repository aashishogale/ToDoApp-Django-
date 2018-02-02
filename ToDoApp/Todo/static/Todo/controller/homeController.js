var toDo = angular.module('Todo');
toDo.controller('homeController', function ($scope, restService,
	$location, $state, $uibModalStack, $uibModal) {
	$scope.gridelistDOM;
	angular.element(document).ready(function () {
		console.log("inside grid")
		$scope.gridelistDOM = $('#pinBoot').pinterest_grid({
			no_columns: 3,
			padding_x: 10,
			padding_y: 10,
			margin_bottom: 50,
			single_column_breakpoint: 700
		});
		// $scope.gridlist();
	});
	$scope.isGrid = true
	$scope.gridlist = function () {
		if ($scope.isGrid) {
			$scope.gridelistDOM.pinterest_grid1({
				no_columns: 1
			});
			$scope.isGrid=false
		}else{
			$state.reload()
			$scope.gridelistDOM.pinterest_grid({
				no_columns: 3
			});
			$scope.isGrid=true
		}
	}
	$scope.Notelist = [];
	var getallnotes = function () {
		id = localStorage.getItem("id");
		var service = restService.service('GET', 'notes');
		service.then(function (response) {
			console.log(response.data)
			$scope.Notelist = response.data;
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

	$scope.dropdown = false;
	$scope.changeClass = function () {
		$scope.showdropdown = !$scope.showdropdown;
	};

	$scope.logout = function () {
		var service = restService.service('GET', 'userlogout');
		service.then(function (response) {
			localStorage.clear();
			$state.reload();
		})

	};

	$scope.openCustomModal = function (note) {
		$scope.note = note
		$uibModal.open({
			scope: $scope,
			state: $state,
			templateUrl: '/static/Todo/templates/EditNote.html',
			parent: angular.element(document.body)

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
});
