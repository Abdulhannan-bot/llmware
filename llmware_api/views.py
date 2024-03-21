import json
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ChatResponse
from django.http import JsonResponse
# Create your views here.
import os
from llmware.prompts import Prompt
from llmware.setup import Setup
from llmware.models import PromptCatalog

llm_name="TheBloke/Llama-2-7B-Chat-GGUF"
api_key = "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"

@api_view(['POST'])
@permission_classes([AllowAny])
def home(request):
    body = json.loads(request.body)
    prompt = body.get("prompt")
    prompter = Prompt(llm_name=llm_name, llm_api_key=api_key)
    history = ChatResponse.objects.all().order_by("-id")[:5]
    context = ""
    for record in history:
        context += f"""[INST]
        <<SYS>>You are a helpful assistant. Answer like Neil De Grasse Tyson.<</SYS>>
        {record.chat.get("prompt")}
        [/INST]
        {record.chat.get("response")}
        """
    prompt = f"""[INST]
    <<SYS>>You are a helpful assistant. Answer like Neil De Grasse Tyson.<</SYS>>
    {prompt}
    [/INST]
    """
    response = prompter.prompt_main(prompt=prompt, context=context)["llm_response"]
    print (f"- Context: {context}\n- Prompt: {prompt}\n- LLM Response:\n{response}")
    new_chat = Prompt.objects.create(chat={"prompt": prompt, "response": response})
    new_chat.save()

    return Response({'success':True, 'data': {'prompt': new_chat.chat.get("prompt"), 'response': new_chat.chat.get("response")}})
