function toUnderScore(str){
	return str.replace(/ /g,"_");
}



function modification(){
	var el = document.getElementById("modif");
	el.setAttribute("value", "Filled");
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
	   			'action' : "getEventFollowed",
  		};
		$.ajax({
        		type: 'POST',
		     url: document.URL,
		     data: JSON.stringify(outbound_message),         
	    		dataType: 'json',
	    		contentType: 'application/json; charset=utf-8', 
		       
		     success: function(response) {
		     	if(response.nb !== 0){
		     		for(j=0;j<response.nb;j++){
		     			document.getElementById("events").innerHTML +="\n\t<a href='http://localhost:5000/profileEvent/"+toUnderScore(events[j][0])+"'><section id='event_"+j+"'>\n<h4>"+events[j][0]+"</h4>\n<p>"+events[j][1]+"</p>\n<p>"+events[j][2]+"</p>\n<p>"+events[j][3]+"</p>\n</section></a>";
		     		}
		     	}
		     	else{
		     		console.log("pas d'évènements suivis");
		     	}
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function getClubFollowed(){
	
	var outbound_message = {
	   			'action': "getClubFollowed",
  		};
		$.ajax({
        	type: 'POST',
		   url: document.URL,
	    	data: JSON.stringify(outbound_message),         
	    	dataType: 'json',
	   	contentType: 'application/json; charset=utf-8', 
		       
		   success: function(response) {
		   	if(response.nb !== 0){
		     		for(i=0;i<response.nb;i++){
		     			document.getElementById("clubs").innerHTML +="\n\t<a href='http://localhost:5000/home/profileClub/"+response.clubs[i][0]+"'><section><h4>"+response.clubs[i][1]+"</h4><p>"+response.clubs[i][2]+"</p></section></a>";
		     		}
		     	}
		     	else{
		     		console.log("pas de clubs suivis");
		     	}
			},
		   error: function() {
		   	console.log("do not work");
		   }
    });
}
