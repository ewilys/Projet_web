function checkLog() {
		
		var outbound_message = {
	   			'login': $("#userID").val(),
	   			'pswrd': $("#pswrd").val(), 
	   			'memtype': $("input[type=radio][name=memberType]:checked").attr('value')
  		};
		$.ajax({
        		type: 'POST',
		     url: '/login',
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.user !== ""){
		     		$("#test_valid_ID").text(response.user);
		     		var el=document.getElementById("test_valid_ID");
		     		el.setAttribute("value", "logFilled");
		     	}
		     		
		     	if(response.psw !== ""){ 
		     		$("#test_valid_pswrd").text(response.psw);    	
		         var el=document.getElementById("test_valid_pswrd");
		     		el.setAttribute("value", "pswFilled");
		     	}
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function checkSignUpMember() {
		
		var outbound_message = {
	   			'license': $("#userNo").val(),
	   			'newLogin': $("#login").val(),
	   			'email':$("#userMail").val(),
	   			'clubId':$("#clubId").val(),
	   			
  		};
		$.ajax({
        		type: 'POST',
		     url: '/register/member',
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.license !== ""){
		     		$("#test_duplicate_license").text(response.license);
		     		var el=document.getElementById("test_duplicate_license");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.email !== ""){
		     		$("#test_duplicate_email").text(response.email);
		     		var el=document.getElementById("test_duplicate_email");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.newLogin !== ""){
		     		$("#test_duplicate_login").text(response.newLogin);
		     		var el=document.getElementById("test_duplicate_login");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.license !== ""){
		     		$("#test_valid_clubId").text(response.clubId);
		     		var el=document.getElementById("test_valid_clubId");
		     		el.setAttribute("value", "Filled");
		     	}
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}


function checkSignUpClub() {
		
		var outbound_message = {
	   			'userName': $("#userName").val(),
	   			'newLogin': $("#login").val(),
	   			'email':$("#email").val(),
	   			'noFede':$("#noFederation").val(),
	   			
  		};
		$.ajax({
        		type: 'POST',
		     url: '/register/club',
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.userName !== ""){
		     		$("#test_duplicate_userName").text(response.clubName);
		     		var el=document.getElementById("test_duplicate_userName");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.email !== ""){
		     		$("#test_duplicate_email").text(response.email);
		     		var el=document.getElementById("test_duplicate_email");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.newLogin !== ""){
		     		$("#test_duplicate_login").text(response.newLogin);
		     		var el=document.getElementById("test_duplicate_login");
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.noFede !== ""){
		     		$("#test_duplicate_noFede").text(response.noFede);
		     		var el=document.getElementById("test_duplicate_noFede");
		     		el.setAttribute("value", "Filled");
		     	}
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}
