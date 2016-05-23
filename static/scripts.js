var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='number' name='licence_"+i+"' id='licence_"+i+"' required/>\n<label for='email_"+i+"'>Email du sportif "+i+" : </label>\n<input type='email' name='email_"+i+"' id='email_"+i+"' />";
	i++;
}

function toUnderScore(str){
	return str.replace(/ /g,"_");
}

function resultSearch(){
	type = $("input[type=radio][name=searchType]:checked").attr('value') ;
	console.log(type);
	if (type == "club"){
		
		var outbound_message = { 
					'stype' : 'club',
					'clubName': $("#clubName").val(),
		   			'place': $("#cplace").val(), 
		   		 };
		 console.log(outbound_message);
	}
	else{
		var outbound_message = { 
					'stype' : 'event',
					'categorie': $("#categorie").val(),
					'date':$("#date").val(),
					'eventName': $("#eventName").val(),
		   			//'place': $("#eplace").val(), 
		   		 };
	}
	$.ajax({
		type: 'POST',
		url: document.URL,
		data : JSON.stringify(outbound_message),
		dataType: 'json',
		contentType : 'application/json; charset=utf-8',
		success : function(response){
		
			var el = document.getElementById("result");
			var errase = el.innerHTML.replace(/<a[\s\S]*\/a>/,"");
			document.getElementById("result").innerHTML=errase;
			
			if (response.resSearch[0]=="null"){
				console.log ("pas de réponse" );
				document.getElementById("result").innerHTML += "\n\t<section id='element'><p>Aucune réponse ne correspond à votre recherche</p></section>";
			}
			else{
				console.log(response.resSearch[0]);
				if (type == 'club'){
					for(var i=0; i<response.resSearch.length; i++){
						document.getElementById("result").innerHTML += "\n\t<a href='http://localhost:5000/home/profile"+response.searchType+"/"+toUnderScore(response.resSearch[i][2])+"'>\n\t<section id='element'><h4>"+response.resSearch[i][0]+"</h4>\n\t<p>"+response.resSearch[i][1]+"</p></section></a>";
					}
				}
				else{
					
					for(var i=0; i<response.resSearch.length; i++){
						document.getElementById("result").innerHTML += "\n\t<a href='http://localhost:5000/profile"+response.searchType+"/"+toUnderScore(response.resSearch[i][0])+"'>\n\t<section id='element'><h4>"+response.resSearch[i][0]+"</h4>\n\t<p>"+response.resSearch[i][1]+"</p></section></a>";
					}
				}
			}
			 
		},
		error : function(){
			console.log("do not work");
		}
	});
}
			

function testRadio(){
	console.log("testRadio a été appelé");
	var outbound_message = {
	   			'searchtype': $("input[type=radio][name=searchType]:checked").attr('value')
  		};
	console.log(outbound_message.searchtype);
	if(outbound_message.searchtype === "event"){
		var el = document.getElementById("searchEvent");
		el.setAttribute("value", "Filled");
		el = document.getElementById("searchClub");
		el.setAttribute("value", "_blank");
	}
	else{
		var el = document.getElementById("searchClub");
		el.setAttribute("value", "Filled");
		el = document.getElementById("searchEvent");
		el.setAttribute("value", "_blank");
	}
}

function newSection(){
	console.log(document.URL);
	var pos = document.URL.lastIndexOf('/');
	var login = document.URL.substring(pos+1, document.URL.length);
	console.log(login);
	var outbound_message = { msg : 'hello' };
	$.ajax({
		type : 'POST',
		url: '/home/'+login,
		data : JSON.stringify(outbound_message),
		dataType : 'json',
		contentType : 'application/json; charset=utf-8',
		
		success : function(response){
			var nbEventTotal=response.N;
			console.log(nbEventTotal);
			var events = response.listeEvent;
			console.log(events);
			for(var j=0; j<nbEventTotal; j++){
				document.getElementById("container").innerHTML +="\n\t<a href='http://localhost:5000/profileEvent/"+toUnderScore(events[j][0])+"'><section id='event_"+j+"'>\n<h4>"+events[j][0]+"</h4>\n<p>"+events[j][1]+"</p>\n<p>"+events[j][2]+"</p>\n<p>"+events[j][3]+"</p>\n</section></a>";
		
			}
		},
		error : function(){
			console.log("do not work");
		}
	});
}

function testDate(id){
	console.log("recherche date");
	today=Tdate();
	if (id=="bday"){
        document.getElementById(id).setAttribute("max",resultat);
        }
     if (id=="start"){
        document.getElementById(id).setAttribute("min",resultat);
        document.getElementById("end").setAttribute("min",resultat);
        }
}


function testHour(){
	valStart=document.getElementById("start").value;
	today=Tdate();
	date=new Date;
	console.log(today, date);
	if(valStart==today){
		hours=date.getHours();
		minutes=date.getMinutes();
		hour=''+hours+':'+minutes+'';
		console.log(hour);
		document.getElementById("hour").setAttribute("min",hour);
	}
}


function Tdate(){
		
        date = new Date;
        year = date.getFullYear();
        month = date.getMonth()+1;
        if (month < 10){
        	month="0"+month;
        	}
        day = date.getDate();
        if(day <10){
        	day="0"+day;
        	}
        resultat=''+year+'-'+month+'-'+day+'';
        console.log(resultat);
        return resultat;
      
}

function testEnd(){
	valStart=document.getElementById("start").value;
	console.log(valStart);
	document.getElementById("end").setAttribute("min",valStart);
	testHour();
}

function modifProfileMember(){
	document.getElementById("container").innerHTML +="\n<form method='POST' action=''>\n"
	for(var i=0; i<6; i++){
		document.getElementById("field").innerHTML +="\n<input type='text' />"
	}
}
