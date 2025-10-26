# CLAUDE.md

Ovaj fajl pruža uputstva za Claude Code (claude.ai/code) prilikom rada u ovom repozitoriju.

## Svrha Repozitorija

Ovo je **centralna evidencija za Gastrohem biznis** - nije repozitorij za kodiranje već za:

- Praćenje svih WhatsApp community komunikacija
- Evidenciju informacija o kompaniji (djelatnost, menadžment, radnici, lokacije, klijenti, partneri, konkurencija)
- Praćenje sastanaka i odluka
- Arhiviranje svih poslovnih informacija vezanih za Gastrohem

**Primarni jezik**: Bosanski (BS)

## Struktura Repozitorija

### Glavne Fascikle

**gastrohem kompanija/** - Centralna evidencija kompanije:
- Ideja i djelatnost firme
- Lista menadžera
- Lista radnika
- Lokacije
- Klijenti
- Partneri
- Konkurencija

**gastrohem whatsapp/** - Evidencija WhatsApp community komunikacija po odjelima:
- **administracija/** - Administrativni taskovi, tehnička pitanja
- **finansije/** - Finansijske teme, troškovi, planiranje
- **prodaja/** - Prodajne aktivnosti, klijenti, ponude
- **servis/** - Servisne intervencije, problemi, rješenja
- **svaštara/** - Opšte diskusije
- **sastanci menadžmenta/** - Formalni sastanci i odluke
- **adis-chat/** - Direktna komunikacija sa Adisom

### Organizacija po Datumima

Komunikacije se organizuju po **sedmicama** (format `DD.MM - DD.MM`), a unutar njih po **danima**:

```
gastrohem whatsapp/{odjel}/
  ├── 20.10 - 27.10/           # Sedmični folder
  │   ├── 24.10/               # Dnevni folder
  │   │   ├── chat.md          # Transkript razgovora za taj dan
  │   │   ├── summary.md       # Dnevni summary
  │   │   ├── *.json           # Audio/slika transkripcije
  │   │   └── *.png/pdf        # Dokumenti, slike
  │   ├── 25.10/               # Sljedeći dan
  │   ├── 26.10/
  │   └── sedmicni-summary.md  # Summary cijele sedmice
  └── 27.10 - 03.11/           # Sljedeća sedmica
      ├── 27.10/
      └── ...
```

**Napomena**: Dnevni folderi su fizički unutar sedmičnih foldera. Sedmica počinje nedeljom.

## O Kompaniji Gastrohem

### Djelatnost (iz opis-gastrohem.json)

Gastrohem je kompanija koja nudi **sve iz jedne ruke** za gastronomiju i hoteljarstvo:

**Oprema i Prodaja:**
- Nove mašine i oprema
- Dijelovi za opremu
- Oprema za hotele (peškiri, kuhinjske potrebštine)
- Dozatori za WC, papiri
- Oprema za vešeraj

**Servis:**
- Profesionalni EU-standard servis
- Male popravke na licu mjesta
- Za veće popravke: zamjena sa rezervnom mašinom dok se mušterijina ne popravi
- Klijent može nastaviti rad bez prekida

**Hemija:**
- Hemija za gastronomiju
- Hemija za hotele
- Hemija za vešeraj

**Marketing i Dodatne Usluge:**
- Promotivni materijal (jeftiniji za partnere)
- Grafičke usluge (menije, karte, opisi poslovanja)
- Brendirani artikli (majice, nošnje za kuhinju, upaljači, olovke, vizitke, letci)
- Partnerski program: roll-up display u objektu = dodatni procenti i povoljnosti

### Menadžment i Radnici

**Core Menadžment:**
- **Adis Kadric** - Core management, AT/DE tržišta i partnerstva
- **Muhamed Nukić** - Core management, strategija i komercijala

**Operativni Tim:**
- **Adnan Erović** - Lokacije/logistika (Sarajevo/Vogošća), infrastruktura
- **Mahir** - Administracija/Finansije/IT & Digital, web, dokumentacija
- **Haris (BiH)** - Servis & nabavka, tehnički pre-sales, obuka
- **Haris (Tutin/Srbija)** - Prodaja Sandžak region (Pazar, Kraljevo, Raška)
- **Ševal** - Field sales menadžer (DE/AT + BiH) - 3 mjeseca proba

### Trenutne Lokacije i Planovi (iz meeting.md 23.10.2025)

**U toku:**
- Sarajevo/Vogošća - prostor u užem izboru, sastanci sa vlasnikom
- Salzburg (AT) - besplatno 500 m² skladište + 200 m² showroom kod partnera "Marijana"

**Tržišta:**
- BiH - domaće tržište
- AT/DE - Austrija i Njemačka (paralelno pokretanje)
- Srbija - Sandžak region

**Cilj otvaranja:** 1.12.2025 (idealno) ili 03.01.2026 (backup)

## Dokumentacioni Workflow

### Trenutni Proces

1. WhatsApp razgovori se prepisuju ili transkribuju
2. Audio/slike → JSON format sa timestamp-ovima
3. Sve ide u dnevni `chat.md` fajl
4. Kreira se `summary.md` koji izvlači:
   - Šta je ko uradio
   - Šta bi ko trebao da uradi
   - Ključne odluke i akcije

### Planirana Automatizacija

Za detaljan tracking operativnih taskova, vidi **[TASKOVI.md](TASKOVI.md)**

## Format Summary Fajlova

Summary fajlovi koriste standardni format sa sekcijama po osobi:

```markdown
# Summary - Naziv Teme (DD.MM.YYYY)

## **Ime Prezime**

### Što je uradio:
- Konkretne akcije koje je osoba izvršila

### Što bi trebao da uradi:
- Akcioni stavovi za ubuduće
```

## Standardi Rada (iz meeting.md)

- **Fokus na isporuku**: Nema 'radnog vremena' do stabilizacije
- **Profesionalizam**: Dress code, uredno, tačnost
- **Sigurnost**: Nulta tolerancija na curenje informacija
- **Evidencija**: Sve se dokumentuje u odgovarajućim kanalima
- **Komunikacija**: Interna komunikacija kroz 'community' kanale po odjelima

## Imenovanje Fajlova

Kanonski format:
```
YYYY-MM-DD_Tema_Verb.ext
```

Za dnevne foldere:
```
DD.MM/
```

## Digitalna Infrastruktura (planirana/u toku)

- **Domene**: gastrohem.ba (postojeća), gastrohem.at (u pripremi)
- **Email format**: i.prezime@gastrohem.ba / .at
- **Social media**: Odvojeni kanali za BA i AT/DE
- **Softver**: Vodi Kenan/Keto - bar-kod sistem i skeneri

## Rad sa Ovim Repozitorijem

- **Jezik**: SVE na bosanskom jeziku
- **Format datuma**: DD.MM.YYYY (evropski)
- **Checkboxes**: Koristi `- [ ]` za taskove
- **Struktura**: Odvajaj po odjelima i datumima
- **Summary**: Uvijek izvlači konkretne akcije i dodijeli osobama
- **Svrha**: Dokumentuj SVE vezano za Gastrohem biznis - ovo je centralna evidencija
