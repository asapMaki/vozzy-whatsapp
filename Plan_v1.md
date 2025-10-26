# Plan: Claude Asistent za Mahira - Svakodnevna Podrška IT/Administracija

**Verzija:** 1.1
**Datum:** 26.10.2025
**Status:** U Implementaciji

---

## 📊 Analiza Tvoje Uloge

**Mahir Kadić** - IT & Administracija / Organizacija poslovanja:

- ✅ Administracija cijele firme
- ✅ Organizacija procesa
- ✅ Društvene mreže
- ✅ Sve što je vezano za tehnologiju
- ✅ Korištenje AI tehnologija
- ✅ Upravljanje sa 2 radnika (Harun - IT partner, Muhammed - praktikant)

---

## 🎯 Strategija: Claude Kao Tvoj Glavni Asistent

### Faza 1: Custom Skillovi Za Tvoj Svakodnevni Rad

**A. Dokumentacioni Skillovi (Najviši Prioritet)**

1. **`gastrohem-media-processor`** - Audio/Slike → Markdown/JSON ✅ **IMPLEMENTIRANO**

   - Audio transkripcija paralelno (3x brže) → `.json` fajlovi
   - Slike OCR sa prirodnim sažetkom → `.md` fajlovi fokusirani na Gastrohem info
   - Automatski skenira sve odjele za današnji datum
   - Usage: `process media` ili `process media for 24.10`
   - WhatsApp glasovne poruke
   - Slike dokumenata/whiteboard-a
   - Screenshot-ovi

2. **`/dnevni-summary`** - Analizira sve chat.md iz današnjeg dana

   - Pregleda sve odjele
   - Izvlači tvoje taskove
   - Kreira akcioni plan za tebe

3. **`/sedmicni-summary`** - Nedeljni izvještaj

   - Sve što si uradio
   - Sve što tvoj tim treba da uradi
   - Blokeri i prioriteti

4. **`/ekstraktor-kontakata`** - Iz razgovora izvlači:

   - Nove klijente
   - Partnere
   - Konkurente
   - Automatski ih dodaje u gastrohem kompanija/

5. **`/task-tracker`** - Iz svih chat.md ekstraktuje:
   - Task-ove za tebe
   - Task-ove za Haruna
   - Task-ove za Muhammeda
   - Deadlines i prioritete

**B. Organizacioni Skillovi**

6. **`/tim-status`** - Pregled tvojih radnika

   - Šta radi Harun (ad-hoc zadaci)
   - Šta radi Muhammed (društvene mreže, AI research)
   - Task queue za oba

7. **`/admin-check`** - Daily checklist administrativnih stvari

   - Email provjera
   - Dokumenti pending
   - IT alati status
   - Social media aktivnost

8. **`/sastanak-prep`** - Priprema za sastanke menadžmenta
   - Šta si završio od prošlog sastanka
   - Blokirajući problemi
   - Prijedlozi i pitanja

**C. IT & Digital Skillovi**

9. **`/infrastruktura-status`** - Pregled digitalne infrastrukture

   - Domene (gastrohem.ba, .at)
   - Email setup
   - Social media kanali
   - Bar-kod sistem progress (Kenan/Keto)

10. **`/repo-cleanup`** - Održavanje repozitorija
    - Provjera strukture foldera
    - Nedostajući summary-ji
    - Prazni folderi
    - Nekonzistentnosti

---

### Faza 2: Repository Organizacija - Najbolja Struktura Za Tebe

**Trenutna Struktura (Dobra, Ali Treba Proširiti):**

```
gastrohem-menadzment/
├── CLAUDE.md              # Uputstva
├── TASKOVI.md             # Operativni taskovi
├── gastrohem kompanija/   # Centralna evidencija
│   └── osoblje/
│       ├── menadzeri.md
│       └── radnici.md
└── gastrohem whatsapp/    # Komunikacije po odjelima
```

**NOVA STRUKTURA - Prilagođena Za Tvoj Rad:**

