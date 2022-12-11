# Cassandra Notion bot (powered by GPT-3)

## Bots
Cassandra is the name given to this project, which consists of a container that executes a Python program.

This program monitors the pages indicated in Notion, which have a callout type block and that the emoji is a woman. The text indicated in this block will be sent to the Davinci model of GPT-3 created by OpenAI.

The response will be added to the callout block in Notion as another quote block.


## Requeriments
- Docker
- Create a [Notion integration](https://www.notion.so/my-integrations) for API Key.
- Create a [OpenAI API key](https://beta.openai.com/account/api-keys)


## Preparation in Notion
Cassandra needs a database in order to work. This database specifies the URLs of the pages to be monitored.

Now what we will do is to create a database and get its ID to configure it in the container.

1. Create a database. Name the database and the page as you wish, for example "Cassandra DB".
2. Create a field in the database of type URL and call it "URL" (without the quotes). You can add as many fields as you want, but this one must be created.
3. In the database, click on the three dots at the top right and click on "Copy link to view". The link will look something like this, we are interested in the part in bold: *notion.so/***966e887a3048453c86bec11f4bbffcee***?v=150787ea6d9a47a6acedd40ecb49cad7*
4. Add the integration to a page. Three dots at the top right of the site, under Connections.

![create_database_add_connection](https://user-images.githubusercontent.com/49794514/206880697-092874a3-8aee-4073-bca3-693c4d483065.gif)


To add a page to the database you must click on the three dots at the top of the web and click on "Copy link" inside the page you want to add. This link must be pasted into the URL field of the database we created earlier.

Don't forget to add Cassandra to the page, in the same way as in step 4 above.


## Running the container

### Necessary environment variables
| Name                        | Mandatory | Description                                                               |
| --------------------------- | --------- | --------------------------------------------------------------------------|
| NOTION_API_KEY              | **Yes**   | Required to work with Notion integration.                                 |
| NOTION_DB_ID                | **Yes**   | Required to use the database (more info in Preparation in Notion).        |
| OPENAI_API_KEY              | **Yes**   | Required in order to use the OpenAI GPT-3 model.                          |


### Create and run the image
You must create a file in "utils" directory called env.list, in this file you must define the system variables indicated below. To start a container with environment variables there is more information [here](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file).

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
The definition of task scheduling is done in the _utils/crontab.txt_ file.
You can enable or disable task scheduling with the following command:
```bash
./utils/container.sh scheduling
```

#### b. Manually
It is possible to manually run Cassandra with the following command:
```bash
./utils/container.sh cassandra
```

### Some support commands

You can open a shell (sh) to the container with the following helper:
```bash
./utils/container.sh sqlite
./utils/container.sh shell
```


## Credits
To [Notion](https://www.notion.so/) for their fantastic application and for opening their API to the public.

To [OpenAI](https://openai.com/) for Davinci, a spectacular GPT-3 model.
