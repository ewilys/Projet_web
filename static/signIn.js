
function checkLog() {
		
		var outbound_message = {
	   			'login': $("#userID").val(),
	   			'pswrd': $("#pswrd").val(), 
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

