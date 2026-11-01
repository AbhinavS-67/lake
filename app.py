"""A little lake, just for her.  Run with:  streamlit run app.py

Everything personal lives in the CONFIG block below. Edit the words, add your
photos to the photos/ folder, and you're done. lake.html draws the world.
"""
import base64
import io
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent

st.set_page_config(page_title="A Little Lake", page_icon="🦆", layout="wide",
                   initial_sidebar_state="collapsed")

# =============================== EDIT THIS PART ===============================

# Optional secret word she has to type before the lake opens. Leave "" for none.
PASSCODE = ""
GATE_HINT = "Type our secret word to come in."

# Optional: lets her write back through the message-in-a-bottle.
# Put your WhatsApp number with country code, digits only (e.g. "919876543210").
# Leave "" and the bottle will simply copy her note so she can paste it to you.
REPLY_WHATSAPP = "916207993987"

CONFIG = {
    "mapTitle": "A Little Lake, Just for You",
    "introKicker": "made with care, for one person",
    "introTitle": "A little place, just for you.",
    "introText": "I wanted to make you something special. Somewhere you could escape to "
                 "whenever you felt like it. So I made a little lake.",
    "enterText": "Enter the little world ♡",

    # Rename the four lakes if you like.
    "lakes": {
        "lily":     {"name": "Lily Pond",       "sub": "where the ducks live"},
        "memory":   {"name": "Memory Cove",     "sub": "a boat full of moments"},
        "blossom":  {"name": "Blossom Meadow",  "sub": "pick a few flowers"},
        "firefly":  {"name": "Firefly Lake",    "sub": "best after dark"},
    },

    "messages": {
        # 7 messages, one per lily pad.
        "lily": [
            "I love how your face lights up when you're excited.",
            "Your smile is genuinely one of my favourite things.",
            "I love listening to you talk about the things you enjoy.",
            "You make ordinary days feel special.",
            "I hope you know how much you matter.",
            "You're easy to talk to, and I never want to run out of things to say.",
            "Somewhere out there a duck thinks you're wonderful. So do I.",
        ],
        # Caught fireflies show these in random order.
        "fireflies": [
            "If I could choose someone to spend an ordinary Tuesday with, I'd choose you.",
            "You are my favourite notification.",
            "I wish I could bottle up the happiness you give me.",
            "Just a reminder that somebody is thinking about you right now.",
            "You have a way of making a room feel softer.",
            "I'm really glad our paths crossed.",
            "Your laugh is the kind of sound I'd play on repeat.",
            "I hope tonight is kind to you.",
            "You caught me thinking about you. Oh wait, you just did.",
            "You deserve all the gentle things.",
        ],
        # Shown after she skips a pebble onto any lake.
        "pebbles": [
            "I wish I could give you a hug right now.",
            "Here's a reminder to drink some water!",
            "I hope something makes you smile today.",
            "If I were there, I'd probably be annoying you right now.",
            "Sending you the biggest virtual hug.",
            "Make a wish. I won't peek.",
            "You're doing better than you think.",
        ],
        # Floating lotus lanterns in Memory Cove (use 4+; the first two she reads count).
        "floats": [
            "One of those moments I wish I could experience all over again.",
            "This is the one I replay in my head when I need a smile.",
            "Some days just stay with you. This was one of them.",
            "Inside joke goes here. (Replace me with a real one!)",
        ],
        "ducks": [
            "Quack. (That means you're doing great.)",
            "This duck has been told to remind you to drink water.",
            "I asked the ducks to look after you. They take the job very seriously.",
            "The ducklings say hi. They are also very proud of you.",
            "Fun fact: ducks are happier when you're around. Not a real fact, but it should be.",
        ],
        "butterflies": [
            "Butterflies. Fitting, since I get them around you.",
            "This one flew a long way just to say you're lovely.",
            "Make a wish on the butterfly. It's very good at keeping secrets.",
        ],
        # One of these appears each time she picks a flower.
        "flowers": [
            "Good pick. You have excellent taste.",
            "That one reminded me of you.",
            "For your bouquet ♡",
            "Careful, you're collecting my favourites.",
            "Flowers always look better in your hands.",
        ],
        "frog": "Ribbit. The frog says you're somebody's favourite person.",
        "sun": "The sun is setting slowly here because I don't want this evening to end.",
        "sun2": "Even the sun came out to say hi to you.",
        "sun3": "Good morning, sunshine. (Yes, that was on purpose.)",
        "locked": "A chest sits on the island, but it's locked. Maybe each lake is holding a piece of the key.",
        "unlock": "Something just unlocked on the map. Go and look at the little island.",
    },

    # The letter that opens when she taps the moon in Firefly Lake. Rewrite it in
    # your own voice. This is the most important part of the whole page.
    "letterGreeting": "Hey you,",
    "letter": [
        "I know this is just a little website, but I wanted to make something that "
        "could remind you that even on the most ordinary days, there's someone who "
        "thinks the world of you.",
        "I'm not always great at saying things out loud, so I built this instead. "
        "Every lily pad, every firefly and every duck is a small thing I'd tell you "
        "if the words came out right.",
        "There's no pressure in any of it. I just want you to have a place that's "
        "calm, and a reminder that you make my days better.",
        "Thank you for being exactly who you are.",
    ],
    "signature": "Yours, (your name)",

    # Photos for the boat. Put images in the photos/ folder and list the file name.
    # Leave "photo" as "" to show a placeholder until you've added one.
    "memories": [
        {"photo": "us.jpeg", "caption": "One of those moments I wish I could experience all over again.", "date": "."},
        {"photo": "WhatsApp Image 2026-11-01 at 22.37.08.jpeg", "caption": "You, being completely you.", "date": "."},
        {"photo": "WhatsApp Image 2026-11-01 at 22.37.07 (2).jpeg", "caption": "pretty you", "date": "."},
        {"photo": "WhatsApp Image 2026-11-01 at 22.37.07.jpeg", "caption": "pretty woman again", "date": "."},
    ],

    "bottle": {
        "text": "There's a note in this bottle for you. If you feel like writing back, I'd love to read it.",
        "placeholder": "Write whatever you like...",
    },
    "bouquetNote": "These are for you. Every single one.",

    "finalTitle": "The final surprise",
    "finalMessage": "Out of all the beautiful places in the world, I think my favourite "
                    "will always be wherever you're smiling.",
    "stayText": "Stay a little longer? ♡",
}

