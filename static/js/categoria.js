$(document).ready(function(){
    $('#save').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'aplicacition/json',
            data: {
                button_text: $(this).text()              
            },
            success: function(responsive){
                $('.btn').text(responsive.seconds)
            }
        })
    })
})