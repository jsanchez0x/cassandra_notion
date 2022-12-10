# -*- coding: utf-8 -*-

import inc

def main():
    notion = inc.notion_class.Notion()
    for block in notion.get_cassandra_blocks():
        writed = notion.write_ia_response(block)

if __name__ == "__main__":
    main()