```
gastrohem-menadzment/
├── CLAUDE.md
├── TASKOVI.md
├── Plan_v1.md                          # Ovaj dokument
│
├── mahir/                              # 🆕 TVOJ LIČNI FOLDER
│   ├── daily-logs/                     # Dnevni zapisi
│   │   └── 2025-10-26.md
│   ├── weekly-reviews/                 # Sedmični review-ji
│   │   └── 2025-W43.md
│   ├── tim/                            # Tvoj tim
│   │   ├── harun-tasks.md
│   │   └── muhammed-tasks.md
│   ├── admin-checklist.md              # Šta pratiš svakodnevno
│   └── it-projekti.md                  # IT projekti u toku
│
├── gastrohem kompanija/
│   ├── djelatnost/                     # 🆕 Šta nudimo
│   │   ├── oprema.md
│   │   ├── servis.md
│   │   ├── hemija.md
│   │   └── marketing-usluge.md
│   ├── osoblje/
│   │   ├── menadzeri.md
│   │   └── radnici.md
│   ├── lokacije/                       # 🆕 Prostori i tržišta
│   │   ├── sarajevo-vogosca.md
│   │   ├── salzburg-at.md
│   │   └── trzista-plan.md
│   ├── klijenti/                       # 🆕 Baza klijenata
│   │   ├── README.md (indeks)
│   │   └── [pojedinaćni klijenti]
│   ├── partneri/                       # 🆕 Poslovni partneri
│   │   └── marijana-salzburg.md
│   └── konkurencija/                   # 🆕 Analiza konkurenata
│
├── gastrohem whatsapp/                 # Postojeće (ostaje)
│   ├── administracija/
│   ├── finansije/
│   ├── prodaja/
│   ├── servis/
│   ├── svaštara/
│   ├── sastanci menadžmenta/
│   └── adis-chat/
│
└── .claude/                            # 🆕 Claude Code konfiguracija
    └── commands/                       # Custom slash commands (skillovi)
        ├── transkribuj.md
        ├── dnevni-summary.md
        ├── sedmicni-summary.md
        ├── ekstraktor-kontakata.md
        ├── task-tracker.md
        ├── tim-status.md
        ├── admin-check.md
        ├── sastanak-prep.md
        ├── infrastruktura-status.md
        └── repo-cleanup.md
```

---

### Faza 3: Tvoj Svakodnevni Workflow Sa Claude

**🌅 UJUTRO (09:00)**

```bash
/admin-check          # Šta čeka danas
/tim-status           # Šta rade Harun i Muhammed
/dnevni-summary       # Šta se desilo juče u WhatsApp-u
```

**📊 TOKOM DANA**

```bash
process media         # Procesira sve audio/slike iz današnjih foldera ✅
/task-tracker         # Kad treba dodjeliti taskove
/ekstraktor-kontakata # Kad se pomene novi klijent/partner
```

**🌙 NAVEČER (18:00)**

```bash
mahir/daily-logs/2025-10-26.md  # Šta si uradio
/tim-status                      # Šta je tim završio
```

**📅 NEDJELJA**

```bash
/sedmicni-summary     # Izvještaj cijele sedmice
/sastanak-prep        # Priprema za monday meeting
```

---

### Faza 4: Ažuriranje CLAUDE.md - Nova Sekcija Za Tebe

Dodati sekciju:

```markdown
## Mahir Kadić - Tvoj Rad Sa Claude

### Tvoja Uloga

- IT & Administracija / Organizacija poslovanja
- Upravljanje radnicima: Harun (IT partner), Muhammed (praktikant)
- Digitalna infrastruktura, društvene mreže, AI tehnologije

### Tvoji Custom Skillovi

- `/transkribuj` - Audio/slike → dokumentacija
- `/dnevni-summary` - Pregled dnevnih aktivnosti
- `/sedmicni-summary` - Nedeljni izvještaj
- `/ekstraktor-kontakata` - Automatska evidencija klijenata/partnera
- `/task-tracker` - Task management za tim
- `/tim-status` - Status Haruna i Muhammeda
- `/admin-check` - Daily admin checklist
- `/sastanak-prep` - Priprema za sastanke
- `/infrastruktura-status` - IT infrastruktura pregled
- `/repo-cleanup` - Održavanje repozitorija

### Tvoj Daily Workflow

[Detaljno kao u Fazi 3]
```

---

### Faza 5: Ažuriranje TASKOVI.md - Restrukturiranje

Dodati sekcije po osobama:

```markdown
## 🔴 Mahir - Visok Prioritet

### Kreiranje Claude Skillova

- [x] ✅ Skill `gastrohem-media-processor` (audio/slike → .json/.md)
- [ ] Skill /dnevni-summary
- [ ] Skill /sedmicni-summary
- [ ] Skill /ekstraktor-kontakata
- [ ] Skill /task-tracker
- [ ] Skill /tim-status
- [ ] Skill /admin-check
- [ ] Skill /sastanak-prep
- [ ] Skill /infrastruktura-status
- [ ] Skill /repo-cleanup
- [ ] Skill /internal-comms - preurediti da odgovara gastrohemu
- [ ] Skill da obriše sve audio i slike iz dnevnih foldera

### IT & Digital Infrastruktura

- [ ] Postaviti gastrohem.at domenu
- [ ] Konfigurisati email @gastrohem.ba / .at za sve
- [ ] Social media kanali (BA i AT/DE odvojeno)
- [ ] Bar-kod sistem i skeneri (koordinacija sa Kenanom/Keto)

### Administracija

- [ ] Kompletirati gastrohem kompanija/ evidenciju
- [ ] Kreirati mahir/ folder strukturu
- [ ] Postaviti daily/weekly workflow
- [ ] Template-i za dokumentaciju

---

## 🟡 Harun - IT Partner Taskovi

- [ ] [Ad-hoc IT zadaci kako budu dolazili]
- [ ] Podrška u sistemima i alatima
- [ ] Integracije (prema potrebi)

---

## 🟢 Muhammed - Praktikant Taskovi

- [ ] Social media setup i održavanje
- [ ] AI research za automatizaciju
- [ ] Tehnološka i administrativna pomoć
- [ ] Ad-hoc zadaci
```

