
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
		     	$("#test_valid_ID").text(response.user);
		          $("#test_valid_pswrd").text(response.psw);
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}


function checkLicense() {
		
		var outbound_message = {
	   			'license': $("#userNo").val(),
	   			
  		};
		$.ajax({
        		type: 'POST',
		     url: '/register/member',
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	$("#test_duplicate_license").text(response.license);
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function checkDuplicateLog() {
		
		var outbound_message = {
	   			'login': $("#userID").val(),
  		};
		$.ajax({
        		type: 'POST',
		     url: '/register/member',
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	$("#test_duplicate_login").text(response.login);    
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

