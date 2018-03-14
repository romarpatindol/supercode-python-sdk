# Supercode Python SDK
**Supercode Python SDK** is a wrapper around the Supercode API

**Step 1:**
- Get this supercode python sdk and treat it as part of your library where you can import it.

**Step 2:**
- Sample supercode usage: [**Get Trello Cards**](https://git.io/vxkeN)
```
import supercode

results = supercode.call(
    <SUPERCODE_FUNCTION_ID>,
    <SUPERCODE_API_KEY>,
    trello_api_key=<TRELLO_API_KEY>,
    trello_token=<TRELLO_TOKEN>,
    trello_username=<TRELLO_USERNAME>,
    trello_url=<TRELLO_URL>,
    trello_list_name=<TRELLO_LIST_NAME>,
    trello_label_name=<TRELLO_LABEL_NAME> or "all",
    trello_card_fields=<TRELLO_CARD_FIELDS>
)
print(results)
```
