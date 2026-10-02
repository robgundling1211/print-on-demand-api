# merch1211

A print-on-demand API client with **no account and no key**. Send a picture; get back the link where your user sees it on a shirt, hoodie, cap, tumbler or tote and buys it. [1211](https://1211holding.com) prints each order one at a time, ships it free to US addresses, takes the payment and handles sales tax and support.

```
pip install merch1211
```

```python
import merch1211

# A picture that is already online: one call.
d = merch1211.create_design("hoodie", image_url="https://example.com/art.png", color="Black",
                            front="center", size="L", ref="your-app")
print(d["url"])            # send your user here: they see it on the hoodie, pick sizes and pay
print(d["price"]["usd"])   # what one costs, US shipping included

# A file on disk: upload it, then use its id.
up = merch1211.upload("drawing.png")
d = merch1211.create_design("tee", upload_id=up["upload"])

# No request at all: a link that opens with the picture already on the item.
print(merch1211.make_link("tee", image_url="https://example.com/art.png", color="Black"))
```

- `front="center"` prints big and centered (shirts and hoodies); the default is a small left-chest print.
- `side="back"` or `side="both"` for back prints. `size="L"` preselects a size on the page.
- Errors raise `merch1211.Merch1211Error` with `.problems`: each has a `code`, what it `says`, and the `fix`.
- No dependencies: the standard library only.

Docs: https://1211holding.com/developers · OpenAPI: https://1211holding.com/openapi.json · MIT license.
