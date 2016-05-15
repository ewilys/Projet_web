var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='number' name='licence_"+i+"' id='licence_"+i+"' required/>\n<label for='email_"+i+"'>Email du sportif "+i+" : </label>\n<input type='email' name='email_"+i+"' id='email_"+i+"' />";
	i++;
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


