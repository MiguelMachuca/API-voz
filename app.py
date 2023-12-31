from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import asyncio
import io  
from google.cloud import texttospeech
from google.cloud.texttospeech_v1.types.cloud_tts import SsmlVoiceGender
import cloudinary.uploader

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'demoServiceAccount.json'

app = Flask(__name__)
#CORS(app, resources={r"/synthesize": {"origins": "https://convert-404900.ue.r.appspot.com"}})
CORS(app)


cloudinary.config( 
  cloud_name = "dwivq8xpf", 
  api_key = "281237694383168", 
  api_secret = "JEpjLegCXhz1LTdEP5XgO2uvb3Q" 
)

async def synthesize_speech(input_text, voice_params):
    async with texttospeech.TextToSpeechAsyncClient() as client:
        synthesis_input = texttospeech.SynthesisInput(text=input_text)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = await client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        
        return response.audio_content

@cross_origin    
@app.route('/synthesize/<language>/<nombre>/<text>', methods=['GET'])
def synthesize_get(language, nombre, text):
    voice_params = get_voice_params(language, nombre)

    audio_content = asyncio.run(synthesize_speech(text, voice_params))

    upload_result = cloudinary.uploader.upload_large(
        io.BytesIO(audio_content),
        resource_type='video',
        folder='audio_files',
        overwrite=True,
        filename_override=f'audio_{language}.mp3'
    )

    audio_url = upload_result['secure_url']

    print(f'Enlace del audio: {audio_url}')  

    return jsonify({'audio_url': audio_url}), 200

    # return jsonify({'message': f'Audio synthesized in {language}', 'audio_url': audio_url}), 200
        
@cross_origin
@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data['text']
    language = data['language']
    nombre = data['nombre']
    
    voice_params = get_voice_params(language, nombre)
    
    audio_content = asyncio.run(synthesize_speech(text, voice_params))

    upload_result = cloudinary.uploader.upload_large(
        io.BytesIO(audio_content),
        resource_type='video',
        folder='audio_files',
        overwrite=True,
        filename_override=f'audio_{language}.mp3'
    )

    audio_url = upload_result['secure_url']

    print(f'Enlace del audio: {audio_url}')  # Imprime el enlace en la consola
    
    return jsonify({'message': f'Audio synthesized in {language}', 'audio_url': audio_url}), 200


