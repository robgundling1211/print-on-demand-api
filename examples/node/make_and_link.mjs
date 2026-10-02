// npm install merch1211 && node make_and_link.mjs https://example.com/art.png
import { createDesign, makeLink, Merch1211Error } from "merch1211";

const imageUrl = process.argv[2];
if (!imageUrl) {
  console.error("usage: node make_and_link.mjs <public image link>");
  process.exit(1);
}

// 1. No request: a link that opens with the picture on a black hoodie.
console.log("link:", makeLink({ item: "hoodie", imageUrl, color: "Black", front: "center" }));

// 2. One request: a saved design with its price, print size and a picture of the result.
try {
  const d = await createDesign({ item: "hoodie", imageUrl, color: "Black", front: "center", size: "L", ref: "example-node" });
  for (const p of d.problems) console.log("note:", p.says);
  console.log(d.sides.front.says);
  console.log(`$${d.price.usd}, free US shipping:`, d.url);
} catch (e) {
  if (e instanceof Merch1211Error) for (const p of e.problems) console.error(p.code, p.says, p.fix);
  else throw e;
}
