---
layout: post
comments: true
current: post
cover: assets/images/posts/lucas-george-wendt-U43qS0ooeck-unsplash_resized.webp
navigation: True
title: "Building a ChatGPT-based AI Assistant with Python using OpenAI APIs"
date: 2023-03-05 11:11:11
tags: [AI]
class: post-template
subclass: 'post tag-ai'
author: faizan
excerpt: This article demonstrates a workflow for integrating multiple AI services to perform speech-to-text (STT), natural language processing (NLP), and text-to-speech (TTS) using OpenAI's ChatGPT and Whisper API's in Python.
---
ChatGPT has unveiled a world of possibilities lying ahead for us in the age of AI. The rate of adoption of ChatGPT rattled giants like Google. In the rising generation of AI, we will witness paradigm shifts and the far-reaching consequences of AI in almost all spheres of human lives. But this age will also allow us to leverage AI to improve human lives.

As scary as it can get for some people, ChatGPT can be leveraged in fun new ways. This article is a practical demonstration of one of the ways we can leverage the power of ChatGPT, NLP, STT and TTS :).

This article demonstrates a workflow for integrating multiple AI services to perform speech-to-text (STT), natural language processing (NLP), and text-to-speech (TTS) using OpenAI's ChatGPT and Whisper APIs in Python.

***
# Table of Contents

