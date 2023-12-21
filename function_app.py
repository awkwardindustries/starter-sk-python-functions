import azure.functions as func
import json
import logging
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.core_skills import WebSearchEngineSkill

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="evaluate_kid_friendliness")
async def evaluate_kid_friendliness(req: func.HttpRequest) -> func.HttpResponse:
    """
    An Azure Function triggerable by HTTP request. It accepts a JSON body
    that includes a general location. The input is passed to Semantic Kernel
    and any configured plugins before determining a response back to the
    user.
    params:
        req : func.HttpRequest
            The originating HTTP request triggering the function including a
            JSON body with a `location` parameter (e.g., 
            `{ "location": "Jackson Heights Queens, NY" }`)
    returns:
        func.HttpResponse
            An HTTP response with a JSON value representing the response from
            the LLM after processing through the Semantic Kernel plugins (e.g.,
            `{ "result": "Kid-friendliness rating for Jackson Heights: 4" }`)
    raises:
        an error if required environment variables have not been set (through
        the application settings)
    """
    # Assign the location in which we're interested to determine kid friendliness
    location = req.params.get('location')
    if not location:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            location = req_body.get('location')
    if not location:
        return func.HttpResponse(
            "Please pass a `location` on the query string or in the request body",
            status_code=400
        )

    logging.info(f'Running the Kid Friendliness Evaluator for {location}')

    logging.info('Checking for Azure OpenAI and Bing Search settings...')

    aoai_deployment_name = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    aoai_endpoint = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    aoai_api_key = os.environ["AZURE_OPEN_AI__API_KEY"]
    bing_api_key = os.environ["AZURE_BING_SEARCH__API_KEY"]

    logging.info('Initializing the Semantic Kernel...')

    # Setup logging for semantic_kernel.kernel to DEBUG for all the details
    logging.getLogger("kernel").setLevel(logging.DEBUG)
    # Initialize the kernel
    kernel = sk.Kernel()
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
    search_engine_connector = BingConnector(api_key = bing_api_key)
    kernel.import_skill(WebSearchEngineSkill(search_engine_connector), "WebSearch")
        
    logging.info('Loading custom plugins...')

    # Load custom plugins
    plugins_directory = "./plugins"
    kid_friendliness_plugin = kernel.import_semantic_skill_from_directory(
        plugins_directory, "KidFriendlinessPlugin"
    )

    logging.info('Processing the request...')

    # Run!
    variables = sk.ContextVariables()
    variables["input"] = location
    variables["searchQuery"] = f'places in {location}'
    variables["num_results"] = '4'
    result = await kernel.run_async(
        kid_friendliness_plugin["Evaluate"],
        input_vars = variables,
    )

    logging.info('Returning the result as JSON.')
    return func.HttpResponse(
        json.dumps(result.result),
        mimetype="application/json",
    )
