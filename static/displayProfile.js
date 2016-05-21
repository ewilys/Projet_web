function toUnderScore(str){
	return str.replace(/ /g,"_");
}



function modification(){
	var el = document.getElementById("modif");
	el.setAttribute("value", "Filled");
}

function getEventFollowed(){
	el = document.getElementById("events");
	var errase = el.innerHTML.replace(/<a[\s\S]*\/a>/,"");
  	document.getElementById("events").innerHTML=errase;
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
		     			document.getElementById("events").innerHTML +="\n\t<a href='http://localhost:5000/profileEvent/"+toUnderScore(response.events[j][0])+"'><section id='event_"+j+"'>\n<h4>"+response.events[j][0]+"</h4>\n<p>"+response.events[j][1]+"</p>\n<p>"+response.events[j][2]+"</p>\n<p>"+response.events[j][3]+"</p>\n</section></a>";
		     		}
		     	}
		     	else{
		     		console.log("pas d'évènements suivis");
		     		document.getElementById("events").innerHTML += "<a href='http://localhost:5000/home/search'><section id='no_event'><p>Vous n'êtes inscrit a aucun évènement, cliquez pour lancer une recherche !</p></section></a>";
		     	}
		     	var el = document.getElementById("events");
		     	el.setAttribute("value", "Filled");
		     	el = document.getElementById("modif");
		     	el.setAttribute("value", "_blank");
		     	el = document.getElementById("clubs");
		     	el.setAttribute("value", "_blank");
		     	var errase = el.innerHTML.replace(/<a[\s\S]*\/a>/,"");
		     	document.getElementById("clubs").innerHTML=errase;
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function getClubFollowed(){
	el = document.getElementById("clubs");
	var errase = el.innerHTML.replace(/<a[\s\S]*\/a>/,"");
  	document.getElementById("clubs").innerHTML=errase;
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
		     		document.getElementById("clubs").innerHTML += "<a href='http://localhost:5000/home/search'><section id='no_club'><p>Vous ne suivez aucun club, cliquez pour lancer une recherche !</p></section></a>";
		     	}
		     	var el = document.getElementById("clubs");
		     	el.setAttribute("value", "Filled");
		     	el = document.getElementById("modif");
		     	el.setAttribute("value", "_blank");
		     	el = document.getElementById("events");
		     	el.setAttribute("value", "_blank");
		     	var errase = el.innerHTML.replace(/<a[\s\S]*\/a>/,"");
		     	document.getElementById("events").innerHTML=errase;
			},
		   error: function() {
		   	console.log("do not work");
		   }
    });
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
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.newL !== ""){
		     		$("#test_duplicate_login").text(response.newL);
		     		var el=document.getElementById("test_duplicate_login");
		     		el.setAttribute("value", "Filled");
		     	}
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}

function checkNewInfoMember(){

	var outbound_message = {
	   			'newE': $("#newEmail").val(),
	   			'newL': $("#newLogin").val(),
	   			'action' : "checkInfo",
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
		     		el.setAttribute("value", "Filled");
		     	}
		     	if(response.newL !== ""){
		     		$("#test_duplicate_login").text(response.newL);
		     		var el=document.getElementById("test_duplicate_login");
		     		el.setAttribute("value", "Filled");
		     	}
		     		
		     },
		     error: function() {
		           console.log("do not work");
		     }
       	});
}