---

## ✅ TRENUTNI STATUS IMPLEMENTACIJE

**26.10.2025 - Završeno:**

### 1. `gastrohem-media-processor` Skill ✅

**Što radi:**
- Automatski procesira audio i slike iz WhatsApp dnevnih foldera
- Audio: Paralelna transkripcija (do 3 istovremeno) → `.json` fajlovi
- Slike: OCR sa prirodnim sažetkom → `.md` fajlovi
- Default: Koristi današnji datum, skenira sve odjele

**Struktura output-a:**

Audio (`.json`):
```json
{
  "speakers": [],
  "chunks": [...],
  "text": "Full transcribed text"
}
```

Slike (`.md`):
```markdown
# image.png

**Poslao:** Mahir Kadic
**Datum:** 26.10.2025 13:58

---

[Prirodan sažetak fokusiran na Gastrohem-relevantne informacije:
 kontakti, imena, emailovi, brojevi telefona, poslovni detalji]
```

**Performance:**
- Audio: ~3-5 sec po fajlu (paralelno)
- Slike: ~2-3 sec po slici (batch)
- Scan svih odjela: <1 sekunda

**Lokacija:** `.claude/skills/gastrohem-media-processor/`

---

## 📋 IMPLEMENTACIONI PLAN

### **Korak 1**: Kreirati `mahir/` folder strukturu

- `daily-logs/`, `weekly-reviews/`, `tim/`
- Admin checklist template
- IT projekti tracking

### **Korak 2**: Proširiti `gastrohem kompanija/`

- Dodati `djelatnost/`, `lokacije/`, `klijenti/`, `partneri/`, `konkurencija/`
- Ekstraktovati podatke iz postojećih chat.md fajlova

### **Korak 3**: Kreirati `.claude/commands/` skillove

- 10 custom slash komandi
- Svaki skill sa jasnim uputstvom

### **Korak 4**: Ažurirati CLAUDE.md

- Dodati sekciju za Mahira
- Workflow uputstva
- Skill dokumentacija

### **Korak 5**: Restrukturirati TASKOVI.md

- Po osobama (Mahir, Harun, Muhammed)
- Po prioritetima
- Sa deadlines gdje postoje

---

## ⚡ Dodatne Preporuke

**1. GitHub Actions / Automatizacija (Buduće):**

- Daily reminder u 09:00 za `/admin-check`
- Auto-kreiranje `mahir/daily-logs/YYYY-MM-DD.md`
- Weekly reminder nedeljom za `/sedmicni-summary`

**2. Templates:**

- Template za daily log
- Template za weekly review
- Template za sastanak prep
- Template za klijente/partnere

**3. Integracije (Buduće):**

- WhatsApp → auto transkript
- Email → taskovi u TASKOVI.md
- Calendar → deadline tracking

---

## 🎯 Očekivani Rezultati

Nakon implementacije:

- ✅ **10 minuta dnevno** umjesto 1 sat za administraciju
- ✅ **Automatsko** praćenje taskova iz WhatsApp-a
- ✅ **Centralizovana** evidencija svih kontakata i informacija
- ✅ **Efikasno** upravljanje timom (Harun, Muhammed)
- ✅ **Organizovan** pregled svega u jednom mjestu
- ✅ **AI-powered** pomoć u svakodnevnim zadacima

---

## 📝 Napomene

- Ovaj plan je **draft** - može se prilagođavati prema potrebama
- Prioritet je na **praktičnosti** - samo ono što ti stvarno pomaže
- Fokus na **automatizaciju** ponavljajućih taskova
- **Iterativni pristup** - implementirati postepeno, testirati, prilagoditi

---

**Sljedeći Koraci:**

1. ~~Review plana~~ ✅
2. ~~Odlučiti prioritete~~ ✅
3. Početi sa implementacijom po fazama ⏳ **U TOKU**

---

## 📝 Version History

### v1.1 (26.10.2025)
- ✅ Implementiran `gastrohem-media-processor` skill
- Refaktorisan image OCR: `.json` → `.md` sa prirodnim sažetkom
- Audio transkripcija ostaje `.json` (output iz insanely-fast-whisper)
- Dodana "Trenutni Status Implementacije" sekcija
- Ažuriran task tracking i workflow
- Status promijenjen: Draft → U Implementaciji

### v1.0 (26.10.2025)
- Inicijalni plan
- Definisano 10 custom skillova
- Predložena nova struktura repozitorija
- Definisan daily/weekly workflow
