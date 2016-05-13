var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='number' name='licence_"+i+"' id='licence_"+i+"' required/>\n<label for='email_"+i+"'>Email du sportif "+i+" : </label>\n<input type='email' name='email_"+i+"' id='email_"+i+"' />";
	i++;
}

function date(id){
		console.log("recherche date");
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
        if (id=="bday"){
        document.getElementById(id).setAttribute("max",resultat);
        }
        if (id=="start"){
        document.getElementById(id).setAttribute("min",resultat);
        }
        
}
