# chat/views.py

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from groq import Groq
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from langchain_groq import ChatGroq


# Initialize the Groq client
client = Groq(api_key=settings.GROQ_API_KEY)
# client = ChatGroq(
#     temperature=0.7,
#     groq_api_key=settings.GROQ_API_KEY,
#     model_name="llama-3.1-70b-versatile"
# )
@login_required
def chatbot(request):
    return render(request, 'chat.html')


@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON.'}, status=400)

        user_message = data.get('message', '')
        initialize = data.get('initialize', False)

        if initialize:
            # Handle initialization: job role and company name
            job_role = data.get('job_role')
            company_name = data.get('company_name', 'the company')

            # system_prompt = f"""
            #     You are simulating an interview for the position of {job_role} at {company_name}.
            #     - Start by greeting the candidate.
            #     - Ask one question at a time relevant to the {job_role} position.
            #     - Wait for the candidate's response before proceeding.
            #     - After each response, provide detailed (but not too long) and constructive feedback in the following format:
            #         1. **What was good about the answer**: Write a short paragraph highlighting the strengths.
                    
            #         2. **Areas for improvement**: Write a short paragraph pointing out the weaknesses or gaps in the answer.

            #         3. **Tips to enhance the answer**: Write a short paragraph offering practical and actionable tips.

            #     - Leave one empty line between each paragraph to ensure clarity and readability.
            #     - Proceed to the next question after providing the feedback in the specified format.
            #     """
            system_prompt = f"""
                You are simulating an interview for the position of {job_role} at {company_name}.
                - Start by greeting the candidate.
                - Ask one question at a time relevant to the {job_role} position.
                - Wait for the candidate's response before proceeding.
                - After each response, provide detailed (but not too long) and constructive feedback **strictly** in the following format with one blank line between paragraphs:

                Strictly follow the below format:
                **What was good about the answer**:  
                [Provide a short paragraph about the strengths of the candidate's answer.]

                
                **Areas for improvement**:  
                [Provide a short paragraph discussing weaknesses or areas that need more detail.]

                
                **Tips to enhance the answer**:  
                [Offer concise and actionable suggestions for improving the response.]

                - Use proper formatting, with **bold headings** as shown, and strictly ensure that each paragraph is separated by a blank line for readability.
                - Do not combine feedback into a single paragraph. Each section must appear as a standalone paragraph with spacing.
                """


            # Initialize conversation with system prompt
            conversation = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Begin the interview."}
            ]
            request.session['conversation'] = conversation

            # Call Groq API for initial response
            try:
                chat_completion = client.chat.completions.create(
                    messages=conversation,
                    model="llama-3.3-70b-specdec",
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                    stream=False,
                )
                bot_response = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"API Error: {e}")  # Log the error for debugging
                return JsonResponse({'message': 'Sorry, an error occurred while processing your request.'}, status=500)

            # Append assistant's reply to the conversation
            conversation.append({"role": "assistant", "content": bot_response})
            request.session['conversation'] = conversation

            return JsonResponse({'message': bot_response})

        elif user_message:
            conversation = request.session.get('conversation', [])

            # Append user's message
            conversation.append({"role": "user", "content": user_message})

            # Call Groq API for assistant's response
            try:
                chat_completion = client.chat.completions.create(
                    messages=conversation,
                    model="llama-3.3-70b-specdec",
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                    stream=False,
                )
                bot_response = chat_completion.choices[0].message.content.strip()
                print(bot_response)
            except Exception as e:
                print(f"API Error: {e}")  # Log the error for debugging
                return JsonResponse({'message': 'Sorry, an error occurred while processing your request.'}, status=500)

            # Append assistant's reply to the conversation
            conversation.append({"role": "assistant", "content": bot_response})
            request.session['conversation'] = conversation

            return JsonResponse({'message': bot_response})
        else:
            return JsonResponse({'message': 'No message received.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)

