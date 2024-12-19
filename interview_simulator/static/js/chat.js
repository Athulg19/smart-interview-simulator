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
                displayAssistantMessage(response.message);
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

        // Display user's message
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
                displayAssistantMessage(response.message);
            },
            error: function(){
                alert('Error processing your message.');
            }
        });
    });

    // Function to display assistant's message with formatting
    function displayAssistantMessage(message) {
        // Split message by double line breaks for separate paragraphs
        var paragraphs = message.split('\n\n');
        var formattedMessage = '';

        paragraphs.forEach(function(paragraph) {
            formattedMessage += '<p>' + paragraph + '</p>';
        });

        $('#messages').append('<div class="assistant-message">' + formattedMessage + '</div>');
        $('#messages').scrollTop($('#messages')[0].scrollHeight); // Auto-scroll to bottom
    }
});
