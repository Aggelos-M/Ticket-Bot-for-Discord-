Discord Ticket Bot 🎟️

Ένα πλήρως λειτουργικό Discord Bot γραμμένο σε Python (`discord.py`) για τη διαχείριση tickets, ειδικά σχεδιασμένο για servers (όπως RedM / Roleplay).

## 🚀 Τι κάνει αυτός ο κώδικας;

1. **Σύστημα Panel Tickets (`!setup_ticket`):**

   * Δημιουργεί ένα όμορφο embed μήνυμα με banner και κουμπί επιλογής (`📩 Ticket`).

2. **Μενού Κατηγοριών (Dropdown Menu):**

   * Όταν ο χρήστης πατήσει το κουμπί, εμφανίζεται μενού επιλογής ανάμεσα σε 6 κατηγορίες:

     * 🤠 **RP Issue** (Προβλήματα Roleplay)

     * 🛜 **Connection Issue** (Προβλήματα σύνδεσης στον server)

     * ⚙️ **Support Issue** (Γενική υποστήριξη)

     * ❓ **Question** (Απορίες)

     * 💸 **Donation support** (Θέματα δωρεών)

     * 💥 **Bug report** (Αναφορά bugs)

3. **Αυτόματη Δημιουργία Καναλιού:**

   * Δημιουργεί ιδιωτικό κανάλι μέσα στην αντίστοιχη κατηγορία του Discord, δίνοντας πρόσβαση **μόνο** στον χρήστη που το άνοιξε και στο Staff.

4. **Έλεγχος Διπλών Tickets:**

   * Αποτρέπει έναν χρήστη από το να ανοίγει πολλαπλά active tickets ταυτόχρονα.

5. **Ασφαλές Κλείσιμο Ticket:**

   * Κάθε ticket περιέχει κουμπί κλεισίματος (`🔒 Close Ticket`) το οποίο **επιτρέπεται να πατήσουν αποκλειστικά Administrators ή χρήστες με το Staff Role**.

## 🛠️ Οδηγίες Εγκατάστασης & Ρύθμισης στο Discord

### Βήμα 1: Δημιουργία του Bot στο Discord Developer Portal

1. Πήγαινε στο [Discord Developer Portal](https://discord.com/developers/applications).

2. Κάνε κλικ στο **New Application** και δώσε του ένα όνομα (π.χ. *Eclipse Ticket Bot*).

3. Πήγαινε στην καρτέλα **Bot** από το αριστερό μενού και κάνε κλικ στο **Add Bot**.

4. Κάτω από το Username, βρες το **Token** και κάνε κλικ στο **Reset Token** (ή Copy). Αυτό είναι το `TOKEN` σου.

5. Στην ίδια σελίδα, κύλησε προς τα κάτω στα **Privileged Gateway Intents** και ενεργοποίησε και τα τρία:

   * ✅ **Presence Intent**

   * ✅ **Server Members Intent**

   * ✅ **Message Content Intent**

### Βήμα 2: Πρόσκληση του Bot στον Server σου

1. Πήγαινε στην καρτέλα **OAuth2** -> **URL Generator**.

2. Στις επιλογές **Scopes** τσέκαρε:

   * `bot`

   * `applications.commands`

3. Στις επιλογές **Bot Permissions** τσέκαρε:

   * `Administrator` (ή τουλάχιστον: *Manage Channels, Read Messages/View Channels, Send Messages, Manage Messages*).

4. Αντέγραψε το Generated URL στο κάτω μέρος, άνοιξέ το στον browser σου και πρόσθεσε το bot στον Discord server σου.

### Βήμα 3: Ρύθμιση του Κώδικα (`bot.py`)

Άνοιξε το αρχείο `bot.py` και αντικατάστησε τις μεταβλητές στην αρχή του κώδικα με τα δικά σου στοιχεία:

* `TOKEN`: Βάζεις το token που πήρες από το Developer Portal.

* `STAFF_ROLE_ID`: Το ID του ρόλου των Staff στον server σου (επιτρέπεται να κλείνουν tickets και να τα βλέπουν).

* Τα IDs κατηγοριών (`RP_CATEGORY_ID`, `CONNECTION_CATEGORY_ID` κλπ.): Τα IDs από τις κατηγορίες καναλιών του Discord όπου θέλεις να δημιουργούνται τα αντίστοιχα tickets.

*(💡 **Tip για να βρεις IDs στο Discord:** Ενεργοποίησε τα Developer Mode στις ρυθμίσεις του Discord (Settings -> Advanced -> Developer Mode), κάνε δεξί κλικ σε ρόλους ή κατηγορίες και πάτα "Copy ID").*

### Βήμα 4: Εκτέλεση του Bot

1. Βεβαιώσου ότι έχεις εγκατεστημένη την Python και τη βιβλιοθήκη `discord.py`:

   ```
   pip install discord.py
   
   ```

2. Τρέξε το bot σου από το τερματικό:

   ```
   python bot.py
   
   ```

3. Μπες στον Discord server σου και γράψτε σε κάποιο κανάλι την εντολή:

   ```
   !setup_ticket
   
   ```

   *(Η εντολή απαιτεί δικαιώματα Administrator).* Το μήνυμα/panel υποστήριξης θα εμφανιστεί αυτόματα!
