# Starter Project for Azure Function (Python) with Semantic Kernel

## Resources

- Azure OpenAI Service
- Azure Bing Search
- Azure Functions

## Build and run

### 0. Choose your development environment

#### (Option) Local Development

You can develop in this project locally on your own machine. You'll need to:
1. If you choose to run the project locally within a devcontainer, all necessary software and libraries will be included and run within the devcontainer. If you choose to run locally without a devcontainer, you will need to ensure that you have the necessary software and libraries installed. You will need:
   - [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
   - [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools)
   - [Python 3.9 or greater](https://wiki.python.org/moin/BeginnersGuide/Download)
   - [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
   - Visual Studio Code extensions (optional, but expected in documentation)
      - Azure Functions (`ms-azuretools.vscode-azurefunctions`)
      - Azurite (`Azurite.azurite`)
      - Azure Storage (`ms-azuretools.vscode-azurestorage`)
      - Python (`ms-python.python`)
      - REST Client (`humao.rest-client`)
      - Semantic Kernel Tools (`ms-semantic-kernel.semantic-kernel`)
1. Clone this repository to your local machine.

#### (Option) GitHub Codespaces with devcontainers

Alternatively, you can use GitHub Codeswpaces with devcontainers. This method allows you to use a pre-configured development environment and avoids the need to install anything on your local machine. You'll need to:

1. Navigate to the repository on GitHub.
1. Click on the 'Code' button and then select 'Open with Codespaces'.
1. Click on the '+ New codespace' button.
1. After a few minutes, your codespace should be ready, and you'll be taken to an online version of Visual Studio Code.

This codespace is a full-fledged development environment, and you can write and run your code just like you would on your local machine. The devcontainer configuration in the repository sets up all the necessary software and libraries for you.

### 1. Setup your environment

1. Copy the provided `local.settings.json.example` to a new `local.settings.json` file.
1. If you have not already created your Azure resources, you'll need to create them now. Otherwise, you'll just need the information available from the deployments, keys, and endpoints.
   - [Create and deploy an Azure OpenAI Service resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
   - [Create a Bing search resource](https://portal.azure.com/#create/microsoft.bingsearch)
1. Correctly assign the following in your `local.settings.json` based on your Azure OpenAI Service and the chat completion model deployment you want to use: 
   - `AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME`
   - `AZURE_OPEN_AI__ENDPOINT`
   - `AZURE_OPEN_AI__API_KEY`
   - `AZURE_BING_SEARCH__API_KEY`
1. Create a Python virtual environment (venv). In your Visual Studio Code terminal at the project root, execute the command:
   ```sh
   python -m venv .venv
   ```
1. Activate the Python virtual environment.  In your Visual Studio Code terminal at the project root, execute the command:
   ```sh
   source .venv/bin/activate
   ```

### 2. Debug

1. Start the Azurite services
   - In Visual Studio Code, open the command palette (**F1**) and select **Azurite: Start** to start the Blob, Queue, and Table services.
1. Debug the Azure Functions
   - In Visual Studio Code, press **F5**. You should see a terminal window appear that will install any requirements (if not already installed), and run the Azure Functions Core Tools host. When ready, it should list the functions available:
      ```sh
      # EXAMPLE OUTPUT WHEN READY...
      Azure Functions Core Tools
      Core Tools Version:       4.0.5455 Commit hash: N/A  (64-bit)
      Function Runtime Version: 4.27.5.21554
      
      [2023-12-20T15:31:14.052Z] Customer packages not in sys path. This should never happen! 
      [2023-12-20T15:31:17.231Z] Worker process started and initialized.
      
      Functions:
      
              http_trigger_sample:  http://localhost:7071/api/http_trigger_sample
      
              orchestrate_chat_completion:  http://localhost:7071/api/orchestrate_chat_completion
      
      For detailed output, run func with --verbose flag.
      [2023-12-20T15:31:22.442Z] Host lock lease acquired by instance ID '00000000000000000000000068F265FA'.
      ```
   - Visual Studio Code should be attached to the process at this time, so you may place breakpoints where needed within your function code.
1. Stop debugging
   - You can disconnect the debugging process, or you can `<CTRL-C>` kill the *func host start* terminal window. That will ensure the underlying Functions Host is stopped, and the debugging process should also be released.
   - Note that you may see errors at the time of the forced shutdown, but that is most likely due only to the shutdown.

#### Troubleshooting

##### Popup: Failed to verify "AzureWebJobsStorage" connection specified in "local.settings.json". Is the local emulator installed and running?

You may cancel this popup and address the issue with the following.

If you're debugging locally with the Azurite emulator, make sure your `local.settings.json` file's `AzureWebJobsStorage` is set to `UseDevelopmentStorage=true` and the Azurite service is started (**F1** then **Azurite: Start**).

If you're using a deployed Azure Storage Account, verify the connection string assigned to your `AzureWebJobsStorage` is correct and that the storage account is accessible from your local machine.

##### Popup: Could not find the task 'func: host start'.

You may cancel this popup and address the issue with the following.

You may not have installed the Azure Functions extension in Visual Studio Code, or it may not be configured if running in the devcontainer or GitHub codespaces. Press **F1** then **Tasks: Run Task** then select **func: extensions install** or (if it is not visible) navigate to it by selecting the **func** directory then selecting **func: extensions install**.

### 3. Evaluate

Open the `tests.http` file in Visual Studio Code. If the *REST Client* extension is installed as expected, there should be a **Send Request** link above the HTTP requests to trigger the functions. Click **Send Request** above the function you wish to trigger.

The terminal window will display any output from the Azure Function, and the HTTP response will be presented in a new window.
