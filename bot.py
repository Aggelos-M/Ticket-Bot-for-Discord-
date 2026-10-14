import discord
from discord.ext import commands
from discord.ui import View, Select, Button

# ΡΥΘΜΙΣΕΙΣ (Συμπλήρωσε τα δικά σου στοιχεία) 
TOKEN = "MTU1OTk0NTQxOTc1NTIzMzM0MA.GaEBO2.iZDYKPHTfZf-4ehXrIPrBEvc85aqXXDsEbP2TU"
CATEGORY_ID = 1310237114310463583 # Το ID της κατηγορίας όπου θα ανοίγουν τα Tickets
STAFF_ROLE_ID = 1310237113018744928  # Το ID του Role των Staff που θα βλέπουν τα tickets

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dropdown Menu με τις 4 Επιλογές 
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="RP Issue", description="Πρόβλημα που σχετίζεται με το Roleplay", emoji="🎭"),
            discord.SelectOption(label="Connect Issue", description="Πρόβλημα σύνδεσης στον RedM server", emoji="🔌"),
            discord.SelectOption(label="Support Issue", description="Γενικό θέμα υποστήριξης", emoji="🛠️"),
            discord.SelectOption(label="Question", description="Έχεις κάποια απορία;", emoji="❓"),
        ]
        super().__init__(placeholder="Επίλεξε την κατηγορία του ticket σου...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True) # Εμποδίζει το "Interaction Failed"
        
        selected_option = self.values[0]
        guild = interaction.guild
        user = interaction.user

        # Έλεγχος αν υπάρχει η κατηγορία
        category = guild.get_channel(CATEGORY_ID)
        staff_role = guild.get_role(STAFF_ROLE_ID)

        # Δικαιώματα πρόσβασης στο νέο κανάλι
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Δημιουργία του καναλιού ticket
        channel_name = f"ticket-{user.name}".lower()
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        # Μήνυμα μέσα στο νέο κανάλι του ticket
        embed_ticket = discord.Embed(
            title=f"Eclipse Roleplay - Support Ticket",
            description=f"Γεια σου {user.mention}!\n\n**Κατηγορία:** `{selected_option}`\n\nΠαρακαλώ γράψε εδώ αναλυτικά την ερώτηση ή το πρόβλημα που αντιμετωπίζεις και ένα μέλος της ομάδας μας θα σου απαντήσει το συντομότερο δυνατό.",
            color=discord.Color.red()
        )
        await ticket_channel.send(content=f"{user.mention} {staff_role.mention if staff_role else ''}", embed=embed_ticket)

        # Επιβεβαιωτικό μήνυμα στον χρήστη (ορατό μόνο σε αυτόν)
        await interaction.followup.send(
            content=f"✅ **Ticket successfully created!**\nΜπορείς να κάνεις την ερώτησή σου στο κανάλι: {ticket_channel.mention}",
            ephemeral=True
        )

class TicketSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# --- Κουμπί "Create Ticket" ---
class InitialTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket", style=discord.ButtonStyle.danger, custom_id="open_ticket_btn", emoji="📩")
    async def ticket_button(self, interaction: discord.Interaction, button: Button):
        # Όταν πατάει το κουμπί, του εμφανίζει το Dropdown Menu
        embed_options = discord.Embed(
            title="Eclipse Roleplay - Επιλογή Κατηγορίας",
            description="Παρακαλώ επίλεξε την κατηγορία που ταιριάζει στο αίτημά σου από το παρακάτω μενού:",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed_options, view=TicketSelectView(), ephemeral=True)

# --- Συμβάν όταν το Bot είναι Online ---
@bot.event
async def on_ready():
    print(f'Έγινε σύνδεση ως {bot.user.name} (Eclipse Roleplay Bot)')
    bot.add_view(InitialTicketView()) # Διατηρεί τα κουμπιά λειτουργικά ακόμα κι αν κάνει restart το bot

# --- Εντολή για αποστολή του Embed Panel στο κανάλι ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    await ctx.message.delete()
    
    embed = discord.Embed(
        title="🌵 Καλώς ήρθατε στον Eclipse Roleplay 🌵",
        description=(
            "Χρειάζεστε βοήθεια ή έχετε κάποια απορία;\n\n"
            "Πατήστε το κουμπί **Ticket** παρακάτω για να ανοίξετε ένα κανάλι επικοινωνίας με την ομάδα υποστήριξης (Staff Team)."
        ),
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="Eclipse RedM Roleplay • Ticket System")
    
    await ctx.send(embed=embed, view=InitialTicketView())

    bot.run("MTU1OTk0NTQxOTc1NTIzMzM0MA.GaEBO2.iZDYKPHTfZf-4ehXrIPrBEvc85aqXXDsEbP2TU")
