$(document).ready(function(){
    $('.pump').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text(),
                cl:$(this).id()
            },
            success: function(response){
                $('.pump').text(response.html_paste)
            }
        })

    });
    $('.led').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text()
            },
            success: function(response){
                $('.led').text(response.html_paste)
            }
        })

    });
    $('.heat').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text()
            },
            success: function(response){
                $('.heat').text(response.html_paste)
            }
        })

    });
    $('.fan').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text()
            },
            success: function(response){
                $('.fan').text(response.html_paste)
            }
        })

    });
})