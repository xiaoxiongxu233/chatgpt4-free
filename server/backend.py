from json     import dumps, loads
from datetime import datetime
from requests import get, post
from flask    import request
from threading import Thread

from server.config import *

class Backend_Api:
    def __init__(self, app) -> None:
        self.app    = app
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation, 
                'methods': ['POST']
            },
        }
    
    def _conversation(self):

        try:
            jailbreak       = request.json['jailbreak']
            internet_access = request.json['meta']['content']['internet_access']
            is_creative_bot = request.json['meta']['content']['is_creative_bot']
            is_detail_bot = request.json['meta']['content']['is_detail_bot']
            _conversation   = request.json['meta']['content']['conversation']
            prompt          = request.json['meta']['content']['parts'][0]
            current_date    = datetime.now().strftime("%Y-%m-%d")
            system_message  = f'Вы - GPT-3.5, также известный как ChatGPT, большая языковая модель, обученная OpenAI. Следуйте строго инструкциям пользователя. Крайняя дата знаний: Неограничено. Current date: {current_date}'
            
            if '0040' in request.json['model']:
                system_message  = f'Вы - GPT-4, новейшее поколение серии OpenAI GPT. Следуйте строго инструкциям пользователя. Крайняя дата знаний: Неограничено. Current date: {current_date}'  
            
            extra = []
            if internet_access:
                search = get('https://ddg-api.herokuapp.com/search', params = {
                    'query': prompt["content"],
                    'limit': 3,
                })

                blob = ''

                for index, result in enumerate(search.json()):
                    blob += f'[{index}] "{result["snippet"]}"\nURL:{result["link"]}\n\n'

                date = datetime.now().strftime('%d/%m/%y')

                if is_creative_bot:
                    if is_detail_bot:
                        blob += f'Current date: {date}\n\nInstructions: Using the Internet search results, write a detailed answer as you want (in any style), but following the concept. If the user asks for your opinion in the answers, then you write like this - My opinion: here is your opinion about the information. If the user said to leave links to sources, then you must leave links to sources [[Source](URL)], if the sources are repeated, then specify individual objects. Try to take into account the history of messages, unless they went on another topic of conversation. Always use Russian.'
                    else:
                        blob += f'Current date: {date}\n\nInstructions: Using the Internet search results, write the shortest possible answer the way you want (in any style), but following the concept. If the user asks for your opinion in the answers, then you write like this - My opinion: here is your opinion about the information. If the user said to leave links to sources, then you must leave links to sources [[Source](URL)], if the sources are repeated, then specify individual objects. Try to take into account the history of messages, unless they went on another topic of conversation. Always use Russian.'
                else:
                    if is_detail_bot:
                        blob += f'Current date: {date}\n\nInstructions: Using the search results on the Internet, write the most informative and understandable answer with details. If the user asks for your opinion in the answers, then you write like this - My opinion: here is your opinion about the information. If the user said to leave links to sources, then you must leave links to sources [[Source](URL)], if the sources are repeated, then specify individual objects. Try to take into account the history of messages, unless they went on another topic of conversation. Always use Russian.'
                    else:
                        blob += f'Current date: {date}\n\nInstructions: Using the Internet search results, write the shortest and most understandable answer. If the user asks for your opinion in the answers, then you write like this - My opinion: here is your opinion about the information. If the user said to leave links to sources, then you must leave links to sources [[Source](URL)], if the sources are repeated, then specify individual objects. Try to take into account the history of messages, unless they went on another topic of conversation. Always use Russian.'

                extra = [{'role': 'user', 'content': blob}]

            conversation = [{'role': 'system', 'content': system_message}] +  extra  + special_instructions[jailbreak] +  _conversation + [prompt]
            
            headers = {
                'authority': 'www.sqlchat.ai',
                'accept': '*/*',
                'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
                'content-type': 'text/plain;charset=UTF-8',
                'origin': 'https://www.sqlchat.ai',
                'referer': 'https://www.sqlchat.ai/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }

            data = {
                'messages': conversation,
                'openAIApiConfig':{
                    'key':'',
                    'endpoint':''
                }
            }

            gpt_resp = post('https://www.sqlchat.ai/api/chat', headers=headers, json=data, stream=True)

            # headers = {
            #     'authority': 'www.t3nsor.tech',
            #     'accept': '*/*',
            #     'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            #     'cache-control': 'no-cache',
            #     'content-type': 'application/json',
            #     'origin': 'https://www.t3nsor.tech',
            #     'pragma': 'no-cache',
            #     'referer': 'https://www.t3nsor.tech/',
            #     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            #     'sec-ch-ua-mobile': '?0',
            #     'sec-ch-ua-platform': '"macOS"',
            #     'sec-fetch-dest': 'empty',
            #     'sec-fetch-mode': 'cors',
            #     'sec-fetch-site': 'same-origin',
            #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            # }

            # gpt_resp = post('https://www.t3nsor.tech/api/chat', headers = headers, stream = True, json = {
            #     'model': {
            #         'id'   : 'gpt-3.5-turbo', 
            #         'name' : 'Default (GPT-3.5)'
            #     },
            #     'messages'  : conversation,
            #     'key'       : '',
            #     'prompt'    : system_message
            # })

            def stream():
                answer = ''
                for chunk in gpt_resp.iter_content(chunk_size=1024):
                    try:
                        answer += chunk.decode()
                        yield chunk.decode()

                    except GeneratorExit:
                        break
                    
                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_next)
                        continue
                
                # Thread(target=log, args = [ip_address, model, prompt['content'], answer]).start()
            
            return self.app.response_class(stream(), mimetype='text/event-stream')
        
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return {
                '_action' : '_ask',
                'success' : False,
                "error"   : f"Ошибка {str(e)}"}, 400
