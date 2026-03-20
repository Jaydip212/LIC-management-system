# MySQL Workbench - Database Manage Karnyachi Purna Process

He guide **LIC Management System** cha database check karnya aani tya madhe changes karnyabaddal aahe.

## Step 1: MySQL Workbench Open Kara

1. Tumchya computer var khali taskbar madhe **MySQL Workbench** search kara aani te app open kara.
2. Open zalyavar home screen var **"MySQL Connections"** chya khali **"Local instance MySQL80"** (kiva tumcha connection box) asel, tyavar click kara.
3. Jar password vicharla tar tumcha password taka (udhaharanarth: `Jaydip@123`) aani OK kara.

## Step 2: Database Select Kara

1. Workbench open zalyvar, window chya left side la khali don tabs distil: **"Administration"** aani **"Schemas"**.
2. Tya pakki **"Schemas"** tab var click kara.
3. Tithe tumhala tumchya projects chya databases chi list disel. Tya list madhil **`lic_management`** var double-click kara. (Double-click kelyamule hya database che nav **bold** hoil, yacha artha to database successfully select zala aahe).

## Step 3: Tables Bagha

1. **`lic_management`** chya aatmadhe **"Tables"** navacha dropdown/folder asel, tyavar click karun to expand kara.
2. Ithe tumhala apli sagli tables distil: `agents`, `claims`, `contact_messages`, `customers`, `policies`, `premium_payments`, vagere.

## Step 4: Data Check Ani Edit Kara (Changes Karnyachi Process)

1. Kontehi table (udhaharanarth: `customers`) war apla mouse cha arrow ghevun jaa.
2. Table navachya ekdam ujavya (right) bajula tine (3) chote icons distil. Tyatil shevatacha aani **chota grid/table cha icon** asel. (hya icon var mouse thevlya var 'Select Rows - Limit 1000' asa lihilela yeil). Tya icon var click kara.
3. Ek navin tab (Results Grid) open hoil center la, ithe tumhala database madhil aatla sagla data disel. (Ithech tumhala tumche add kelele Marathi names pan distil).
4. **Data Change (Edit) Karnyasaathi:**
   - Grid madhil kontyahi cell (box) madhe je badlaychay tya var double-click kara.
   - Puna click karun backspace ne khoda aani navin mahiti (nav, number, etc.) type kara.
5. **Navin Data (Row) Add Karnyasaathi:**
   - Grid chya ekdam khali ek empty (rikaami) blank row asel (jithe `null` lihila asel). Tithe click karun tumhi ahet tithe navin entry type karu shakta.

## Step 5: Changes Save Kara (Khup Important!)

1. Kontahi change kelya vr, screen chya khali ujavya (right) bajula ek **"Apply"** button active hoil. Tya **Apply** button var nkkii click kara. (Jar click nahi kel tar changes save honar nahi).
2. Ek navin popup window yeil jyat database saathi SQL code asel. Tya window madhe pan khali **"Apply"** var click kara.
3. Aani shevti **"Finish"** var click kara.
4. Tumche changes ataa successfully database madhe aani tumchya website var save zale ahet!
