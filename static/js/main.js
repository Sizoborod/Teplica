$(document).ready(function(){
    $('.pump').click(function(){
        $.ajax({
            url: '/buttons',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text(),
                name:'pump'

            },
            success: function(response){
                $('.pump').text(response.html_paste)
            }
        })

    });
    $('.led').click(function(){
        $.ajax({
            url: '/buttons',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text(),
                name:'led'
            },
            success: function(response){
                $('.led').text(response.html_paste)
            }
        })

    });
    $('.heat').click(function(){
        $.ajax({
            url: '/buttons',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text()
                ,
                name:'heat'
            },
            success: function(response){
                $('.heat').text(response.html_paste)
            }
        })

    });
    $('.fan').click(function(){
        $.ajax({
            url: '/buttons',
            type: 'get',
            contentType: 'application/json',
            data:{
                button_text: $(this).text()
                ,
                name:'fan'
            },
            success: function(response){
                $('.fan').text(response.html_paste)
            }
        })

    });
})