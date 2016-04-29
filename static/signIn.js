

function inscription-membre() {
    $('#btnConnexion').click(function() {
 
        $.ajax({
            url: '/connexion',
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
