import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import asyncio

# ΡΥΘΜΙΣΕΙΣ (Συμπλήρωσε τα δικά σου ID για κάθε κατηγορία) 
TOKEN = "" # Το token του bot
STAFF_ROLE_ID =  # Το ID του Role των Staff που θα βλέπουν τα tickets

# --- ID ΚΑΤΗΓΟΡΙΩΝ ΓΙΑ ΚΑΘΕ ΤΥΠΟ TICKET ---
RP_CATEGORY_ID =        # Βάλε εδώ το ID για τα RP Issue
CONNECTION_CATEGORY_ID =  # Βάλε εδώ το ID για τα Connection Issue
SUPPORT_CATEGORY_ID =    # Βάλε εδώ το ID για τα Support Issue
QUESTION_CATEGORY_ID =  # Βάλε εδώ το ID για τα Question
DONATION_CATEGORY_ID =  # Βάλε εδώ το ID για τα Donation support
BUG_CATEGORY_ID =        # Βάλε εδώ το ID για τα Bug report

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# View για το Κλείσιμο του Ticket (Αυστηρός έλεγχος μόνο για Staff / Admin)
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.secondary, custom_id="close_ticket_btn", emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        staff_role = guild.get_role(STAFF_ROLE_ID)
        
        # Έλεγχος αν ο χρήστης είναι Admin ή έχει τον Staff ρόλο
        is_admin = interaction.user.guild_permissions.administrator
        is_staff = staff_role and staff_role in interaction.user.roles

        # Αν ΔΕΝ είναι ούτε Admin ούτε Staff, απορρίπτεται η ενέργεια
        if not (is_admin or is_staff):
            await interaction.response.send_message("❌ Μόνο η ομάδα Staff μπορεί να κλείσει αυτό το ticket.", ephemeral=True)
            return

        # Αν είναι Staff ή Admin, προχωράει κανονικά η διαδικασία διαγραφής
        await interaction.response.send_message("🔒 Το ticket κλείνει και το κανάλι θα διαγραφεί σε λίγα δευτερόλεπτα...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

# Dropdown Menu με τις Επιλογές 
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="RP Issue", description="Πρόβλημα που σχετίζεται με το Roleplay", emoji="🤠"),
            discord.SelectOption(label="Connection Issue", description="Πρόβλημα σύνδεσης στον RedM server", emoji="🛜"),
            discord.SelectOption(label="Support Issue", description="Γενικό θέμα υποστήριξης", emoji="⚙️"),
            discord.SelectOption(label="Question", description="Έχεις κάποια απορία;", emoji="❓"),
            discord.SelectOption(label="Donation support", description="Θέλεις να κάνεις μια δωρεά;", emoji="💸"),
            discord.SelectOption(label="Bug report", description="Αναφορά κάποιου bug του server", emoji="💥")
        ]
        super().__init__(placeholder="Επίλεξε την κατηγορία του ticket σου...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        # Έλεγχος αν ο χρήστης έχει ήδη ανοιχτό κανάλι ticket στον server
        # Ελέγχουμε αν υπάρχει κανάλι που το όνομα του περιέχει το όνομα του χρήστη
        existing_ticket = discord.utils.get(guild.text_channels, name=f"rp-ticket-{user.name}".lower()) or \
                          discord.utils.get(guild.text_channels, name=f"connection-issue-ticket-{user.name}".lower()) or \
                          discord.utils.get(guild.text_channels, name=f"support-ticket-{user.name}".lower()) or \
                          discord.utils.get(guild.text_channels, name=f"question-{user.name}".lower()) or \
                          discord.utils.get(guild.text_channels, name=f"donation-ticket-{user.name}".lower()) or \
                          discord.utils.get(guild.text_channels, name=f"bug-ticket-{user.name}".lower())

        if existing_ticket:
            await interaction.response.send_message(
                f"❌ Έχεις ήδη ανοιχτό ticket στο κανάλι {existing_ticket.mention}! Πρέπει να κλείσει από το Staff προτού ανοίξεις νέο.", 
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True) # Εμποδίζει το "Interaction Failed"
        
        selected_option = self.values[0]
        staff_role = guild.get_role(STAFF_ROLE_ID)

        # ΚΑΘΟΡΙΣΜΟΣ ΚΑΤΗΓΟΡΙΑΣ ΚΑΙ ΟΝΟΜΑΤΟΣ ΑΝΑΛΟΓΑ ΜΕ ΤΗΝ ΕΠΙΛΟΓΗ
        if selected_option == "RP Issue":
            category = guild.get_channel(RP_CATEGORY_ID)
            channel_name = f"rp-ticket-{user.name}".lower()
        elif selected_option == "Connection Issue":
            category = guild.get_channel(CONNECTION_CATEGORY_ID)
            channel_name = f"connection-issue-ticket-{user.name}".lower()
        elif selected_option == "Support Issue":
            category = guild.get_channel(SUPPORT_CATEGORY_ID)
            channel_name = f"support-ticket-{user.name}".lower()
        elif selected_option == "Question":
            category = guild.get_channel(QUESTION_CATEGORY_ID)
            channel_name = f"question-{user.name}".lower()
        elif selected_option == "Donation support":
            category = guild.get_channel(DONATION_CATEGORY_ID)
            channel_name = f"donation-ticket-{user.name}".lower()
        elif selected_option == "Bug report":
            category = guild.get_channel(BUG_CATEGORY_ID)
            channel_name = f"bug-ticket-{user.name}".lower()
        else:
            category = guild.get_channel(RP_CATEGORY_ID)
            channel_name = f"ticket-{user.name}".lower()

        # Δικαιώματα πρόσβασης στο νέο κανάλι
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)

        # Δημιουργία του καναλιού ticket τη σωστή κατηγορία
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        # Προσαρμοσμένο κείμενο ανάλογα με την κατηγορία
        if selected_option == "Donation support":
            desc = f"Γεια σου {user.mention}!\n\n**Κατηγορία:** `💎 Donation support`\n\nΣε ευχαριστούμε πολύ για τη στήριξη στον server! Παρακαλώ γράψε εδώ τις λεπτομέρειες της δωρεάς σου και η αρμόδια διαχείριση θα σε εξυπηρετήσει άμεσα."
        else:
            desc = f"Γεια σου {user.mention}!\n\n**Κατηγορία:** `{selected_option}`\n\nΠαρακαλώ γράψε εδώ αναλυτικά την ερώτηση ή το πρόβλημα που αντιμετωπίζεις και ένα μέλος της ομάδας μας θα σου απαντήσει το συντομότερο δυνατό."

        # Μήνυμα μέσα στο νέο κανάλι του ticket μαζί με το κουμπί κλεισίματος
        embed_ticket = discord.Embed(
            title=f"Eclipse Roleplay - Support Ticket",
            description=desc,
            color=discord.Color.dark_red()
        )
        
        await ticket_channel.send(
            content=f"{user.mention} {staff_role.mention if staff_role else ''}", 
            embed=embed_ticket,
            view=CloseTicketView()
        )

        # Επιβεβαιωτικό μήνυμα στον χρήστη (ορατό μόνο σε αυτόν)
        await interaction.followup.send(
            content=f"✅ **Ticket successfully created!**\nΜπορείς να κάνεις την ερώτησή σου στο κανάλι: {ticket_channel.mention}",
            ephemeral=True
        )

class TicketSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# Κουμπί "Create Ticket" 
class InitialTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket", style=discord.ButtonStyle.danger, custom_id="open_ticket_btn", emoji="📩")
    async def ticket_button(self, interaction: discord.Interaction, button: Button):
        embed_options = discord.Embed(
            title="Eclipse Roleplay - Επιλογή Κατηγορίας",
            description="Παρακαλώ επίλεξε την κατηγορία που ταιριάζει στο αίτημά σου από το παρακάτω μενού:",
            color=discord.Color.dark_red()
        )
        await interaction.response.send_message(embed=embed_options, view=TicketSelectView(), ephemeral=True)

# Συμβάν όταν το Bot είναι Online
@bot.event
async def on_ready():
    print(f'✅ Έγινε σύνδεση ως {bot.user.name} (Eclipse Roleplay Bot)')
    bot.add_view(InitialTicketView())
    bot.add_view(CloseTicketView()) # Διατηρεί το κουμπί κλεισίματος ενεργό

# Εντολή για αποστολή του Embed Panel στο κανάλι 
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    await ctx.message.delete()
    
    embed = discord.Embed(
        title="📩 SUPPORT / TICKETS",
        description=(
            "Για οποιαδήποτε απορία, βοήθεια ή αίτημα, παρακαλούμε να ανοίγετε ένα ticket.\n\n"
            "• Μην κάνετε ping staff χωρίς λόγο\n"
            "• Μην γράφετε σε άλλα κανάλια για support\n"
            "• Όλα τα θέματα εξυπηρετούνται μόνο μέσω tickets\n\n"
            "📌 **Τι μπορείτε να κάνετε μέσω ticket:**\n"
            "• Ερωτήσεις για τον server\n"
            "• Αναφορές προβλημάτων\n"
            "• Aιτήματα ή βοήθεια\n"
            "• Oτιδήποτε χρειάζεται διαχείριση από staff\n"
            "• DONATIONS"
        ),
        color=discord.Color.dark_red()
    )
    embed.set_author(name="Eclipse Ticket System", icon_url="https://i.postimg.cc/YSdMpfJm/ecplipse.png")
    # Προσθήκη του banner εικόνας στο κάτω μέρος του embed
    embed.set_image(url="https://i.postimg.cc/HxJDTG0T/content.png")
    
    await ctx.send(embed=embed, view=InitialTicketView())

# --- Εκκίνηση του Bot ---
bot.run(TOKEN)
