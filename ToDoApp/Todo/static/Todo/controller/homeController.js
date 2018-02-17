var toDo = angular.module('Todo');
toDo.controller('homeController', function ($scope, restService,
	$location, $state, $uibModalStack, $uibModal, Upload, $interval, $filter, toastr) {


	// $scope.archiveurl = "/static/Todo/img/archive.svg";
	// $scope.trashurl = "/static/Todo/img/trash.svg";
	// $scope.moreurl = "/static/Todo/img/threedots.svg";
	// $scope.pinurl = "/static/Todo/img/pin.svg";
	// $scope.collaburl = "/static/Todo/img/colloborator.svg";
	// $scope.reminderurl = "/static/Todo/img/reminder.svg";
	// $scope.cancelurl = "/static/Todo/img/cancel.svg";
	// $scope.checkurl = "/static/Todo/img/check.svg";
	// $scope.pictureurl = "/static/Todo/img/picture.svg";

	$scope.note1 = {};
	//$scope.isGrid=localStorage.getItem("Grid")
	$scope.nameofuser = localStorage.getItem('name')
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

	$scope.class2 = localStorage.getItem("trashGrid");
	$scope.archivegridlist = function () {



		if ($scope.class2 == 'list') {
			//$scope.width="32%"
			$scope.class2 = 'grid'

			//$('.card').css("width", "32%");
			//$scope.isGrid = false;
			localStorage.setItem("trashGrid", "grid")
		} else {

			//$scope.width="100%"
			$scope.class2 = 'list'



			//$('.card').css("width", "100%");
			//$scope.isGrid = true;
			localStorage.setItem("trashGrid", "list")
		}
	}
	$scope.options = ['#FFFFFF', '#FF8A80', '#FFD180', '#FFFF8D', '#CFD8DC', '#80D8FF', '#A7FFEB', '#CCFF90'];
	$scope.Notelist = [];
	$scope.pinned = '';
	$scope.others = '';
	$scope.color = '';

	$scope.colorChanged = function (newColor, oldColor, note) {
		console.log('from ', oldColor, ' to ', newColor);
		note.color = newColor

		var url = "note/" + note.id
		note.collab = {}
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			toastr.success('color changed')
			$state.reload();
		})

	}



	$scope.getallcollaborators = function (note) {

		var service2 = restService.service('GET', 'collaborator', null, note.id);
		$scope.collaborators = [];
		$scope.collaborator = [];
		service2.then(function (response) {




			$scope.collaborators = response.data

			$scope.user = {};
			for (i in $scope.collaborators) {
				$scope.user = $scope.collaborators[i];

				$scope.owner = $scope.user.owner
				console.log("owner" + $scope.owner)

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
			console.log("collabortorlist" + $scope.collaborator)




		})

	}
	$scope.getcollabbynote = function (note) {

		var id = note.id
		var url = 'getcollabbynote/' + id
		var service = restService.service('GET', url)
		service.then(function (response) {
			note.collab = response.data;
			console.log(note)
		})
	}



	$scope.getownername = function () {

		$scope.ownername = {}
		var url = "getuser/" + localStorage.getItem("id");
		var service2 = restService.service('GET', url);
		service2.then(function (response) {

			$scope.ownername = response.data
			$scope.note1.ownername = $scope.ownername.username
			console.log("here" + $scope.ownername.username)
		})

	}

	$scope.note = {};
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
				$scope.getLabelForNote($scope.note)


			}
		})
	};

	$scope.collabuser = {};
	$scope.addCollaborator = function (note) {
		console.log(note)
		if ($scope.collabuser.username != localStorage.getItem('name')) {
			var collaborator = {};

			collaborator.owner = note.owner;

			collaborator.note = note.id;

			var url = "getuserbyusername/" + $scope.collabuser.username
			var service2 = restService.service('GET', url);
			service2.then(function (response) {

				user = {}
				user = response.data

				collaborator.shareduser = user.id
				if ($scope.containsObject(user, $scope.note.collab) == false) {
					savecollaborator(collaborator)
				}

				else {
					toastr.error("collaborator already exists");



				}

			})
		}

		else {
			toastr.error("cannot enter owner");



		}

	}
	$scope.containsObject = function (obj, list) {
		var i;
		for (i = 0; i < list.length; i++) {
			if (angular.equals(list[i], obj)) {
				return true;
			}
		}

		return false;
	};
	$scope.deleteCollaborator = function (note, user) {
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
		service2.then(function (response) {
			$state.reload()
			toastr.success('deleted successfully')
			console.log("deleted successfully")
		})
	}
	var savecollaborator = function (collaborator) {
		console.log(collaborator)
		var service2 = restService.service('POST', "collaborator", collaborator);
		service2.then(function (response) {
			toastr.success("collab added successfully")
			console.log("collab added successfully")
			$state.reload();
		})
	}

	//getallnotes();
	$scope.addnote = {}
	$scope.deleteNote = function (note) {
		var url = "note/" + note.id
		console.log(note)
		var service = restService.service('DELETE', url, note);
		service.then(function (response) {
			$state.reload();
			toastr.success("Note deleted Successfully")

		})

	}
	$scope.createNote = function (addnote) {
		$scope.note1.ownername = localStorage.getItem("name")
		$scope.note1.owner = localStorage.getItem("id")

		$scope.note1.description = $("#description").html();
		console.log($scope.note)
		var service = restService.service('POST', 'createnote', $scope.note1);
		service.then(function (response) {
			toastr.success("Note Added Successfully")
			$scope.note1 = {};
			$state.reload();
		})
	};

	$scope.checked = "col-md-3"



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
			$state.go('login');
		})

	};
	interVal();
	function interVal() {

		$interval(
			function () {
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
							// console.log("toaster exeute");
							// toastr.success($scope.Notelist[i].title, 'Reminder');
							Push.Permission.GRANTED;
							Push.create("reminder", {
								body: $scope.Notelist[i].title,
								icon: $scope.imageurl,
								timeout: 4000,
								onClick: function () {
									window.focus();
									this.close();
								}
							});

						}
					}
				}

			}, 55000);
	}
	;

	$scope.addReminder = function (note) {
		console.log(note)
		note.collab = {}
		note.labelString = {}
		var url = "note/" + note.id
		console.log(note)
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			$state.reload();
		})
	}
	$scope.note = {}
	$scope.editNote = function (note) {
		console.log(note)
		$scope.note.collab = {}
		$scope.note.title = $(".title").html()
		$scope.note.description = $(".description").html();
		var url = "note/" + $scope.note.id
		console.log(note)
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			$state.reload();
			toastr.success("Note Edited Successfully")

		})

	}
	$scope.archiveNote = function (note) {
		note.isArchived = !note.isArchived
		console.log(note)
		note.collab = {}
		note.labelString = {}
		note.isTrashed = false
		note.isPinned = false
		var url = "note/" + note.id
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			toastr.success("Note Archived Successfully")

			$state.reload();
		})
	}
	$scope.pinNote = function (note) {
		note.isPinned = !note.isPinned
		note.collab = {}
		note.labelString = {}
		note.isArchived = false
		note.isTrashed = false
		var file = new File([note.photo], "note.photourl");
		$scope.file;
		var url = "note/" + note.id
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			$state.reload();
			toastr.success("Note Pinned Successfully")

		})

	}




	$scope.trashNote = function (note) {
		note.isTrashed = !note.isTrashed
		note.collab = {}
		note.labelString = {}
		note.isArchived = false
		note.isPinned = false
		var url = "note/" + note.id
		var service = restService.service('PUT', url, note);
		service.then(function (response) {
			$state.reload();
			toastr.success("Note Trashed Successfully")

		})
	}

	$scope.openCustomModal = function (note) {
		console.log("inside modal")

		$scope.note = note
		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/EditNote.html',
			scope: $scope,
			windowClass: 'modal modal-slide-in-right',



		}).result.then(function () {
		}, function (res) {
		});

	}


	$scope.openLabelModal = function () {
		console.log("inside modal")


		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/Label.html',
			scope: $scope,




		}).result.then(function () {
		}, function (res) {
		});

	}

	$scope.addLabeltoNoteModal = function (note) {
		console.log("inside modal")
		$scope.note = note

		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/addlabeltonote.html',
			scope: $scope,




		}).result.then(function () {
		}, function (res) {
		});

	}
	$scope.addImageModal = function () {
		console.log("inside modal")


		$scope.$modalInstance = $uibModal.open({
			templateUrl: '/static/Todo/templates/imagemodal.html',
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
	function getBase64Image(base64string) {
		return base64string.replace(/^data:image\/(png|jpg);base64,/, "");
	}

	$scope.upload = function (croppeddataurl, filename) {
		console.log(croppeddataurl)
		var blob = new Blob([croppeddataurl], { type: 'image/jpg' });

		var file = JSON.stringify(getBase64Image(croppeddataurl))
		console.log("this is" + file)
		Upload.upload({

			url: 'addimage',
			data: {
				file: file, filename: filename, owner: localStorage.getItem('id'),
				headers: {
					token: localStorage.getItem('token'),
					id: localStorage.getItem('id'),

					'Cache-Control': 'no-cache'


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



	$scope.uploadnote = function (file, note) {
		Upload.upload({

			url: 'addimagetonote',
			data: {
				file: file, note: note.id,
				headers: {
					token: localStorage.getItem('token'),
					id: localStorage.getItem('id'),

					'Cache-Control': 'no-cache'


				}
			}

		}).then(function (resp) {
			console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
			$state.reload();
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
	var ctrl = function () {
		this.data = {
			selected: { src: null },
			imgToCrop: null,
		};
	};


	ctrl.prototype.onFileSelect = function (files) {
		var file = files[0];
		var _this = this;
		var reader = new FileReader();

		reader.onloadend = function () {
			_this.$scope.$apply(function () {
				_this.data.imgToCrop = reader.result;
			});
		}

		reader.readAsDataURL(file);
	};


	$scope.getImage = function () {
		var url = "getimage/" + localStorage.getItem("id")
		var service = restService.service('GET', url)
		service.then(function (response) {
			console.log(response.data)
			var image = response.data
			console.log("here is " + image.image)
			$scope.imageurl = 'http://127.0.0.1:8000/media/' + image.image
			console.log($scope.imageurl)
		})
	}
	$scope.getImage();




	$scope.addLabel = function (label) {
		var service = restService.service('POST', 'addlabel', label);
		service.then(function (response) {
			console.log("label added successfully")
			$state.reload()
			toastr.success("Label Added Successfully")

		})

	}
	var getLabelForUser = function () {
		$scope.labels = []
		var service = restService.service('GET', 'getlabel');
		service.then(function (response) {
			$scope.labels = response.data
			$scope.templabels = response.data
			console.log($scope.labels)
		})
	}
	$scope.getLabelForNote = function (note) {
		$scope.note.labels = {}
		var url = 'getlabelbynote/' + note.id
		var service = restService.service('GET', url);
		service.then(function (response) {
			note.labelstring = response.data

			console.log($scope.labels)
		})
	}
	$scope.addlabeltonote = function (label, note) {
		console.log(label)
		$scope.note = note
		$scope.note.collab = {}
		$scope.note.labelstring = {}
		$scope.note.label.push(label.id)
		// $scope.note.photo={}

		console.log("after push" + $scope.note)
		var url = "note/" + $scope.note.id
		var service = restService.service('PUT', url, $scope.note);
		service.then(function (response) {
			//$state.reload();
			//getLabelForUser() 
			// 	var index = $scope.templabels.indexOf(label);
			// $scope.templabels.splice(index, 1); 
			console.log("templabels" + $scope.templabels)
			$scope.getLabelForNote($scope.note)
		})

	}

	$scope.removelabelfromnote = function (label, note) {

		$scope.remove(label, note)


	}

	$scope.getnotebylabel = function (label) {
		localStorage.setItem("labelid", label.id)
		$scope.labellednotes = []
		localStorage.setItem("label", label.label)
		$state.go('label')
		getalllabelednotes()

	}
	$scope.deletelabel = function (label) {
		var url = "deletelabel/" + label.id
		var service = restService.service('DELETE', url);
		service.then(function (response) {
			toastr.success("label deleted")
			$state.reload()
			toastr.success("Label deleted Successfully")

		})

	}
	var getalllabelednotes = function () {
		$scope.displaylabel = localStorage.getItem("label")
		var labelid = localStorage.getItem("labelid")
		var url = 'getnotebylabel/' + labelid
		var service = restService.service('GET', url);
		service.then(function (response) {

			$scope.labellednotes = response.data
			console.log($scope.labellednotes)
			for (i in $scope.labellednotes) {


				if ($scope.note.isPinned) {
					$scope.pinned = 'Pinned';
					$scope.others = 'Others';
				}
				$scope.getcollabbynote($scope.labellednotes[i])
				$scope.getLabelForNote($scope.labellednotes[i])
				console.log($scope.labellednotes[i])

			}

		})

	}

	$scope.labelcolor = "#607D8B";
	//getalllabelednotes();

	$scope.remove = function (label, note) {
		var url = "note/" + note.id
		$scope.note = note
		var index = $scope.note.label.indexOf(label.id);
		$scope.note.label.splice(index, 1);
		$scope.note.labelstring = {}
		$scope.note.collab = {}

		var service = restService.service('PUT', url, $scope.note);

		service.then(function (response) {
			//$state.reload();
			console.log($scope.templabels)
			// $scope.templabels.push(label)
			$scope.getLabelForNote($scope.note)
		})
	}
	getLabelForUser()

	var getnotes = function () {
		if ($state.current.name == 'label') {
			getalllabelednotes();
		}
		else {

			getallnotes();
		}
	}
	getnotes();


});
