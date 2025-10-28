# CLAUDE.md

Ovaj fajl pruža uputstva za Claude Code (claude.ai/code) prilikom rada u ovom repozitoriju.

## Svrha Repozitorija

Ovo je **centralna evidencija za Vozzy App Development**:

- Praćenje WhatsApp komunikacija vezanih za razvoj
- Task management i koordinacija
- Dokumentacija projekta

**Primarni jezik**: Bosanski (BS)

**Feature Specifikacije**: Vidi **[documentation.md](documentation.md)** za kompletan spisak funkcionalnosti po verzijama (v1 / v2)

## Struktura Repozitorija

**vozzy-whatsapp/** - Evidencija WhatsApp komunikacija:
- Organizovano po sedmicama (`DD.MM - DD.MM`)
- Unutar sedmica po danima (`DD.MM/`)
- Svaki dan ima `chat.md` i `summary.md`

**vozzy-tasks/** - Task management:
- Taskovi po osobama
- Praćenje šta je completed

## Dokumentacioni Workflow

### Trenutni Proces

1. WhatsApp poruke se prepisuju u `chat.md`
2. Audio/slike se transkribuju u JSON
3. Kreira se `summary.md` koji izvlači:
   - Šta je ko uradio
   - Šta bi ko trebao da uradi
   - Action items

## Format Summary Fajlova

```markdown
# Summary - [Tema] (DD.MM.YYYY)

## **Ime Prezime**

### Što je uradio:
- Konkretne akcije

### Što bi trebao da uradi:
- Action items
```

## Format Taskova

```markdown
- [ ] **[Kategorija]**: Opis task-a
  - Assigned: Ime
  - Priority: High/Medium/Low
```

## Rad sa Ovim Repozitorijem

- **Jezik**: Bosanski
- **Format datuma**: DD.MM.YYYY
- **Checkboxes**: `- [ ]` za taskove
- **Summary**: Izvlači akcije i dodijeli osobama
