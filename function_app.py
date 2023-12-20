import azure.functions as func
import logging
import os
import semantic_kernel as sk
from semantic_kernel.core_skills import TimeSkill
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger_sample")
def http_trigger_sample(req: func.HttpRequest) -> func.HttpResponse:
    """
    An Azure Function triggerable by HTTP request for example.
    params:
        req : func.HttpRequest
            The originating HTTP request triggering the function
    returns:
        func.HttpResponse
            An HTTP response with a text description of the outcome of the 
            function invocation
    """
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="orchestrate_chat_completion")
async def orchestrate_chat_completion(req: func.HttpRequest) -> func.HttpResponse:
    """
    An Azure Function triggerable by HTTP request. It accepts a JSON body
    that includes the user's input. The input is passed to Semantic Kernel
    and any configured plugins before determining a response back to the
    user.
    params:
        req : func.HttpRequest
            The originating HTTP request triggering the function including a
            JSON body with a `user_prompt` parameter (e.g., 
            `{ "user_prompt": "Tell me about turtles." }`)
    returns:
        func.HttpResponse
            An HTTP response with a JSON value representing the response from
            the LLM after processing through the Semantic Kernel plugins (e.g.,
            `{ "response": "Where to begin? Turtles rock." }`)
    raises:
        an error if required environment variables have not been set (through
        the application settings)
    """
    logging.info('Checking Azure OpenAI settings...')

    aoai_deployment_name = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    aoai_endpoint = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    aoai_api_key = os.environ["AZURE_OPEN_AI__API_KEY"]

    # Initialize the kernel with extra logging detail
    kernel = sk.Kernel( log = sk.NullLogger() )
    # Add Azure OpenAI for chat completions
    kernel.add_chat_service(
        "chat_completion",
        AzureChatCompletion(
            deployment_name = aoai_deployment_name,
            endpoint = aoai_endpoint,
            api_key = aoai_api_key,
        ),
    )
    # Load built-in plugins
    time = kernel.import_skill(TimeSkill())
    # Load plugins
    # plugins_directory="./plugins"
    # sample_plugin = kernel.import_semantic_skill_from_directory(plugins_directory, "SamplePlugin")

    # Run!
    currentDate = await kernel.run_async(time["today"])
    return func.HttpResponse(f"Hello! The current date is {currentDate}.")
