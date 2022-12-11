# Cassandra Notion bot (powered by GPT-3)

## What is this?
Cassandra is the name given to this proof of concept, which consists of a Docker container that executes a Python program.

This program monitors the pages indicated in Notion, which have a callout type block and the emoji is a woman. The text indicated in this block will be sent to the Davinci model of GPT-3 created by OpenAI as prompt.

The response will be added to the callout block in Notion as quote block.

![Cassandra test](https://user-images.githubusercontent.com/49794514/206881319-cd0cfcb3-d094-431b-9a83-e95ea78a8f59.gif)


## Requeriments
- Docker
- Create a [Notion integration](https://www.notion.so/my-integrations) for API Key.
- Create a [OpenAI API key](https://beta.openai.com/account/api-keys)


## Preparation in Notion
Cassandra needs a database in order to work. This database specifies the URLs of the pages to be monitored.  
Now what we will do is to create a database and get its ID to configure it in the container.

1. Create a database. Name the database and the page as you wish, for example "Cassandra DB".
2. Create a field in the database of **type URL** and call it **"URL" (without the quotes)**. You can add as many fields as you want, **but this one must be created**.
3. In the database, click on the three dots at the top right and click on *Copy link to view*. The link will look something like this, we are interested in the part in bold: *notion.so/***3459a2378689d30278583g9237r5176p***?v=150787e...*
4. Add the integration to a page. Three dots at the top right of the site, under *Connections*.

![Creating the database, the URL field, copying the database link and activating the integration.](https://user-images.githubusercontent.com/49794514/206880697-092874a3-8aee-4073-bca3-693c4d483065.gif)


To add a page to the database you must click on the three dots at the top of the web and click on *Copy link* inside the page you want to add. This link must be pasted into the URL field of the database we created earlier.

**Don't forget to add Cassandra to the page**, in the same way as in step 4 above.


## Running the container

### Necessary environment variables
| Name                        | Mandatory | Description                                                               |
| --------------------------- | --------- | --------------------------------------------------------------------------|
| NOTION_API_KEY              | **Yes**   | Required to work with Notion integration.                                 |
| NOTION_DB_ID                | **Yes**   | Required to use the database (more info in Preparation in Notion).        |
| OPENAI_API_KEY              | **Yes**   | Required in order to use the OpenAI GPT-3 model.                          |

You must create a file in *utils* directory called "**env.list**" (without the quotes), in this file you must define the system variables indicated below. The file should look like this: 
>NOTION_API_KEY=secret_eyHJKM45WEDIGHJBNIOPpwimvtyk748byk877ED  
>NOTION_DB_ID=3459a2378689d30278583g9237r5176p  
>OPENAI_API_KEY=sk-pptbkiORt4679kbD358856dvcxQEsfgnlk007hbr5f45h


More information on how to start a Docker container with system variables [here](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file). 


### Create and run the image

The container image is created with this command:
```bash
./utils/container.sh image
```

And it is executed with the following command:
```bash
./utils/container.sh run
```


### Executing Cassandra

#### a. Through scheduled tasks
The container when started will schedule Cassandra execution as defined in the _utils/crontab.txt_ file.

#### b. Manually
It is possible to manually run Cassandra with the following command:
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
