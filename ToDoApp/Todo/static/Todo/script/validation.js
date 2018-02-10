function checkvalid() {

	if (document.getElementById("username").value == "") {

		//alert("Cannot leave firstname this field blank");
		/*	document.getElementById("fname").height="30%"*/
		document.getElementById("error").innerHTML = "cannot leave this blank";
		return false;
	}
	var regex = /^[a-zA-Z0-9]{2,30}$/;
	var ctrl = document.getElementById("username");

	if (regex.test(ctrl.value) != true) {
		document.getElementById("error").innerHTML = "pls enter correct name";
		return false;
	}

	if (document.getElementById("username").value == "") {

		//alert("Cannot leave firstname this field blank");
		/*	document.getElementById("fname").height="30%"*/
		document.getElementById("error").innerHTML = "cannot leave this blank";
		return false;
    }
    
    regex = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/
	ctrl = document.getElementById("email");
	if (document.getElementById("email").value == "") {
		document.getElementById("error").innerHTML = "pls enter correct value";
		//alert("Cannot leave email field blank");
		return false;
	}
	if (regex.test(ctrl.value) != true) {
		document.getElementById("email").innerHTML = "pls enter correct email";
		return false;
	}

	if (document.getElementById("password").value == "") {
		//alert("Cannot leave password field blank");
		document.getElementById("error").innerHTML = "pls enter password";
		return false;
	}
	if (document.getElementById("password").value.length < 4
		|| document.getElementById("password").value.length > 20) {
		document.getElementById("error").innerHTML = "pls enter password with correct length";
		//alert("pls enter correct number of character for password");
		return false;
    }
    return true;
}

$('[data-toggle="offcanvas"]').click(function () {
	console.log("entered here")
	$('#wrapper').toggleClass('toggled');
});


