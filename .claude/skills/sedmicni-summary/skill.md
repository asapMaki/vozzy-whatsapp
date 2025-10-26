---
name: sedmicni-summary
description: Create weekly summaries by aggregating daily summaries for Gastrohem WhatsApp conversations. This skill should be used when the user asks to generate weekly summaries, see what happened during the week, or prepare plans for next week (e.g., "Make weekly summary", "Generiši sedmični summary", "Weekly report for 20.10-27.10"). Aggregates activities per person, detects completed tasks, and generates next week's plan.
---

# Sedmični Summary

## Overview

Kreira sedmične summaries agregacijom svih dnevnih summaries iz sedmice - analizira aktivnosti i generiše planove.

**Što radi:**
- Pronalazi sve dnevne `summary.md` fajlove u sedmičnom folderu
- **Podrška za dva tipa summaries:**
  - **Person-based** (po osobama) - Administracija, Svaštara
  - **Topic-based** (po temama) - Finansije, Servis
- Agregira aktivnosti po osobama ili temama kroz cijelu sedmicu
- Detektuje završene taskove (checkboxes, ključne riječi)
- **Generiše plan za narednu sedmicu** baziran na aktivnostima
- Kreira `sedmicni-summary.md` u root-u sedmičnog foldera

**Performance:**
- Procesira sve dnevne summaries za sedmicu
- Automatski detektuje format (person-based vs topic-based)
- Agregira po osobama ili temama
- Generiše planova pomoću pattern matching

**Note:** Script radi kompletnu agregaciju i generisanje - Claude može dodatno analizirati ako je potrebno.

## When to Use This Skill

User says:
- "Make weekly summary"
- "Generiši sedmični summary"
- "Weekly report"
- "What happened this week"
- "Summary for 20.10 - 27.10"

**Default behavior:** Processes all weekly folders, generates summary for each.

## Workflow

### Simple Usage

**Weekly summary for all weeks:**
```bash
python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py
```
- Finds all weekly folders across departments
- Generates `sedmicni-summary.md` for each week

**Weekly summary for specific week:**
```bash
python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py --week "20.10 - 27.10"
```

**Weekly summary for specific department:**
```bash
python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py --dept "svaštara"
```

**Combine filters:**
```bash
python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py --week "20.10 - 27.10" --dept "finansije"
```

### What Happens

**Step 1: Find daily summaries**
- Scans weekly folder for all daily folders (DD.MM pattern)
- Finds `summary.md` in each daily folder
- Sorts by date chronologically

**Step 2: Parse daily summaries**
- Automatski detektuje tip summary-ja (person-based ili topic-based)
- **Person-based:** Ekstraktuje aktivnosti iz "**Aktivnosti:**" sekcija po osobama
- **Topic-based:** Ekstraktuje sve bullet points kao aktivnosti pod nazivom teme
- Podržava multiple formata (current, legacy, tematski)
- Uklanja timestamp-ove, čuva čist tekst aktivnosti

**Step 3: Aggregate by person**
- Groups all activities by person across the week
- Detects completed tasks using:
  - Checked checkboxes: `[x]` or `[X]`
  - Keywords: "završeno", "done", "completed", "gotovo", "urađeno"
- Identifies ongoing tasks (not completed)

**Step 4: Generate next week plan**
- Includes incomplete tasks from "u_toku"
- Analyzes activity patterns (sastanak, dokument, nabavka, servis, prodaja)
- Suggests continuations based on common themes

**Step 5: Write sedmicni-summary.md**
- Creates structured markdown in weekly folder root
- Includes: activities, completed tasks, next week plan
- Path: `gastrohem whatsapp/{odjel}/{sedmica}/sedmicni-summary.md`

## Summary Format

```markdown
# Sedmični Summary - {Odjel} ({DD.MM - DD.MM})

**Period:** 20.10 - 27.10
**Broj dana:** 5
**Aktivnih osoba:** 6

---

## **Ime Prezime**

### Aktivnosti u sedmici:
- [24.10] Aktivnost 1
- [25.10] Aktivnost 2
- [26.10] Aktivnost 3

### Završeni taskovi:
- ✅ Task koji je završen
- ✅ Drugi završen task

### Plan za narednu sedmicu:
- Nastaviti sa nedovršenim zadacima:
  - Task 1 koji nije završen
  - Task 2 koji treba nastaviti
- Planirati sljedeće sastanke
- Nastaviti sa dokumentacijom
```

**Primjer stvarnog sedmičnog summary-ja:**

