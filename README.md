# Print-on-demand API: a picture in, a buy link out (no account, no key)

Put your users' pictures on a shirt, hoodie, sweatshirt, polo, quarter-zip, cap, trucker hat, tumbler or tote with **one request**, and get back the page where they see it on the item, pick sizes and pay.

[1211](https://1211holding.com) prints each order one at a time, ships it free to US addresses, takes the payment and handles sales tax and support. There is nothing to sign up for: no account, no API key, no store to set up, no inventory. Your user pays on 1211's page; there is no charge to you.

## Quickstart

```bash
curl -s https://1211holding.com/v1/designs \
  -H 'Content-Type: application/json' \
  -d '{"item": "hoodie", "color": "Black",
       "front": {"art": {"url": "https://example.com/your-image.png"}, "placement": "center"},
       "size": "L", "ref": "your-app"}'
```

The answer (status 201) carries `url` - the page to send your user to - plus a picture of the result (`mockup`), how big each side prints (`sides`), the price (`price.usd`, US shipping included) and any `problems` that did not stop the design.

### Python

```
pip install merch1211
```

```python
import merch1211

d = merch1211.create_design("hoodie", image_url="https://example.com/art.png", color="Black", front="center", size="L")
print(d["url"])

up = merch1211.upload("drawing.png")                      # a file on disk
print(merch1211.create_design("tee", upload_id=up["upload"])["url"])
```

### JavaScript (browser or Node 18+)

```
npm install merch1211
```

```js
import { createDesign, upload } from "merch1211";

const d = await createDesign({ item: "hoodie", imageUrl: "https://example.com/art.png", color: "Black", front: "center" });
window.open(d.url);

const up = await upload(document.getElementById("pic").files[0]);   // <input type="file" id="pic">
```

### No code at all

A link opens the same page with the picture already on the item - anyone can write it, including an AI assistant in a chat:

```
https://1211holding.com/make?item=hoodie&color=Black&art=https://example.com/your-image.png&front=center&size=L
```

## What you can print

Items, colours, sizes, print sizes and today's prices are always live at [GET /v1/catalog](https://1211holding.com/v1/catalog). A shirt's front prints small on the left chest by default, or big and centered with `front=center` (`"placement": "center"` in the API); a back prints large. About 150 pixels per printed inch prints well; 300 is sharp.

## Limits and rules

- Per address per hour: 30 designs, 20 uploads, 300 catalog reads. Calls from your users' browsers count against each user's own address (the API allows any origin).
- Only art your user made or has permission to print; they confirm it when they buy.
- Never check out for anyone: the person pays on 1211's page. Shipping is to US addresses.

## Reference

- Quickstart and errors: https://1211holding.com/developers
- OpenAPI 3.1: https://1211holding.com/openapi.json
- For AI assistants: https://1211holding.com/for-ai and https://1211holding.com/llms.txt

## This repository

- `clients/python` - the `merch1211` package on PyPI (standard library only)
- `clients/js` - the `merch1211` package on npm (fetch + FormData only, with TypeScript types)
- `examples/` - runnable examples: curl, a Python command line, a browser "put it on a shirt" button, Node

MIT license.
