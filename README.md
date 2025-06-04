# Simple Discord Bot Assistant written in python for server: Devtherapy
summarize long conversations, articles, links or any overwhelming information by leveraging Discord Bot along with Gemini 
![summirize](https://media.discordapp.net/attachments/1379631159905878016/1379640884223803602/link_scraper.gif?ex=6840fa33&is=683fa8b3&hm=df889bd81089a3668224144cab2395ae54899370e1eddda0ec835d86c2704765&=&width=1097&height=721)
![summirize](https://media.discordapp.net/attachments/1379631159905878016/1379641336629821451/conversation.gif?ex=6840fa9f&is=683fa91f&hm=77edb6fb984d45232da23251583666048c581c630b30b22ea0795485ad915138&=&width=1082&height=848)

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
![summirize](https://cdn.discordapp.com/attachments/1379631159905878016/1379631443445157898/get_bot_token.gif?ex=6840f168&is=683f9fe8&hm=e52c13df201b028aefa2fdcc170c4c63c8df3f8f8c6fd189cba8447d0db5ffff&)
3. Rename ```devtherapy.examlpe.env``` to ```.env```
4. Fill out remaining credentials in ```.env``` (change already filed in credintials to desired discord GUILD_ID and USER_ID)
3. run project (installation and running is the same command when using uv)
```bash
uv run main.py
```



