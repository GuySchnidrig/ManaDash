"""
Build-time Scryfall metadata cache for ManaDash.

Replaces the per-card, per-render `/cards/named?fuzzy=` calls with a single
cached pass over the *unique* cards in `drafted_decks`:

  * uses `/cards/collection` (POST, 75 identifiers per request) instead of one
    GET per card -- ~800 unique cards becomes ~11 requests, not 800
  * writes `data/card_metadata.csv`, and only fetches names missing from it, so
    re-runs after a new draft cost one or two requests
  * image URLs point at `cards.scryfall.io` (their CDN, fine to hotlink);
    `--download-images` mirrors them locally instead

Usage:
    python -m src.backend.card_images              # refresh metadata cache
    python -m src.backend.card_images --download-images
    python -m src.backend.card_images --force      # ignore cache, refetch all
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import pandas as pd
import requests

# Works whether invoked as `python -m src.backend.card_images` (repo root on
# sys.path) or `python src/backend/card_images.py` (this dir on sys.path).
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from src.backend.backend_functions import DATA_DIR, get_data, initialize_data
except ModuleNotFoundError:
    sys.path.insert(0, _HERE)
    from backend_functions import DATA_DIR, get_data, initialize_data

ROOT_DIR = os.path.dirname(DATA_DIR)

COLLECTION_URL = "https://api.scryfall.com/cards/collection"
CACHE_PATH = os.path.join(DATA_DIR, "card_metadata.csv")
IMAGE_DIR = os.path.join(ROOT_DIR, "images", "cards")

# Scryfall's collection endpoint caps at 75 identifiers per request.
BATCH_SIZE = 75

# Scryfall asks for 50-100ms between requests and a descriptive User-Agent.
REQUEST_DELAY = 0.1
HEADERS = {
    "User-Agent": "ManaDash/1.0 (vintage cube draft analytics)",
    "Accept": "application/json",
}

COLUMNS = [
    "scryfall_id", "card_name", "cmc", "type_line",
    "is_creature", "is_land", "image_url", "image_url_small", "local_path",
]


def _face_images(card: dict) -> dict:
    """Front-face image URIs, handling transform/modal cards."""
    if "image_uris" in card:
        return card["image_uris"]
    faces = card.get("card_faces") or []
    if faces and "image_uris" in faces[0]:
        return faces[0]["image_uris"]
    return {}


def _extract(card: dict) -> dict:
    faces = card.get("card_faces") or []
    type_line = card.get("type_line") or (faces[0].get("type_line", "") if faces else "")
    images = _face_images(card)
    return {
        "scryfall_id": card.get("id", ""),
        "card_name": card.get("name", ""),
        "cmc": card.get("cmc", 0.0),
        "type_line": type_line,
        "is_creature": "creature" in type_line.lower(),
        "is_land": "land" in type_line.lower(),
        "image_url": images.get("normal", ""),
        "image_url_small": images.get("small", ""),
        "local_path": "",
    }


def _deck_identifiers() -> pd.DataFrame:
    """Unique (scryfall_id, card_name) pairs actually used in drafted decks."""
    decks = get_data("drafted_decks")
    if decks.empty:
        raise RuntimeError("drafted_decks is empty -- did initialize_data() run?")

    id_col = "scryfallId" if "scryfallId" in decks.columns else None
    name_col = "card_name" if "card_name" in decks.columns else "cardName"

    cols = [c for c in [id_col, name_col] if c]
    out = decks[cols].dropna(subset=[name_col]).drop_duplicates()
    out = out.rename(columns={id_col: "scryfall_id", name_col: "card_name"})
    if "scryfall_id" not in out.columns:
        out["scryfall_id"] = ""
    return out.reset_index(drop=True)


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def fetch_metadata(force: bool = False) -> pd.DataFrame:
    """Fetch metadata for every unique drafted card, reusing the cache."""
    wanted = _deck_identifiers()

    cached = pd.DataFrame(columns=COLUMNS)
    if os.path.exists(CACHE_PATH) and not force:
        cached = pd.read_csv(CACHE_PATH)
        for col in COLUMNS:
            if col not in cached.columns:
                cached[col] = ""

    known = set(cached["card_name"].astype(str))
    missing = wanted[~wanted["card_name"].astype(str).isin(known)]

    if missing.empty:
        print(f"Cache is current: {len(cached)} cards, nothing to fetch.")
        return cached

    print(f"Fetching {len(missing)} new cards in "
          f"{-(-len(missing) // BATCH_SIZE)} request(s)...")

    records, not_found = [], []
    rows = missing.to_dict("records")

    for batch in _chunks(rows, BATCH_SIZE):
        identifiers = [
            {"id": r["scryfall_id"]} if str(r.get("scryfall_id", "")).strip()
            else {"name": r["card_name"]}
            for r in batch
        ]
        response = requests.post(
            COLLECTION_URL,
            json={"identifiers": identifiers},
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()

        records.extend(_extract(c) for c in payload.get("data", []))
        not_found.extend(payload.get("not_found", []))
        time.sleep(REQUEST_DELAY)

    if not_found:
        print(f"WARNING: {len(not_found)} identifier(s) not found on Scryfall:")
        for item in not_found[:10]:
            print(f"  {item}")

    fresh = pd.DataFrame(records, columns=COLUMNS)
    combined = pd.concat([cached, fresh], ignore_index=True)
    combined = combined.drop_duplicates(subset="card_name", keep="last")
    combined = combined.sort_values("card_name").reset_index(drop=True)

    combined.to_csv(CACHE_PATH, index=False)
    print(f"Wrote {len(combined)} cards to {CACHE_PATH}")
    return combined


def download_images(meta: pd.DataFrame, size: str = "normal") -> pd.DataFrame:
    """Mirror card images into images/cards/ and record site-relative paths."""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    url_col = "image_url" if size == "normal" else "image_url_small"

    downloaded = skipped = failed = 0

    for idx, row in meta.iterrows():
        url = str(row.get(url_col, "") or "")
        if not url:
            continue

        filename = f"{row['scryfall_id'] or row['card_name']}.jpg"
        filename = filename.replace("/", "_").replace(" ", "_")
        target = os.path.join(IMAGE_DIR, filename)
        # Site-relative so it resolves the same locally and on GitHub Pages.
        meta.at[idx, "local_path"] = f"images/cards/{filename}"

        if os.path.exists(target):
            skipped += 1
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            with open(target, "wb") as handle:
                handle.write(response.content)
            downloaded += 1
            time.sleep(REQUEST_DELAY)
        except requests.RequestException as exc:
            print(f"  failed: {row['card_name']}: {exc}")
            meta.at[idx, "local_path"] = ""
            failed += 1

    meta.to_csv(CACHE_PATH, index=False)
    print(f"Images -> {IMAGE_DIR}: {downloaded} new, {skipped} cached, {failed} failed")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-images", action="store_true",
                        help="mirror images locally instead of hotlinking the CDN")
    parser.add_argument("--force", action="store_true",
                        help="ignore the cache and refetch every card")
    parser.add_argument("--size", default="normal", choices=["normal", "small"],
                        help="image size to download (default: normal)")
    args = parser.parse_args()

    initialize_data()
    meta = fetch_metadata(force=args.force)

    if args.download_images:
        download_images(meta, size=args.size)


if __name__ == "__main__":
    main()