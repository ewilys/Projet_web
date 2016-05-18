function modification(){

	var outbound_message = {
	   			'login': $("#userID").val(),
	   			'pswrd': $("#pswrd").val(), 
	   			'memtype': $("input[type=radio][name=memberType]:checked").attr('value')
  		};
		$.ajax({
        		type: 'POST',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.user !== ""){
		     		$("#test_valid_ID").text(response.user);
		     		var el=document.getElementById("test_valid_ID");
		     		el.setAttribute("value", "logFilled");
		     	}
		     		
		     	
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function getEventFollowed(){
	
	var outbound_message = {
	   			'login': $("#userLogin").val(),
	   			'action' : "getEventFollowed",
  		};
		$.ajax({
        		type: 'GET',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.nb !== 0){
		     		info=new Array(response.nb);
		     		for(i=0;i<response.nb;i++){
		     			info[i]=response.Ev[i];
		     		}
		     		console.log(info);
		     	}else{
		     		console.log("pas de clubs suivis")
		     	}
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function getClubFollowed(){
	
	var outbound_message = {
	   			'login': $("#userID").val(),
	   			'action': "getClubFollowed",
  		};
		$.ajax({
        		type: 'GET',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.nb !== 0){
		     		info=new Array(response.nb);
		     		for(i=0;i<response.nb;i++){
		     			info[i]=response.clubs[i];
		     		}
		     		console.log(info);
		     	}else{
		     		console.log("pas de clubs suivis")
		     	}
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}