import gradio as gr
import openai, config
openai.api_key = config.OPENAI_API_KEY


messages = [{"role": "system", "content": 'You are a therapist. Respond to all input in 25 words or less.'}]

def chatbot(text):
    global messages

    messages.append({"role": "user", "content": text})

    '''
    https://platform.openai.com/docs/api-reference/chat/create

    max_tokens: -integer -Optional -Defaults to inf
    Sohbet tamamlama sırasında oluşturulacak maksimum jeton sayısı.
    Girdi belirteçlerinin ve oluşturulan belirteçlerin toplam uzunluğu, 
    modelin bağlam uzunluğu ile sınırlıdır.

    n: -integer -Optional -Defaults to 1
    Her giriş mesajı için kaç tane sohbet tamamlama seçeneği oluşturulacağı.

    stop: -string or array -Optional -Defaults to null
    API'nin daha fazla belirteç oluşturmayı durduracağı en fazla 4 cümle.

    temperature: -number -Optional -Defaults to 1
    0 ile 2 arasında hangi örnekleme sıcaklığının kullanılacağı. 
    0,8 gibi daha yüksek değerler çıkışı daha rastgele hale getirirken, 
    0,2 gibi daha düşük değerler çıkışı daha odaklanmış ve deterministik hale getirir.
    Genellikle bunu veya top_p ı değiştirmenizi öneririz, ikisini birden değil.

    top_p: -number -Optional -Defaults to 1
    Sıcaklıkla örneklemeye bir alternatif, çekirdek örnekleme olarak adlandırılır ve burada model, 
    top_p olasılık kütlesine sahip belirteçlerin sonuçlarını dikkate alır. Yani 0.1, yalnızca 
    en yüksek %10 olasılık kütlesini oluşturan belirteçlerin dikkate alındığı anlamına gelir.

    frequency_penalty: -number -Optional -Defaults to 0
    -2.0 ile 2.0 arasında bir sayı. Pozitif değerler, yeni belirteçleri o ana kadar metindeki mevcut 
    sıklıklarına göre cezalandırarak, modelin aynı satırı kelimesi kelimesine tekrar etme olasılığını azaltır.

    presence_penalty: -number -Optional -Defaults to 0
    -2.0 ile 2.0 arasında bir sayı. Pozitif değerler, yeni belirteçleri o ana kadar metinde görünüp 
    görünmediklerine bağlı olarak cezalandırır ve modelin yeni konular hakkında konuşma olasılığını artırır.

    stream: -boolean -Optional -Defaults to false
    Ayarlanırsa, ChatGPT'de olduğu gibi kısmi mesaj deltaları gönderilir. Belirteçler, kullanılabilir olduklarında 
    yalnızca veri sunucu tarafından gönderilen olaylar olarak gönderilir ve akış bir data: [DONE] mesajla sonlandırılır. 
    Örnek kod için https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
    '''
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                            messages=messages,
                                            max_tokens=150,
                                            n=1,
                                            stop=None,
                                            temperature=0.5,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stream=False
                                            )

    system_message = response["choices"][0]["message"]
    messages.append(system_message)


    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=chatbot, inputs="text", outputs="text")
ui.launch()