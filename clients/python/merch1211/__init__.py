"""merch1211 - put a picture on a shirt, hoodie, cap, tumbler or tote and get the link where the person buys it.

No account and no key. 1211 prints each order one at a time, ships it free to US addresses, takes the payment and
handles sales tax and support; your user pays on 1211's page.

    import merch1211
    d = merch1211.create_design("hoodie", image_url="https://example.com/art.png", color="Black", front="center", size="L")
    print(d["url"])      # send your user here: they see it on the hoodie, pick sizes and pay

API reference: https://1211holding.com/developers  ·  OpenAPI: https://1211holding.com/openapi.json
No dependencies: the standard library only.
"""
import json
import mimetypes
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid

__version__ = "0.1.0"
__all__ = ["catalog", "upload", "create_design", "get_design", "make_link", "Merch1211Error", "BASE"]

BASE = "https://1211holding.com"
_UA = "merch1211-python/" + __version__


class Merch1211Error(Exception):
    """The API could not do it. ``problems`` is its list of {code, where, says, fix}; ``status`` the HTTP status."""

    def __init__(self, status, problems):
        self.status = status
        self.problems = list(problems or [])
        text = "; ".join(p.get("says", "") + (" " + p["fix"] if p.get("fix") else "") for p in self.problems)
        super().__init__(text or "HTTP %s" % status)


def _call(method, path, body=None, headers=None, base=BASE, timeout=60):
    h = {"User-Agent": _UA, "Accept": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(base.rstrip("/") + path, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            problems = json.loads(e.read().decode("utf-8")).get("problems")
        except Exception:
            problems = None
        raise Merch1211Error(e.code, problems) from None


def catalog(base=BASE):
    """Every item with its colours, sizes, print sizes, the pixels a picture needs, and prices (US shipping included)."""
    return _call("GET", "/v1/catalog", base=base)


def upload(file, base=BASE):
    """Upload a picture: a path or a binary file object. PNG, JPG, WEBP, GIF, HEIC or PDF.

    Returns {"upload": id, "w", "h", "says", "preview", ...}; use the id as ``upload_id`` in create_design()."""
    if hasattr(file, "read"):
        data, name = file.read(), os.path.basename(getattr(file, "name", "picture.png") or "picture.png")
    else:
        with open(file, "rb") as fh:
            data, name = fh.read(), os.path.basename(str(file))
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    head = ('--%s\r\nContent-Disposition: form-data; name="art_file"; filename="%s"\r\nContent-Type: %s\r\n\r\n'
            % (boundary, name.replace('"', ""), ctype)).encode("utf-8")
    body = head + data + ("\r\n--%s--\r\n" % boundary).encode("utf-8")
    return _call("POST", "/v1/art", body, {"Content-Type": "multipart/form-data; boundary=" + boundary}, base=base)


def create_design(item, image_url=None, upload_id=None, color=None, side="front", front=None, size=None,
                  back_image_url=None, back_upload_id=None, title=None, ref=None, base=BASE):
    """Put a picture on an item and get the design back, including ``url`` - the page where the person buys it.

    item:  "tee", "hoodie", "crewneck", "tee-classic", "polo", "quarter-zip", "cap", "trucker", "tumbler", "tote"
           (see catalog()).
    side:  "front", "back" or "both" (both uses the same picture unless a back picture is given).
    front: "chest" (small, on the left chest, the default) or "center" (big and centered; shirts and hoodies).
    size:  a size to start with on the page, such as "L" or "2XL"; the person can change it.
    ref:   your app's name, so 1211 can see who sends people.

    The design also carries ``mockup`` (pictures of the result), ``sides`` (how big each side prints), ``price``
    and ``problems`` (things that did not go as asked but did not stop the design). Raises Merch1211Error when
    nothing could be made."""
    def art(url, up):
        return {"upload": up} if up else ({"url": url} if url else None)

    a, b = art(image_url, upload_id), art(back_image_url, back_upload_id)
    if a is None and b is None:
        raise ValueError("give image_url or upload_id")
    spec = {"item": item}
    if color:
        spec["color"] = color
    if side in ("front", "both") and a is not None:
        spec["front"] = {"art": a}
        if front:
            spec["front"]["placement"] = front
    if side in ("back", "both") and (b or a) is not None:
        spec["back"] = {"art": b or a}
    for k, v in (("size", size), ("title", title), ("ref", ref)):
        if v:
            spec[k] = v
    return _call("POST", "/v1/designs", json.dumps(spec).encode("utf-8"), {"Content-Type": "application/json"}, base=base)


def get_design(design_id, base=BASE):
    """The same object create_design() returned, read again by its id."""
    return _call("GET", "/v1/designs/" + urllib.parse.quote(str(design_id), safe=""), base=base)


def make_link(item, image_url=None, color=None, side=None, front=None, size=None, title=None, ref=None, base=BASE):
    """No request at all: a link that opens 1211's page with the picture already on the item.

    Nothing is created until the person presses Continue. Leave image_url out and the page asks them to upload."""
    q = {"item": item}
    for k, v in (("color", color), ("art", image_url), ("side", side), ("front", front), ("size", size),
                 ("title", title), ("ref", ref)):
        if v:
            q[k] = v
    return base.rstrip("/") + "/make?" + urllib.parse.urlencode(q, safe=":/")
