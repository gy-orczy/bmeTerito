from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def main(request):

    return render(request, 'main/main.html', {})
    

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import ollama


@csrf_exempt
def generate_essay(request):
    def event_stream():
        # Collect form data
        name = request.POST['name']
        location = request.POST['location']
        age = request.POST['age']
        grade = request.POST['grade']
        worst_subject = request.POST['worst_subject']
        best_subject = request.POST['best_subject']
        tone = request.POST['tone']
        print(tone)

        # Construct detailed prompt
        prompt = f"""You are a professional advertiser for BME (Budapest usiversity of technology and echonomics)
        your job is to write  exactly 3 paragraphs of content (no longer than 400 words) that convinces them to
        apply to BME. You should craft the essay excellently so it has the highest chance to of convincing the student.
        Here are some inportant things to concider when you write the essay, Keep them in mind, however, never explicitly refer to them (except for the students name),
        - You should write the essay in a {tone} tone.
        - The name of the student is {name} 
        - The student lives in {location} 
        - His best subjec in school is {best_subject}, and his worst is {worst_subject} 
        - The students age is {age} 
        - And his grade is {grade}

        It is very important that you are talking to this student and that you wish to convince him.
        Be vary personal, write the text like you are talking to him on social media, or sending him a friendly email!
        But most importantly Write it according to the rules stated above. Pay Special attention to the TONE parameter!"""

        # Generate streaming response from Ollama
        stream = ollama.chat(
            model='llama3', 
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        
        for chunk in stream:
            if chunk['done']:
                break
            if 'message' in chunk and 'content' in chunk['message']:
                yield f"{chunk['message']['content']}"

    # Return streaming response
    response = StreamingHttpResponse(
        event_stream(), 
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response    
