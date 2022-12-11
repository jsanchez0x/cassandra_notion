# Cassandra Notion bot (powered by GPT-3)

## What is this?

Cassandra is the name given to this proof of concept, which consists of a Docker container that executes a Python program.

This program monitors the pages accessed by the integration, which have a callout type block and the emoji is a woman. The text indicated in this block will be sent to the Davinci model of GPT-3 created by OpenAI as prompt.

The response will be added to the callout block in Notion as quote block.

![Cassandra test](https://user-images.githubusercontent.com/49794514/206881319-cd0cfcb3-d094-431b-9a83-e95ea78a8f59.gif)


## Requeriments

- Docker
- Create a [Notion integration](https://www.notion.so/my-integrations) for API Key.
- Create a [OpenAI API key](https://beta.openai.com/account/api-keys)


## Preparing Notion

All you have to do is add the integration to the page to be monitored. This is done through the three dots button at the top of the page, in the *Connections* section.


## Running the container

### 1. Necessary environment variables
| Name           | Description                                                        | Example                                          |
| -------------- | -------------------------------------------------------------------| -------------------------------------------------|
| NOTION_API_KEY | Required to work with Notion integration.                          | secret_eyHJKM45WEDIGHJBNIOPpwimvtyk748byk877ED   |
| OPENAI_API_KEY | Required in order to use the OpenAI GPT-3 model.                   | sk-pptbkiORt4679kbD358856dvcxQEsfgnlk007hbr5f45h |

You must create a file in *utils* directory called "**env.list**" (without the quotes), in this file you must define the system variables indicated below. The file should look like this:
>NOTION_API_KEY=secret_eyHJKM45WEDIGHJBNIOPpwimvtyk748byk877ED
>OPENAI_API_KEY=sk-pptbkiORt4679kbD358856dvcxQEsfgnlk007hbr5f45h

More information on how to start a Docker container with system variables [here](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file).


### 2. Create the Docker image
Thanks to the *container.sh* file many Docker commands have been simplified. To create the Docker image is as simple as running:
```bash
./utils/container.sh image
```


### 3. Run the Docker container
Running the container is done with this command:
```bash
./utils/container.sh run
```


### 4. Executing Cassandra

#### a. Through scheduled tasks
When the container is started, Cassandra is scheduled as defined in the _utils/crontab.txt_ file. This is the automatic way.

#### b. Manually
Using container.sh it is also possible to run manually:
```bash
./utils/container.sh cassandra
```


### Some support commands
You can open a shell to the container with the following helper:
```bash
./utils/container.sh sh
```


## Credits
To [Notion](https://www.notion.so/) for their fantastic application and for opening their API to the public.

To [OpenAI](https://openai.com/) for Davinci, a spectacular GPT-3 model.
