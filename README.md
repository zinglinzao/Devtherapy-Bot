# Simple Discord Bot Assistant written in python for server: Devtherapy
summarize long conversations, articles, links or any overwhelming information by leveraging Discord Bot along with Gemini 
![link scraper](https://media.discordapp.net/attachments/1379631159905878016/1379640884223803602/link_scraper.gif?ex=6840fa33&is=683fa8b3&hm=df889bd81089a3668224144cab2395ae54899370e1eddda0ec835d86c2704765&=&width=1097&height=721)
![summarize command](https://media.discordapp.net/attachments/1379631159905878016/1379772388501225604/random_convo.gif?ex=684174ac&is=6840232c&hm=f5f2a50517a0f4a4d719df971d5c5b082501053be9f6d414500574f9e81c41f4&=&width=766&height=549)

## Installation
1. Install [python 3.12](https://www.python.org/downloads/) (version mostly doesn't matter)
2. Install [uv ](https://docs.astral.sh/uv/getting-started/installation/) (alternative to pip but you can still use requirements.txt)
- Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.7.10/install.ps1 | iex"
```
3. Visit: [google ai studio](https://aistudio.google.com/app/apikey) to create gimini api key
4. Visit: [discord dev portal](https://discord.com/developers/applications) and create bot to get it's token (enable privileged intents or bot will fail to initialize)
![create token](https://cdn.discordapp.com/attachments/1379631159905878016/1379631443445157898/get_bot_token.gif?ex=6840f168&is=683f9fe8&hm=e52c13df201b028aefa2fdcc170c4c63c8df3f8f8c6fd189cba8447d0db5ffff&)
5. Invite bot to your server (just paste the link in discord channel or browser)
![invite bot](https://media.discordapp.net/attachments/1379631159905878016/1379775992624709664/create_invite_link.gif?ex=68417807&is=68402687&hm=7695c1a7672472b3b791fb217ad57ad2e8520fa97146bf3243d34a188248b612&=)
6. Rename ```devtherapy.example.env``` to ```.env```
7. Optional: fill out remaining credentials in ```.env``` (change already filled in credintials to desired discord GUILD_ID and USER_ID)
- enable dev mode
![copy guild](https://support.discord.com/hc/article_attachments/22015896495255)
- copy guild(server) and user ids (by right-clicking on icons -> copy ID)
![copy id](https://support.discord.com/hc/article_attachments/30911629534871)
8. run project (installation and running is the same command when using uv)
```bash
uv run main.py
```



