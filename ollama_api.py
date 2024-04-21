import ollama

class OllamaAPI:
    def __init__(self, model, sysprompt) -> None:
        self.model = model
        self.sys = {
                        'role': 'system',
                        'content': sysprompt,
                    }
    def get_response(self, content, stream=False):
        response =  ollama.chat(
                        model=self.model, 
                        messages=[self.sys, 
                                    {
                                        'role': 'user',
                                        'content': content
                                    }],
                        stream=stream)
        if response is None:
            return ''
        elif not stream:
            return response['message']['content']
        else:
            out = ''
            for chunk in response:
                text = chunk['message']['content']
                out += text
                print(text, end='', flush=True)
            return out