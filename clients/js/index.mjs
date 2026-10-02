// merch1211 - put a picture on a shirt, hoodie, cap, tumbler or tote and get the link where the person buys it.
// No account and no key. 1211 prints each order, ships it free to US addresses, takes the payment and handles
// sales tax and support. Works in browsers and in Node 18+ (it only uses fetch and FormData).
// API reference: https://1211holding.com/developers  ·  OpenAPI: https://1211holding.com/openapi.json

export const BASE = "https://1211holding.com";

export class Merch1211Error extends Error {
  constructor(status, problems) {
    const list = Array.isArray(problems) ? problems : [];
    super(list.map((p) => (p.says || "") + (p.fix ? " " + p.fix : "")).join("; ") || `HTTP ${status}`);
    this.name = "Merch1211Error";
    this.status = status;
    this.problems = list;
  }
}

async function call(path, init = {}, base = BASE) {
  const res = await fetch(base.replace(/\/$/, "") + path, {
    ...init,
    headers: { Accept: "application/json", ...(init.headers || {}) },
  });
  let body = null;
  try { body = await res.json(); } catch (e) { /* not JSON */ }
  if (!res.ok) throw new Merch1211Error(res.status, body && body.problems);
  return body;
}

/** Every item with its colours, sizes, print sizes, the pixels a picture needs, and prices (US shipping included). */
export function catalog({ base } = {}) {
  return call("/v1/catalog", {}, base);
}

/** Upload a picture (a File from <input type="file">, or any Blob). Resolves to { upload, w, h, says, ... }. */
export function upload(file, { base } = {}) {
  const fd = new FormData();
  fd.append("art_file", file, file && file.name ? file.name : "picture.png");
  return call("/v1/art", { method: "POST", body: fd }, base);
}

/**
 * Put a picture on an item and get the design back, including `url` - the page where the person buys it.
 * side: "front" | "back" | "both";  front: "chest" (small, left chest, default) | "center" (big, centered; shirts, hoodies);
 * size: a size to start with on the page ("L", "2XL"...);  ref: your app's name.
 */
export function createDesign({ item, imageUrl, uploadId, color, side = "front", front, size,
                               backImageUrl, backUploadId, title, ref, base } = {}) {
  const art = (url, up) => (up ? { upload: up } : url ? { url } : null);
  const a = art(imageUrl, uploadId);
  const b = art(backImageUrl, backUploadId);
  if (!a && !b) throw new Error("give imageUrl or uploadId");
  const spec = { item };
  if (color) spec.color = color;
  if ((side === "front" || side === "both") && a) {
    spec.front = { art: a };
    if (front) spec.front.placement = front;
  }
  if ((side === "back" || side === "both") && (b || a)) spec.back = { art: b || a };
  if (size) spec.size = size;
  if (title) spec.title = title;
  if (ref) spec.ref = ref;
  return call("/v1/designs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(spec),
  }, base);
}

/** The same object createDesign() returned, read again by its id. */
export function getDesign(id, { base } = {}) {
  return call("/v1/designs/" + encodeURIComponent(id), {}, base);
}

/** No request at all: a link that opens 1211's page with the picture already on the item. */
export function makeLink({ item, imageUrl, color, side, front, size, title, ref, base = BASE } = {}) {
  const q = new URLSearchParams({ item });
  for (const [k, v] of [["color", color], ["art", imageUrl], ["side", side], ["front", front],
                        ["size", size], ["title", title], ["ref", ref]]) {
    if (v) q.set(k, v);
  }
  return `${base.replace(/\/$/, "")}/make?${q}`;
}