# ============================== END OF EDIT ZONE ==============================


def embed_photo(name):
    """Turn a file in photos/ into a small data URL, or None if missing."""
    if not name:
        return None
    path = BASE / "photos" / name
    if not path.exists():
        return None
    try:
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im.thumbnail((900, 900))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82)
        data, mime = buf.getvalue(), "image/jpeg"
    except Exception:
        data = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(data).decode()


@st.cache_data(show_spinner=False)
def build_html(cfg_json: str, mtime: float) -> str:
    html = (BASE / "lake.html").read_text(encoding="utf-8")
    return html.replace("__CONFIG__", cfg_json.replace("</", "<\\/"))


def make_config():
    cfg = json.loads(json.dumps(CONFIG))
    cfg["memories"] = [
        {"img": embed_photo(m.get("photo", "")), "caption": m["caption"], "date": m.get("date", "")}
        for m in CONFIG["memories"]
    ]
    digits = "".join(ch for ch in REPLY_WHATSAPP if ch.isdigit())
    cfg["replyUrl"] = f"https://wa.me/{digits}?text=" if digits else ""
    return cfg


st.markdown(
    """<style>
    #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {display:none !important}
    .stApp {background:#141a3d}
    .block-container {padding:0 !important; max-width:100% !important}
    iframe {border:0; display:block}
    </style>""",
    unsafe_allow_html=True,
)

if PASSCODE and not st.session_state.get("ok"):
    st.markdown("<div style='height:18vh'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown(f"<h3 style='color:#fff;text-align:center;font-weight:500'>{GATE_HINT}</h3>",
                    unsafe_allow_html=True)
        code = st.text_input("Secret word", type="password", label_visibility="collapsed")
        if code:
            if code.strip().lower() == PASSCODE.strip().lower():
                st.session_state["ok"] = True
                st.rerun()
            else:
                st.caption("Hmm, not quite. Try again.")
    st.stop()

cfg = make_config()
html = build_html(json.dumps(cfg), (BASE / "lake.html").stat().st_mtime)
components.html(html, height=740, scrolling=False)
