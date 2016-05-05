
function checkLog() {
		var login = $("#userID").val();
		//var psw = $("#pswrd").val();
		$.ajax({
        		type: 'POST',
		     url: '/login',
		     data: JSON.stringify(login),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		          $("#test_valid_ID").text(response.user);
		          //$("#test_valid_pswrd").text(response.psw);
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

["#userID"].forEach(function(item) {
  $(item).on("keyup", function(event) {
    checkLog();
  });
});
