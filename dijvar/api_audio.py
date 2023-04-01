'''
https://gradio.app/docs/#chatbot
https://www.youtube.com/watch?v=Si0vFx_dJ5Y
'''
import gradio as gr
import openai, config, os
openai.api_key = config.OPENAI_API_KEY


messages = [{"role": "system", "content": 'You are a helpfull English teacher. '}]

def transcribe(audio):
    global messages

    print(audio)
    os.rename(audio, audio + '.wav')
    print(audio)

    audio_file = open(audio + '.wav', "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    # subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text")
ui.launch()


