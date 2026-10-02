# merch1211

A print-on-demand API client with **no account and no key**. Send a picture; get back the link where your user sees it on a shirt, hoodie, cap, tumbler or tote and buys it. [1211](https://1211holding.com) prints each order one at a time, ships it free to US addresses, takes the payment and handles sales tax and support.

Works in the browser and in Node 18+. No dependencies.

```
npm install merch1211
```

```js
import { createDesign, upload, makeLink } from "merch1211";

// A picture that is already online: one call.
const d = await createDesign({ item: "hoodie", imageUrl: "https://example.com/art.png",
                               color: "Black", front: "center", size: "L", ref: "your-app" });
window.open(d.url);      // the page where your user sees it, picks sizes and pays

// A file the user picked in <input type="file" id="pic">:
const up = await upload(document.getElementById("pic").files[0]);
const d2 = await createDesign({ item: "tee", uploadId: up.upload });

// No request at all: a link that opens with the picture already on the item.
makeLink({ item: "tee", imageUrl: "https://example.com/art.png", color: "Black" });
```

- `front: "center"` prints big and centered (shirts and hoodies); the default is a small left-chest print.
- `side: "back"` or `"both"` for back prints. `size: "L"` preselects a size on the page.
- Errors throw `Merch1211Error` with `.problems`: each has a `code`, what it `says`, and the `fix`.

Docs: https://1211holding.com/developers · OpenAPI: https://1211holding.com/openapi.json · MIT license.
