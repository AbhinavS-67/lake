# A Little Lake, Just for You

A small interactive world for someone you like: a map of four lakes with ducks,
lily pads, fireflies, a moon with a letter, a boat of photos, a meadow where she
picks flowers into a bouquet, and a locked chest that opens once she has
explored everywhere.

## Make it yours (10 minutes)

1. Open `app.py` and edit the block marked **EDIT THIS PART**.
   - Rewrite every message so it sounds like you. Add real inside jokes and nicknames.
   - Rewrite the **letter** (the moon). This matters most.
   - Fill in `signature`.
2. Put photos in the `photos/` folder, then list the file names in `memories`
   (for example `"photo": "beach.jpg"`). They are resized automatically.
3. Optional: set `PASSCODE` so she has to type a secret word first.
4. Optional: set `REPLY_WHATSAPP` (digits with country code) so the message in the
   bottle can open a chat with you. Leave it empty and the bottle just copies her note.

## Run it on your computer

    pip install -r requirements.txt
    streamlit run app.py

## Put it online (free, Streamlit Community Cloud)

1. Create a GitHub repository and upload these files (`app.py`, `lake.html`,
   `requirements.txt`, the `photos/` folder).
   **Make the repository private.** Your messages and photos are stored in it, and
   a public repo can be read by anyone. Streamlit Community Cloud can deploy private repos.
2. Go to share.streamlit.io, sign in with GitHub, click **Create app**, choose the repo,
   set the main file to `app.py`, and deploy.
3. Send her the link. You can pick a friendlier address under **Advanced settings**.

Notes
- The passcode is a soft gate only. Anyone with repo access can read the messages.
- It is best on a laptop or a phone held sideways.
- Her progress (opened pads, picked flowers) is saved in her own browser.
- Sound starts after her first tap. There is a mute button top right.
