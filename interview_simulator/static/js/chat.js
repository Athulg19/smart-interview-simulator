$(document).ready(function(){
    $('#start-button').click(function(){
        var job_role = $('#job_role').val();
        var company_name = $('#company_name').val();
        if (job_role.trim() === '') {
            alert('Please enter a job role.');
            return;
        }
        $.ajax({
            url: '/chat/get_response/',
            type: 'POST',
            data: JSON.stringify({'initialize': true, 'job_role': job_role, 'company_name': company_name}),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response){
                $('#initial-input').hide();
                $('#chat-window').show();
                $('#messages').append('<div class="assistant-message">' + response.message + '</div>');
            },
            error: function(){
                alert('Error initializing the interview.');
            }
        });
    });

    // Send message with Enter key
    $('#user-input').on('keydown', function(e){
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            $('#send-button').click();
        }
    });

    $('#send-button').click(function(){
        var user_input = $('#user-input').val();
        if (user_input.trim() === '') return;

        $('#messages').append('<div class="user-message">' + user_input + '</div>');
        $('#user-input').val(''); // Clear input box
        $('#user-input').css('height', '50px');

        $.ajax({
            url: '/chat/get_response/',
            type: 'POST',
            data: JSON.stringify({'message': user_input}),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response){
                $('#messages').append('<div class="assistant-message">' + response.message + '</div>');
            }
        });
    });
});