```markdown
# Sedmični Summary - Svaštara (20.10 - 27.10)

**Period:** 20.10 - 27.10
**Broj dana:** 2
**Aktivnih osoba:** 6

---

## **Haris Grupacija**

### Aktivnosti u sedmici:
- [24.10] Amin
- [24.10] Allejkumu sellam,ima fabrika u Jelahu gdje sam isao po boce za hemiju trebalo.bi da oni to mog...
- [24.10] Lifeplast se zove
- [24.10] Sutra zovem elmu da mi da kontakt broj insallah
- [24.10] Moramo i sa elmom provjeriti da li moze obicne kante ili moraju biti one jace jer ide za izvoz...

### Završeni taskovi:
- *(Nema eksplicitno označenih završenih taskova)*

### Plan za narednu sedmicu:
- Nastaviti sa tekućim aktivnostima

---

## **Seval Grupacija**

### Aktivnosti u sedmici:
- [24.10] Mašala brate ti si mašina😉
- [24.10] VIS d.o.o. (Banja Luka)
- [24.10] kapaciteti do 30 litara liferplast pravi
- [24.10] Idealno ti je 15 litara
- [24.10] Evo broja za firmu Lifeplast d.o.o.: +387 32 663 633.

### Završeni taskovi:
- *(Nema eksplicitno označenih završenih taskova)*

### Plan za narednu sedmicu:
- Nastaviti sa tekućim aktivnostima
```

## Script Reference

### generate_weekly_summary.py

**Purpose:** Aggregate daily summaries into weekly summaries with task detection and next week planning

**Usage:**
```bash
# Process all weekly folders
python scripts/generate_weekly_summary.py

# Specific week
python scripts/generate_weekly_summary.py --week "20.10 - 27.10"

# Specific department
python scripts/generate_weekly_summary.py --dept "svaštara"

# Combine filters
python scripts/generate_weekly_summary.py --week "20.10 - 27.10" --dept "finansije"
```

**Arguments:**
- `--week "DD.MM - DD.MM"` - Specific week to process
- `--dept DEPARTMENT` - Specific department to process

**What it does:**
1. Finds all weekly folders matching criteria
2. Locates daily summary.md files in each week
3. Parses activities from daily summaries (supports multiple formats)
4. Aggregates by person across entire week
5. Detects completed tasks via checkboxes/keywords
6. Generates next week plan based on patterns
7. Writes `sedmicni-summary.md` in weekly folder root

**Completed task detection:**
- Checkboxes: `[x]`, `[X]`
- Keywords: "završeno", "done", "completed", "gotovo", "urađeno"

**Next week plan generation:**
- Includes incomplete tasks
- Pattern analysis: sastanak, dokument, nabavka, servis, prodaja
- Suggests continuations

## Important Notes

- **Per-folder summaries:** Each weekly folder gets its own `sedmicni-summary.md`
- **Automatic aggregation:** Script handles all aggregation logic
- **Format support:** Podržava tri formata:
  - Person-based sa "**Aktivnosti:**" sekcijama
  - Person-based legacy sa "### Što je uradio:" sekcijama
  - Topic-based (Finansije, Servis) - ekstraktuje sve bullet points
- **Auto-detection:** Script automatski detektuje koji format je u pitanju
- **Task detection:** Uses multiple indicators to identify completed work
- **Plan generation:** Analyzes patterns to suggest next steps
- **Date format:** Weekly folders use `DD.MM - DD.MM` format
- **Daily folders:** Daily summaries in `DD.MM/summary.md` format

## Best Practices

1. **Run end-of-week** - Generate weekly summaries at end of work week (Friday/Sunday)
2. **Ensure daily summaries exist** - Weekly summary requires daily summaries to aggregate
3. **Review plans** - Generated plans are suggestions based on patterns, review and adjust
4. **Use for planning** - Weekly summaries help plan next week's activities
5. **Archive regularly** - Keep weekly summaries for historical reference
6. **Check all departments** - Use without filters to process all departments at once

## Example Workflow

**User:** "Generiši sedmični summary za 20.10 - 27.10"

**Claude:**
1. Runs: `python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py --week "20.10 - 27.10"`
2. Script output pokazuje:
   ```
   ============================================================
   SEDMIČNI SUMMARY GENERATOR
   ============================================================

   Prona��eno 6 sedmičnih foldera za procesiranje

   📊 Generiše se sedmični summary za administracija/20.10 - 27.10
      Pronađeno 1 dnevnih summary-a
   ✅ Kreiran: gastrohem whatsapp/administracija/20.10 - 27.10/sedmicni-summary.md

   📊 Generiše se sedmični summary za svaštara/20.10 - 27.10
      Pronađeno 2 dnevnih summary-a
   ✅ Kreiran: gastrohem whatsapp/svaštara/20.10 - 27.10/sedmicni-summary.md

   📊 Generiše se sedmični summary za finansije/20.10 - 27.10
      Pronađeno 2 dnevnih summary-a
   ✅ Kreiran: gastrohem whatsapp/finansije/20.10 - 27.10/sedmicni-summary.md

   ============================================================
   ✅ Uspješno generirano: 3/6
   ============================================================
   ```

3. Reports: "✅ Sedmični summaries generirani za 20.10-27.10: 3 odjela (administracija, svaštara, finansije)"

---

**User:** "Make weekly summaries for all weeks"

**Claude:**
1. Runs: `python .claude/skills/sedmicni-summary/scripts/generate_weekly_summary.py`
2. Finds all weekly folders across all departments
3. Generates `sedmicni-summary.md` for each week
4. Reports: "✅ Generirano 12 sedmičnih summaries ukupno"
