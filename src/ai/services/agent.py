# main.py
import json
from google import genai
from google.genai import types
from tools.tools import edit_file_definition, list_files_definition, read_file_definition


class ShrekAgent:
    def __init__(self):
        self.client = genai.Client()  # GOOGLE_API_KEY env dan o'qiydi
        self.model = "gemini-2.0-flash"
        self.tools = [
            edit_file_definition,
            list_files_definition,
            read_file_definition,
        ]

    def get_message(self):
        try:
            user_input = input()
            return user_input, bool(user_input)
        except EOFError as e:
            return "", str(e)

    def run(self):
        conversation = []
        print("Chat with Gemini (use 'ctrl-d' to quit)")
        read_user_input = True

        while True:
            if read_user_input:
                print(colored("You: ", "blue"), end="")
                user_input, ok = self.get_message()
                if not ok:
                    break
                conversation.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=user_input)],
                    )
                )

            response = self.run_inference(conversation)

            # Assistant javobini history ga qo'sh
            conversation.append(
                types.Content(
                    role="model",
                    parts=response.candidates[0].content.parts,
                )
            )

            tool_results = []
            for part in response.candidates[0].content.parts:
                if part.text:
                    print(colored("Gemini:", "yellow"), f" {part.text}")
                elif part.function_call:
                    fc = part.function_call
                    input_data = json.dumps(dict(fc.args))
                    result_part = self.execute_tool(fc.name, input_data)
                    tool_results.append(result_part)

            if not tool_results:
                read_user_input = True
                continue

            read_user_input = False
            # Tool natijalarini user turn sifatida qo'sh
            conversation.append(
                types.Content(
                    role="user",
                    parts=tool_results,
                )
            )

    def execute_tool(self, name, input_data):
        for tool in self.tools:
            if tool.name == name:
                print(colored("tool:", "green"), f" {name}({input_data})")
                result, error = tool.function(input_data)
                if error:
                    return types.Part(
                        function_response=types.FunctionResponse(
                            name=name,
                            response={"error": error},
                        )
                    )
                return types.Part(
                    function_response=types.FunctionResponse(
                        name=name,
                        response={"result": result},
                    )
                )

        return types.Part(
            function_response=types.FunctionResponse(
                name=name,
                response={"error": "tool not found"},
            )
        )

    def run_inference(self, conversation):
        # Toollarni Gemini FunctionDeclaration formatiga o'tkazish
        gemini_tools = []
        for tool in self.tools:
            schema = tool.input_schema
            # Gemini uchun properties ni olish
            properties = {}
            for prop_name, prop_info in schema.get("properties", {}).items():
                properties[prop_name] = types.Schema(
                    type=prop_info.get("type", "string").upper(),
                    description=prop_info.get("description", ""),
                )

            fn_decl = types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=types.Schema(
                    type="OBJECT",
                    properties=properties,
                    required=schema.get("required", []),
                ),
            )
            gemini_tools.append(fn_decl)

        config = types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=gemini_tools)],
            temperature=0,
        )

        return self.client.models.generate_content(
            model=self.model,
            contents=conversation,
            config=config,
        )


def main():
    shrek_agent = ShrekAgent()
    shrek_agent.run()


if __name__ == "__main__":
    main()