* [The OpenAI APIs](#the-openai-apis)
* [Setting Up](#setting-up)
* [Recognize the Speech](#recognize-the-speech)
* [Listen to the Whispers](#listen-to-the-whispers)
* [The Completions](#the-completions)
* [Speak Up](#speak-up)
* [The Assembly Line](#the-assembly-line)
    * [Installing Libraries](#installing-libraries)
* [Usage](#usage)
* [Conclusion](#conclusion)

***

## The OpenAI APIs

OpenAI exposes a set of APIs to interact with its GPT models. For example, earlier this month, they launched an API endpoint for chat completions with the ChatGPT model. This opens up a wide variety of applications. For instance, we can directly call and get responses from the ChatGPT model and embed its answers in our applications OpenAI has recently launched the Whisper APIs used to convert Speech to Text.

In this article, we will leverage the chat completions API using the ChatGPT model and Whisper API to convert speech to text.

## Setting Up

Set up shop properly. To get the job done.

Our script starts by declaring a few variables like the `openaiurl` and the `openai_token` for setting up a connection to the OpenAI API using an API token stored in the environment variable `OPENAI_API_TOKEN`. After that, the script exits with an error code if the token is not set.

The API token is passed into the request in the form of an `Authorization` header, as shown in the code below:

{% highlight python %}
openaiurl = "https://api.openai.com/v1"
openai_token = os.environ.get("OPENAI_API_TOKEN")
if openai_token == "":
    os.exit(1)
headers = { "Authorization" : f"Bearer {openai_token}" }
{% endhighlight %}

## Recognize the Speech

The spoken word and its absence are essential. In many ways.

The intent is to leverage the microphones present on our pristine computational machines. We capture the spoken word into a `wav` format audio file. 

The script then prompts the user to speak into their microphone and records the audio using the `SpeechRecognition` library. Finally, the audio is saved to a WAV file in the `audio` folder.

{% highlight python %}
# obtain the audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source)

folder = "./audio"
filename = "microphone-results"
audio_file_path = f"{folder}/{filename}.wav"

if not os.path.exists(folder):
    os.mkdir(folder)

# write audio to a WAV file
print(f"Generating WAV file, saving at location: {audio_file_path}")
with open(audio_file_path, "wb") as f:
    f.write(audio.get_wav_data())
{% endhighlight %}

## Listen to the Whispers

Whisper is powerful. There is a reason it can't be said out loud.

We intend to leverage the OpenAI Whisper API to transcribe our audio file to text. The model used by OpenAI to perform transcriptions is labelled `whisper-1`.

Our script sends a `POST` request to the Whisper API with the audio file as data. The API performs Speech-To-Text(STT) on the audio and returns the transcribed text.

{% highlight python %}
url = f"{openaiurl}/audio/transcriptions"

data = {
    "model": "whisper-1",
    "file": audio_file_path,
}
files = {
    "file": open(audio_file_path, "rb")
}

response = requests.post(url, files=files, data=data, headers=headers)

print("Status Code", response.status_code)
speech_to_text = response.json()["text"]
print("Response from Whisper API's", speech_to_text)
{% endhighlight %}

We get a response containing a `text` key with the transcription value.

## The Completions

We all need completions. I meant closures.

Here we will call the OpenAI chat completions endpoint with the transcribed text. To use the ChatGPT model, we pass the model's name `gpt-3.5-turbo`.

The script sends another `POST` request to the OpenAI API with the transcribed text as data. The API uses the ChatGPT model to perform NLP on the text and returns a response.

{% highlight python %}
url = f"{openaiurl}/chat/completions"

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": speech_to_text
        }
    ]
}

response = requests.post(url, json=data, headers=headers)

print("Status Code", response.status_code)
chatgpt_response = response.json()["choices"][0]["message"]["content"]
print("Response from ChatGPT model ", chatgpt_response)
{% endhighlight %}

Finally, we have the response from ChatGPT.

## Speak up

We have to Speak up. At some point.

Now we need to play the response back to the user. So, this is how we do it.

Our script uses the `pyttsx3` library to convert the NLP response to speech and plays the audio output through the user's speakers.

{% highlight python %}
engine = pyttsx3.init()
engine.setProperty('rate', 175)

print("Converting text to speech...")
engine.say(chatgpt_response)

engine.runAndWait()
engine.stop()
{% endhighlight %}

We have all experienced text-based interactions with ChatGPT. Our approach here is more of a conversational nature, like Alexa. We can easily extend our script to involve going deeper by asking follow-up questions.

## The Assembly Line

All complex things are assembled. Sometimes in unlikely places.

{% gist f4411801901a51a3cb1f93402611d3f5 %}

### Installing Libraries

Libraries feed curious minds. The ones with books.

I performed this setup on a MacBook Pro. To get the audio recording to work, I had to install the following:

{% highlight shell %}
brew install portaudio
{% endhighlight %}

The following libraries are used in the code. Install them using the following commands:

{% highlight shell %}
pip install SpeechRecognition
pip install pyttsx3
{% endhighlight %}

## Usage

Knowing how to use things is a talent. Knowing when timing.

To use the script, we need to run it. So be sure to install the dependencies first.

{% highlight shell %}
python main.py
{% endhighlight %}

After running the script, we get a message on the terminal stating, "Say Something!". When the prompt hit the terminal, we must come up with a question and speak up. A pause is detected to stop the recording.

{% highlight shell %}
python main.py
[-] Record audio using microphone
Say something!
Generating WAV file, saving at location: ./audio/microphone-results.wav
{% endhighlight %}

After that, the recording gets stored as a `wav` file. The audio file is then passed on to the OpenAI Whisper transcription API. Finally, the API returns with a transcription response.

{% highlight shell %}
python main.py
...
[-] Call to Whisper APIs to get the STT response
Status Code 200
Response from Whisper API's "Summarise Limitless by Jim Kwik"
{% endhighlight %}

The transcribed response is used to query the OpenAI chat completion API leveraging the ChatGPT model. Finally, the endpoint returns a JSON response with the ChatGPT response.

{% highlight shell %}
python main.py
...
[-] Querying ChatGPT model with the STT response data
Status Code 200
Response from ChatGPT model

In his book "Limitless," Jim Kwik offers a variety of strategies to help readers unlock their full brain potential. He emphasizes the importance of proper nutrition, exercise, and sleep for optimal brain function, and also provides techniques for improving memory, learning, and problem-solving skills. Kwik argues that the key to achieving personal and professional success is to continually challenge and stretch yourself, with a focus on long-term growth rather than short-term wins. Overall, "Limitless" provides practical and actionable advice for anyone looking to optimize their cognitive abilities and achieve their goals.
{% endhighlight %}

Finally, this text response is converted to text-to-speech (TTS) audio, which you can hear from the speakers.

{% highlight shell %}
python main.py
...
[-] Try to convert TTS from the response
Converting text to speech...
{% endhighlight %}

## Conclusion

Conclusions are an invitation to continue. That's how I see them.

This code demonstrates how multiple AI services can be integrated to create a more complex application. In this example, the user's spoken input is transcribed to text using STT, analyzed using NLP, and the response is converted to speech using TTS. This workflow can be adapted and extended to create more sophisticated applications with many use cases. You can find the code for this article in the GitHub repo [The Speaking ChatGPT](https://github.com/faizanbashir/speaking-chatgpt).

This article is a dedication to my boy Mursaleen (Mursi) on his 2nd birthday. Happy Birthday! 🎉