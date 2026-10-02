#!/bin/sh
# Put a picture on a black hoodie, big and centered, and print the link where it can be bought.
# usage: sh curl.sh https://example.com/your-image.png
IMG="${1:-https://example.com/your-image.png}"
curl -s https://1211holding.com/v1/designs \
  -H 'Content-Type: application/json' \
  -d "{\"item\": \"hoodie\", \"color\": \"Black\", \"front\": {\"art\": {\"url\": \"$IMG\"}, \"placement\": \"center\"}, \"size\": \"L\", \"ref\": \"example-curl\"}"
echo
# A file on disk instead: upload it first, then use {"art": {"upload": "<id>"}}
#   curl -s -F art_file=@drawing.png https://1211holding.com/v1/art
