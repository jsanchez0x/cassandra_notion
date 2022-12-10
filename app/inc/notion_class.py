# -*- coding: UTF-8 -*-

import inc
import requests
import json

class Notion:

    def compose_basic_header_request(self) -> dict:
        # Generates a dictionary with the basic headers to make a request to the API.

        headers = {
            "accept": "application/json",
            "Notion-Version": inc.cfg.notion_api_version,
            "Authorization": "Bearer " +  inc.cfg.notion_api_key
        }

        return headers


    def get_integration_id(self) -> str:
        # Get unique ID for the integration registered in Notion.

        url = "https://api.notion.com/v1/users/me"
        response = requests.get(url, headers=self.compose_basic_header_request())
        data = json.loads(response.text)
        integration_id = data['id']

        return integration_id


    def get_pages(self) -> list[int]:
        # It connects to a database in Notion that has a field of type url and called "URL".
        # Here you specify the pages that Cassandra will access. These pages will be returned.

        url = "https://api.notion.com/v1/databases/" + inc.cfg.notion_database_id + "/query"
        payload = {"page_size": 100}
        database_response = requests.post(url, json=payload, headers=self.compose_basic_header_request())
        database_response_data = json.loads(database_response.text)
        pages_ids = []

        # Iteration through the different table rows
        for database_row in database_response_data['results']:
            url = database_row['properties']['URL']['url']
            if url != None:
                possible_id = url.split('-')[-1]

                url = "https://api.notion.com/v1/pages/" + possible_id
                page_response = requests.get(url, headers=self.compose_basic_header_request())

                # If a code 200 is returned, it means that Notion recognizes the page and Cassandra has access to it.
                if page_response.status_code == 200:
                    page_response_data = json.loads(page_response.text)
                    archived = page_response_data['archived']

                    # The page is checked to ensure that it is not archived.
                    if not archived:
                        pages_ids.append(possible_id)

        return pages_ids


    def get_children_blocks(self, block_id: str) -> list:
        # Take the children of a parent block.
        url = "https://api.notion.com/v1/blocks/" + block_id + "/children?page_size=100"
        blocks_response = requests.get(url, headers=self.compose_basic_header_request())
        blocks_response_data = json.loads(blocks_response.text)

        try:
            children_blocks = blocks_response_data['results']

        except KeyError:
            children_blocks = []

        return children_blocks


    def create_block(self, parent_block: str, type: str = 'quote', text_content: str = '') -> str:

        url = "https://api.notion.com/v1/blocks/" + parent_block + "/children"
        # It is necessary to add the content-type header because the request is a PATCH
        headers = self.compose_basic_header_request()
        headers['content-type'] = 'application/json'

        requests_data = {
            "children": [{
                "object": "block",
                "type": type,
                "quote": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": { "content": text_content },
                            "annotations": { "italic": True }
                        }
                    ],
                    "color": "yellow_background"
                }
            }]
        }

        creation_response = requests.patch(url, json.dumps(requests_data), headers=headers)
        creation_response_data = json.loads(creation_response.text)

        try:
            block_id = creation_response_data['results'][0]['id']

        except KeyError:
            block_id = ''

        return block_id


    def update_block(self, block_id: str, type: str = 'quote', text_content: str = '') -> bool:
        # Updates the text of a block.

        url = "https://api.notion.com/v1/blocks/" + block_id
        # It is necessary to add the content-type header because the request is a PATCH
        headers = self.compose_basic_header_request()
        headers['content-type'] = 'application/json'

        payload = {
            type: {
                "rich_text": [{
                    "text": { "content": text_content }
                }]
            }
        }

        update_response = requests.patch(url, json=payload, headers=headers)

        if update_response.status_code == 200:
            return True
        else:
            return False


    def delete_block(self, block_id: str) -> bool:
        # Deletes a block indicated by its ID.
        url = "https://api.notion.com/v1/blocks/" + block_id
        response = requests.delete(url, headers=self.compose_basic_header_request())

        if response.status_code == 200:
            return True
        else:
            return False


    def get_cassandra_blocks(self) -> list[int]:
        # Returns a dictionary with the id of all blocks for Cassandra and the text they contain.
        # The blocks must be of type callout, must have an emoji of a woman and must not have been last edited by Cassandra herself.

        cassandra_blocks = []

        for page_id in self.get_pages():
            page_blocks = self.get_children_blocks(page_id)

            # TODO: Implement pagination!!!!!!

            for block in page_blocks:
                try:

                    block_id = block['id']
                    block_last_edited_time = block['last_edited_time']
                    block_last_edited_user_id = block['last_edited_by']['id']

                    block_callout_content = block['callout']
                    icon_type = block_callout_content['icon']['type']
                    icon = block_callout_content['icon'][icon_type]

                    # Emoji checks and last editor.
                    if b'\\U0001f469' in icon.encode('unicode-escape') and block_last_edited_user_id != self.get_integration_id():

                        # Checking the children to see if it already has the Cassandra quote block.
                        children_blocks = self.get_children_blocks(block_id)

                        for son_block in children_blocks:
                            son_block_created_by = son_block['created_by']['id']

                            if son_block_created_by == self.get_integration_id():
                                self.delete_block(son_block['id'])

                        # TODO: Test last edited time.

                        # If the text is formatted, Notion splits it into a dictionary and needs to be reconstructed.
                        block_callout_text = ""
                        for text_part in block_callout_content['rich_text']:
                            plain_text = text_part['plain_text']
                            block_callout_text += plain_text

                        cassandra_block = {"id": block_id, "text":block_callout_text}
                        cassandra_blocks.append(cassandra_block)

                except KeyError:
                    continue

        return cassandra_blocks


    def get_ia_response(self, prompt: str) -> str:
        # Loads the AI class to request a response to the defined API.

        openai = inc.openai_class.OpenAI()
        ia_response = openai.get_model_response(prompt)

        return ia_response


    def write_ia_response(self, block_data: dict) -> bool:
        # Write in the Cassandra callout block in Notion the AI response.
        # It will use a quote format with yellow background.

        block_id = self.create_block(block_data['id'], "quote", "Waiting IA response...")
        self.update_block(block_id, text_content=self.get_ia_response(block_data['text']))