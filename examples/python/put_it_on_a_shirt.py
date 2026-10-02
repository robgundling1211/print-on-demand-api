"""Put a picture on a shirt from the command line and print the link where it can be bought.

    pip install merch1211
    python put_it_on_a_shirt.py drawing.png --item hoodie --color Black --front center --size L
    python put_it_on_a_shirt.py https://example.com/art.png --item tee
"""
import argparse

import merch1211


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("picture", help="a file path or a public image link")
    ap.add_argument("--item", default="tee", help="tee, hoodie, crewneck, tee-classic, polo, quarter-zip, cap, trucker, tumbler, tote")
    ap.add_argument("--color")
    ap.add_argument("--side", default="front", choices=["front", "back", "both"])
    ap.add_argument("--front", choices=["chest", "center"], help="center = big and centered (shirts and hoodies)")
    ap.add_argument("--size", help="a size to start with on the page, such as L")
    ap.add_argument("--ref", default="example-cli", help="your app's name")
    a = ap.parse_args()

    if a.picture.startswith(("http://", "https://")):
        src = {"image_url": a.picture}
    else:
        src = {"upload_id": merch1211.upload(a.picture)["upload"]}
    try:
        d = merch1211.create_design(a.item, color=a.color, side=a.side, front=a.front, size=a.size, ref=a.ref, **src)
    except merch1211.Merch1211Error as e:
        for p in e.problems:
            print("%s: %s %s" % (p["code"], p["says"], p["fix"]))
        raise SystemExit(1)
    for p in d["problems"]:
        print("note:", p["says"])
    for side, s in d["sides"].items():
        print("%s: %s" % (side, s["says"]))
    print("$%s, free US shipping" % d["price"]["usd"])
    print(d["url"])


if __name__ == "__main__":
    main()
