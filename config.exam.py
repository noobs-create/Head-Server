# Head Server Configs
# A Config For Head Server

# Skins Server Configs
# Here You Can Config Skin Servers!
# Placeholders: {username}

# For Default... The Direct URL Are Supported
# But If You Want Mojang API Enter "mojang" As Default Setting
# Because For Mojang Players We Need To Request For UUID First
default = "mojang"

# mojang Also Work Inside Here Too
fallbacks = [
    "http://skinsystem.ely.by/skins/{username}.png",
    "https://auth.tlauncher.org/skin/fileservice/skins/skin_{username}.png"
]

# Skin Mode
# How Skin Will Reply To Client
# Options (Don't Care About Cases)
# head: Return Player Face
# head-1-8: Return 1.8 Style Of Player Face (No Layer 2)
# head-br: Return Bedrock Style Head (Minecraft Bedrock Marketplace Are Crazy That Player Head Model Can Be Changed)
# head-3d: Return Player 3D Head (Like Skull In Minecraft That Turn Right)
# head-3d-l: Like head-3d But The Resault Turn Left
skin_mode = "HEAD-1-8"

# Recommend To Enable This Because Some Service Have Redirect
follow_redirects = True

# We Saperate Bedrock Skin Service Because Bedrock API Are Threat Differently
# If You Enable This We Will Auto-Add Bedrock API (By Geyser) Into The Fallback List
# Usually After default
enable_bedrock_skin = True

# Some Skin API Might Need User Agent... This Is Default One
user_agent = "PrayoadMii Head Server"

# Where WebServer Will Bind On?
host = "0.0.0.0"
port = 7500