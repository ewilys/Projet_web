var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='number' name='licence_"+i+"' id='licence_"+i+"' onkeyup='javascript:checkDupLicence(id,"+i+");' required/>\n<label for='email_"+i+"'>Email du sportif "+i+" : </label>\n<input type='email' name='email_"+i+"' id='email_"+i+"' onkeyup='javascript:checkDupEmail(id,"+i+");'/>\n<br/>\n";
	i++;
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
				document.getElementById("container").innerHTML +="\n\t<a href='http://localhost:5000/home/profileEvent/"+events[j][0]+"'><section id='event_"+j+"'>\n<h4>"+events[j][0]+"</h4>\n<p>"+events[j][1]+"</p>\n<p>"+events[j][2]+"</p>\n<p>"+events[j][3]+"</p>\n</section></a>";
		
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
		if (hours <10) {
			hours='0'+hours;
		}
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
