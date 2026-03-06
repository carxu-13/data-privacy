import ollama
import os

SANDBOX_DIR = "sandbox"

TOOLS = {
    "read_file": "Read a file from the sandbox directory."
}

def read_file(filename):
    path = os.path.join(SANDBOX_DIR, filename)

    if not os.path.exists(path):
        return "File not found."

    with open(path) as f:
        return f.read()


def call_tool(name, arg):
    if name == "read_file":
        return read_file(arg)

    return "Unknown tool."


SYSTEM_PROMPT = f"""
You are a helpful assistant with access to tools.

TOOLS:
read_file(filename) - Read a file from the sandbox directory.

If you want to use a tool, respond ONLY in this format:

TOOL: tool_name
ARG: argument

Otherwise respond normally.
"""


def run_agent(user_input):

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    content = response["message"]["content"]

    print("\nMODEL OUTPUT:")
    print(content)

    if "TOOL:" in content:

        lines = content.split("\n")
        tool = None
        arg = None

        for l in lines:
            if l.startswith("TOOL:"):
                tool = l.replace("TOOL:", "").strip()

            if l.startswith("ARG:"):
                arg = l.replace("ARG:", "").strip()

        if tool and arg:
            result = call_tool(tool, arg)

            print("\nTOOL RESULT:")
            print(result)

            return result

    return content


while True:

    user = input("\nUser: ")

    if user == "exit":
        break

    run_agent(user)