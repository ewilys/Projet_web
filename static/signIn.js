
function connexion() {
    $('#Connexion').click(function() {
 	var login = $("#userID").val();
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
}
