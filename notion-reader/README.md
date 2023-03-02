Notion Reader
=============

Retrieve a database from notion.

## Before you use

```
pip install -r requirements.txt
```

## Usage

### Set Notion token

```
export NOTION_TOKEN=<token>
```

### Find the database id

Open the notion database in your browser first. You can find database id from the URL like this.

`https://www.notion.so/cloudnativedays/<database id>?v=<something>`

For example,

`https://www.notion.so/cloudnativedays/cdbea8502c0c461a83233dad1d41333a?v=b3379832fd1a4fdd9f173cdd947c9808`

In this case, `cdbea8502c0c461a83233dad1d41333a` is database id.

### Run

```
python notion.py <database id>
```
