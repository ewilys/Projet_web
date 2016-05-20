function modification(){

	
}

function checkNewInfoClub(){

	var outbound_message = {
	   			'newE': $("#newEmail").val(),
	   			'newL': $("#newLogin").val(),
  		};
  		console.log(document.URL);
		$.ajax({
        		type: 'POST',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.newE !== ""){
		     		$("#test_duplicate_email").text(response.newE);
		     		var el=document.getElementById("test_duplicate_email");
		     		el.setAttribute("value", "logFilled");
		     	}
		     	if(response.newL !== ""){
		     		$("#test_duplicate_login").text(response.newL);
		     		var el=document.getElementById("test_duplicate_login");
		     		el.setAttribute("value", "logFilled");
		     	}
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function checkNewInfoSportif(){

	var outbound_message = {
	   			'newE': $("#email").val(),
	   			
  		};
		$.ajax({
        		type: 'POST',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.newE !== ""){
		     		$("#test_valid_ID").text(response.newE);
		     		var el=document.getElementById("test_duplicate_email");
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
		     		for(i=0;i<response.nb;i++){
		     			for(j=0;j<response.Ev[i].length();j++){
		     				
		     			}
		     		}
		     		console.log(Ev);
		     	}else{
		     		console.log("pas d'évènements suivis")
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
		     		for(i=0;i<response.nb;i++){
		     			for(j=0;j<response.clubs[i].length();j++){
		     				
		     			}
		     		}
		     		console.log(clubs);
		     		
		     	}else{
		     		console.log("pas de clubs suivis")
		     	}
		     
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}
