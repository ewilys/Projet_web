var i=0;

function newLicence(){
	document.getElementById("players").innerHTML += "\n<br/><label for='licence_"+i+"'>Licence "+i+" : </label>\n<input type='text' name='licence_"+i+"' id='licence_"+i+"' />";
	i++;
}
