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
from pathlib import Path
from django.conf import settings

llm_name="TheBloke/Llama-2-7B-Chat-GGUF"
llm_name="llmware/slim-tags-3b-tool"
api_key = "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"
model_name="TheBloke/Llama-2-7B-Chat-GGUF"

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
    new_chat = ChatResponse.objects.create(chat={"prompt": prompt, "response": response})
    new_chat.save()

    return Response({'success':True, 'data': {'prompt': new_chat.chat.get("prompt"), 'response': new_chat.chat.get("response")}})


@api_view(['POST'])
@permission_classes([AllowAny])
def prompt_with_sources_basic(request):
    body = json.loads(request.body)
    prompt = body.get("prompt")
    file = body.get("file_name")
    fp = os.path.join(settings.BASE_DIR, "media/docs")

    local_file = file

    prompter = Prompt().load_model(model_name)

    prompt_history = """"""
    history = ChatResponse.objects.all().order_by("-id")[:5]

    

    #   .add_source_document will do the following:
    #       1.  parse the file (any supported document type)
    #       2.  apply an optional query filter to reduce the text chunks to only those matching the query
    #       3.  batch according to the model context window, and make available for any future inferences

    sources = prompter.add_source_document(fp, local_file)
    # [INST]<<SYS>>Answer like a Professor. If Answer not in context say I dont know.<</SYS>>What is IPO?[/INST]
    for record in history:
        prompt_history += f"""
            [INST]<<SYS>>You are a helpful assistant. Answer Like a Professor.<</SYS>>{record.chat.get("prompt")}[/INST]
            {record.chat.get("response")}
        """
    
    prompt = """
      [INST]<<SYS>>Answer like a Teacher.<</SYS>>Did they seagull fly at last?[/INST]
      Yes, the young seagull did fly at last after overcoming his initial fear and with the help of his mother. After diving into space and experiencing a moment of terror, he felt his wings spread outwards and managed to fly away. This marks a significant milestone in the young seagull's life as he learns to overcome his fears and take to the skies, just like his siblings and parents.
      [INST]<<SYS>>Answer like a Teacher.<</SYS>>Could elaborate how the author described it?[/INST]
    """
    full_prompt = prompt_history + f"""[INST]<<SYS>You are a helpful assistant. Answer Like a Professor.<</SYS>>{prompt}[/INST]"""
    prompt_instruction = "facts_only"
    response = prompter.prompt_with_source(prompt=full_prompt, prompt_name=prompt_instruction)

    print(f"LLM Response - {response}")

    response_display = response[0]["llm_response"]
    print (f"- Context: {local_file}\n- Prompt: {full_prompt}\n- LLM Response:\n{response_display}")
    prompter.clear_source_materials()
    new_chat = ChatResponse.objects.create(chat={"prompt": full_prompt, "response": response_display})
    new_chat.save()
    return Response({'success':True, 'response': response_display, 'source': local_file})

    

    return 0