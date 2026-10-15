# Discord Ticket Bot 🎟️

A fully functional Discord Bot written in Python (`discord.py`) for ticket management, specifically designed for servers such as RedM / Roleplay.

## 🚀 What does this code do?

1. **Ticket Panel System (`!setup_ticket`):**
   * Generates a sleek embed message featuring a header image, description, and an interactive button (`📩 Ticket`).

2. **Category Select Menu (Dropdown Menu):**
   * When a user clicks the button, a dropdown menu appears allowing them to select from 6 categories:
     * 🤠 **RP Issue** (Roleplay-related problems)
     * 🛜 **Connection Issue** (Connection problems to the RedM server)
     * ⚙️ **Support Issue** (General support topics)
     * ❓ **Question** (General inquiries)
     * 💸 **Donation support** (Donation assistance)
     * 💥 **Bug report** (Server bug reports)

3. **Automatic Channel Creation:**
   * Creates a private text channel within the designated Discord category, granting view/send permissions **only** to the ticket creator and the Staff team.

4. **Duplicate Ticket Prevention:**
   * Prevents users from opening multiple active ticket channels at the same time.

5. **Secure Ticket Closing:**
   * Every created ticket contains a close button (`🔒 Close Ticket`) that **can only be executed by Administrators or users with the designated Staff Role**.

## 🛠️ Setup & Installation Guide for Discord

### Step 1: Create the Bot on the Discord Developer Portal

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on **New Application** and give it a name (e.g., *Eclipse Ticket Bot*).
3. Select the **Bot** tab from the left side menu and click **Add Bot**.
4. Under the Username section, locate **Token** and click **Reset Token** (or Copy). Keep this safe — it is your `TOKEN`.
5. On the same page, scroll down to **Privileged Gateway Intents** and enable all three:
   * ✅ **Presence Intent**
   * ✅ **Server Members Intent**
   * ✅ **Message Content Intent**

### Step 2: Invite the Bot to Your Server

1. Go to **OAuth2** -> **URL Generator**.
2. Under **Scopes**, select:
   * `bot`
   * `applications.commands`
3. Under **Bot Permissions**, select:
   * `Administrator` (or explicitly: *Manage Channels, Read Messages/View Channels, Send Messages, Manage Messages*).
4. Copy the Generated URL at the bottom, open it in your browser, and authorize the bot for your Discord server.

### Step 3: Configure the Code (`bot.py`)

Open `bot.py` and update the variables at the top of the file with your own IDs and token:

* `TOKEN`: Paste your bot token from the Developer Portal.
* `STAFF_ROLE_ID`: The ID of the Staff role on your server (allowed to view and close tickets).
* Category IDs (`RP_CATEGORY_ID`, `CONNECTION_CATEGORY_ID`, etc.): The Discord category IDs where each respective ticket channel should be generated.

*(💡 **Tip to find IDs in Discord:** Enable Developer Mode in Discord Settings under Settings -> Advanced -> Developer Mode, then right-click any role or category and select "Copy ID").*

### Step 4: Running the Bot

1. Ensure you have Python and `discord.py` installed:
   ```bash
   pip install discord.py
   ```

2. Run your bot script:
   ```bash
   python bot.py
   ```

3. Head to your Discord server and type the following command in your designated support channel:
   ```text
   !setup_ticket
   ```
   *(Requires Administrator permissions).* The ticket panel embed will be sent immediately!