def get_voice_params(language, nombre):
    # Idioma Ingles

    if language == 'en':
        # VOCES DE VARONES
        if nombre == 'james':            
            return texttospeech.VoiceSelectionParams(                        
                name='en-AU-Wavenet-B',
                language_code='en-AU',
                ssml_gender=SsmlVoiceGender.MALE
            )
        elif nombre == 'william':
            return texttospeech.VoiceSelectionParams(                        
                name='en-GB-Neural2-B',
                language_code='en-GB'                
            )
        elif nombre == 'john':
            return texttospeech.VoiceSelectionParams(                        
                name='en-US-Neural2-D',
                language_code='en-US'                
            )
        # VOCES DE DAMAS  
        elif nombre == 'jane':
            return texttospeech.VoiceSelectionParams(                        
                name='en-US-Standard-E',
                language_code='en-US'            
            )
        elif nombre == 'emily':
            return texttospeech.VoiceSelectionParams(                        
                name='en-GB-Wavenet-A',
                language_code='en-GB'
            )
        elif nombre == 'virginia':
            return texttospeech.VoiceSelectionParams(                        
                name='en-AU-Wavenet-C',
                language_code='en-AU'
            )
        else:
            return texttospeech.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=SsmlVoiceGender.MALE
            )
    # Idioma Español                  
    elif language == 'es':  
        # VOCES DE VARONES
        if nombre == 'jose':
            return texttospeech.VoiceSelectionParams(                        
                name='es-ES-Neural2-F',
                language_code='es-ES'
            )
        elif nombre == 'pablo':
            return texttospeech.VoiceSelectionParams(                        
                name='es-US-Neural2-C',
                language_code='es-US'
            )
        elif nombre == 'diego':
            return texttospeech.VoiceSelectionParams(                        
                name='es-US-Neural2-B',
                language_code='es-US'
            )
        # VOCES DE DAMAS  
        elif nombre == 'rocio':
            return texttospeech.VoiceSelectionParams(                        
                name='es-ES-Neural2-D',
                language_code='es-ES'                
            )
        elif nombre == 'isabel':
            return texttospeech.VoiceSelectionParams(                        
                name='es-US-Neural2-A',
                language_code='eS-US'
            )
        elif nombre == 'evelin':
            return texttospeech.VoiceSelectionParams(                        
                name='es-US-Wavenet-A',
                language_code='es-US'
            )
        else:
            return texttospeech.VoiceSelectionParams(
                language_code='es-ES',
                ssml_gender=SsmlVoiceGender.MALE
            )        
    
    # Idioma Frances
    elif language == 'fr':
        # VOCES DE VARONES
        if nombre == 'marcel':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-CA-Neural2-B',
                language_code='fr-CA'
            )
        elif nombre == 'albert':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-CA-Neural2-D',
                language_code='fr-CA'
            )
        elif nombre == 'blaise':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-FR-Neural2-B',
                language_code='fr-FR'
            )
        # VOCES DE DAMAS  
        elif nombre == 'simone':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-FR-Neural2-C',
                language_code='fr-FR'                
            )
        elif nombre == 'edith':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-FR-Neural2-E',
                language_code='fr-FR'
            )
        elif nombre == 'juliette':
            return texttospeech.VoiceSelectionParams(                        
                name='fr-CA-Neural2-C',
                language_code='fr-CA'
            )
        else:
            return texttospeech.VoiceSelectionParams(
            name='fr-FR-Neural2-E',
            language_code='fr-FR',
            ssml_gender=SsmlVoiceGender.FEMALE
            )

    # Idioma Aleman        
    elif language == 'de':
        # VOCES DE VARONES
        if nombre == 'franz':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Neural2-B',
                language_code='de-DE'
            )
        elif nombre == 'karl':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Neural2-D',
                language_code='de-DE'
            )
        elif nombre == 'otto':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Polyglot-1',
                language_code='de-DE'
            )
        # VOCES DE DAMAS  
        elif nombre == 'anne':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Neural2-C',
                language_code='de-DE'                
            )
        elif nombre == 'nina':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Neural2-F',
                language_code='de-DE'
            )
        elif nombre == 'emmy':
            return texttospeech.VoiceSelectionParams(                        
                name='de-DE-Studio-C',
                language_code='de-DE'
            )
        else:
            return texttospeech.VoiceSelectionParams(
                language_code='de-DE',
                ssml_gender=SsmlVoiceGender.MALE
            )

    # Idioma Italiano        
    elif language == 'it':
        # VOCES DE VARONES
        if nombre == 'enzo':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Neural2-C',
                language_code='it-IT'
            )
        elif nombre == 'dante':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Standard-C',
                language_code='it-IT'
            )
        elif nombre == 'galileo':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Wavenet-D',
                language_code='it-IT'
            )
        # VOCES DE DAMAS  
        elif nombre == 'grazia':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Standard-A',
                language_code='it-IT'                
            )
        elif nombre == 'elsa':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Wavenet-B',
                language_code='it-IT'
            )
        elif nombre == 'gina':
            return texttospeech.VoiceSelectionParams(                        
                name='it-IT-Standard-B',
                language_code='it-IT'
            )
        else:
            return texttospeech.VoiceSelectionParams(
                name='it-IT-Neural2-A',
                language_code='it-IT',
                ssml_gender=SsmlVoiceGender.FEMALE
            )

     # Idioma Portugues
    elif language == 'pt':
        # VOCES DE VARONES
        if nombre == 'vasco':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-BR-Neural2-B',
                language_code='pt-BR'
            )
        elif nombre == 'paulo':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-BR-Wavenet-B',
                language_code='pt-BR'
            )
        elif nombre == 'luis':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-PT-Wavenet-B',
                language_code='pt-PT'
            )
        # VOCES DE DAMAS  
        elif nombre == 'amalia':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-PT-Wavenet-A',
                language_code='pt-PT'                
            )
        elif nombre == 'mariza':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-PT-Standard-D',
                language_code='pt-PT'
            )
        elif nombre == 'ivete':
            return texttospeech.VoiceSelectionParams(                        
                name='pt-BR-Wavenet-C',
                language_code='pt-BR'
            )
        else:
            return texttospeech.VoiceSelectionParams(
                language_code='pt-BR',
                ssml_gender=SsmlVoiceGender.FEMALE
            )
    else:        
        return texttospeech.VoiceSelectionParams(
            language_code='es-ES',
            ssml_gender=SsmlVoiceGender.MALE
        )


if __name__ == '__main__':
    # Desactiva el modo de depuración
    app.debug = False
    # Ejecuta la aplicación con Gunicorn
    app.run()