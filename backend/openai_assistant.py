import openai
from cat_api import CatAPI
import os
import json
from dotenv import load_dotenv
import markdown

load_dotenv()

class OpenAIAssistant:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
        self.assistant = openai.beta.assistants.retrieve(assistant_id)
        self.cat_api = CatAPI()
        self.thread = openai.beta.threads.create()

    def get_response(self, user_input):
        openai.beta.threads.messages.create(thread_id=self.thread.id, role="user", content=user_input) # adds user input to current thread
        run = openai.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id) # starts a new run on the assistant

        while run.status != "completed":
            run = openai.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id) # update info for run
            if run.status == "requires_action":
                for tool_call in run.required_action.submit_tool_outputs.tool_calls: # checks if any tools were needed
                    if tool_call.function.name == "get_cat": # checks if the "get_cat" tool is used, in case more functions added in the future
                        try:
                            args = json.loads(tool_call.function.arguments)
                            breed, limit = args.get('breed'), args.get('limit', 1)
                            output = json.dumps(self.cat_api.get_cats(breed, limit))
                        except Exception as e:
                            output = json.dumps([])

                        openai.beta.threads.runs.submit_tool_outputs( # submits cat images to the tool outputs
                            thread_id=self.thread.id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": output
                            }]
                        )

        messages = openai.beta.threads.messages.list(thread_id=self.thread.id) # obtain output
        return markdown.markdown(messages.data[0].content[0].text.value)