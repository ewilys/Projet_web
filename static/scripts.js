var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='number' name='licence_"+i+"' id='licence_"+i+"' />";
	i++;
}

function date(){
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
        document.getElementById("bday").setAttribute("max",resultat);
        
}
