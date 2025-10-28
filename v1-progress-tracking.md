# Vozzy v1 - Progress Tracking & Analiza

**Posljednji update**: 28.10.2025
**Izvor podataka**:
- `documentation.md` - v1 specifikacija
- `vozzy whatsapp/28-10-2025/summary.md` - trenutni rad
- `vozzy taskovi/` - ekstraktovani taskovi po osobama

---

## Executive Summary

**Status**: 🟡 **Rana Faza Razvoja** - Fokus na fundamentalnoj infrastrukturi (Auth & Backend)

**Trenutni Fokus**: SMS Authentication & Firebase Backend Setup
**Procjena Završenosti v1**: **~5-10%** (2-3 od ~50+ funkcionalnosti u toku)

**Glavni Blokeri**:
- Auth bug mora biti riješen prije daljih integracija (HIGH priority)
- Backend dokumentacija potrebna za frontend tim
- Većina core funkcionalnosti još nije započeta

---

## 1. Trenutni Rad vs v1 Specifikacija

### ✅ **U TOKU** - Trenutno se radi na ovome

| Funkcionalnost | v1 Requirement | Trenutni Status | Tim | Napomena |
|---------------|----------------|-----------------|-----|----------|
| **Registracija i profil** | v1 - Putnici | 🟡 U TOKU | Faris, Mahir | SMS auth flow, Firebase setup |
| **Admin panel za vozače** | v1 - Admin | 🟡 U TOKU | Mahir | Dodavanje vozača preko admin panela |
| **Pronalazak vozača** | v1 - Tehničko | 🟡 U TOKU | Mirza | Driver search feature |
| **Firebase backend** | v1 - Tehničko | 🟡 U TOKU | Faris | Auth funkcije, Cloud Functions |

### 🔴 **NIJE ZAPOČETO** - v1 funkcionalnosti koje NISU u taskovima

#### Putnici - Osnovne Mogućnosti (v1)
- [ ] Unos lokacije polaska i odredišta (Google Maps)
- [ ] Praćenje vozača na mapi
- [ ] Procjena cijene vožnje unaprijed
- [ ] Potvda/prihvatanje cijene
- [ ] Plaćanje gotovinon - potvrda dolaska vozila
- [ ] Različiti tipovi vozila (obični, veliki, luksuzni)
- [ ] Pozivanje vozača jednim dodirom
- [ ] Pozivanje vozača direktno (Viber, WhatsApp poziv)
- [ ] Direktna komunikacija sa vozačem (poziv/poruka)
- [ ] Praćenje lokacije vozača uživo (od prihvatanja do preuzimanja)

#### Putnici - Napredne Mogućnosti (v1)
- [ ] Čuvanje omiljenih adresa (kuća, posao)
- [ ] Historija svih vožnji
- [ ] Ocjenjivanje vozača nakon vožnje
- [ ] Prijavljivanje problema i žalbi
- [ ] Obavještenja o statusu vožnje (notifikacija: vozač dolazi)

#### Vozači - Osnovne Mogućnosti (v1)
- [ ] Uključivanje/isključivanje dostupnosti
- [ ] Primanje zahtjeva za vožnje
- [ ] Prihvatanje ili odbijanje zahtjeva (evidencija)
- [ ] GPS navigacija do putnika i odredišta
- [ ] Označavanje početka i kraja vožnje
- [ ] Direktna komunikacija sa putnikom (poziv/poruka)
- [ ] Chat (1.5 - basic chat)

#### Vozači - Napredne Mogućnosti (v1)
- [ ] Pregled zarada (dnevno, sedmično, mjesečno)
- [ ] Praćenje radnih sati i broja vožnji
- [ ] Ocjenjivanje putnika

#### Admin Panel (v1)
- [ ] Kontrolna tabla za praćenje aktivnih vožnji
- [ ] Upravljanje putnicima (dodavanje, brisanje, blokiranje sa razlogom)
- [ ] Upravljanje cijenama (povećanje u gužvi - algoritam TBD)

#### Tehnička Infrastruktura (v1)
- [ ] Algoritam za povezivanje vozač–putnik
- [ ] Sistem plaćanja (gotovina)
- [ ] Push obavještenja (vozač dodijeljen, vozač na putu)
- [ ] Navigacija i Google Maps integracija
- [ ] Sistem ocjenjivanja i povratnih informacija

---

## 2. Detaljni Pregled Trenutnih Taskova

### **Faris** (Backend Developer) - 5 taskova

#### 🔴 HIGH Priority
1. **Fiksati auth bug** (#backend #auth)
   - **Pokriva**: Dio "Registracija i profil" (v1)
   - **Blocker**: DA - blokira frontend integraciju
   - **Napomena**: Kritično za nastavak

2. **Dodati UID mapping za SMS auth** (#backend #auth)
   - **Pokriva**: Dio "Registracija i profil" (v1)
   - **Blocker**: DA - potrebno za user management

3. **Organizovati sastanak sa Bojanom** (#operativno)
   - **Pokriva**: Koordinacija i prezentacija napretka
   - **Rok**: Sljedeća sedmica

#### 🟡 MEDIUM Priority
4. **Kreirati Firebase funkcije za kompleksniju logiku** (#backend)
   - **Pokriva**: Dio "Algoritam za povezivanje vozač–putnik" (v1)
   - **Detalji**: Kalkulacije, routing vozača

5. **Pripremiti dokumentaciju za frontend tim** (#backend)
   - **Pokriva**: Tehničko - dokumentacija
   - **Blocker za frontend**: DA

---

### **Mahir Kadic** (Frontend Developer) - 5 taskova

#### 🔴 HIGH Priority
1. **Istražiti Firebase SMS auth format** (#frontend #auth #research)
   - **Pokriva**: Dio "Registracija i profil" (v1)
   - **Napomena**: Potrebno za UID mapping

2. **Integrisati Login/Registration flow sa Firebase** (#frontend #auth)
   - **Pokriva**: "Registracija i profil" (v1)
   - **Dependency**: Nakon Faris auth bug fix
   - **Blocker**: DA - kritično za sve ostalo

3. **Implementirati dodavanje dodatnih podataka usera** (#frontend #auth)
   - **Pokriva**: "Registracija i profil - ime, prezime, adresa, telefon" (v1)

4. **Kompletirati auth flow** (#frontend #auth)
   - **Pokriva**: Dio "Registracija i profil" (v1)
   - **Napomena**: Sve auth komponente moraju biti završene

#### 🟡 MEDIUM Priority
5. **Slati broj telefona i UID u Firebase funkcije** (#frontend #backend)
   - **Pokriva**: Backend integracija
   - **Koordinacija**: Sa Farisom

---

### **Mirza Gojak** (Developer) - 2 taska

#### 🟡 MEDIUM Priority
1. **Nastaviti rad na "pronalazak vozača" feature** (#frontend)
   - **Pokriva**: Dio "Algoritam za povezivanje vozač–putnik" (v1)
   - **Napomena**: Vjerojatno frontend za prikaz vozača

2. **Koordinirati sa Farisom i Mahirom nakon auth flow-a** (#operativno)
   - **Dependency**: Nakon završetka auth flow-a
   - **Napomena**: Integracija sa auth sistemom

---

### **Harun** (Developer) - 0 taskova
- **Status**: Trenutno nema dodijeljenih taskova
- **Preporuka**: Može početi sa nekom od funkcionalnosti koje nisu započete (Google Maps integracija, UI komponente, itd.)

---

## 3. Gap Analiza - Šta Fali?

### 🔴 **KRITIČNE v1 Funkcionalnosti koje NISU u planu:**

#### 1. **Google Maps Integracija**
- Unos lokacije polaska/odredišta
- Praćenje vozača na mapi
- GPS navigacija
- **Napomena**: Ovo je CORE funkcionalnost - bez ovoga nema ride-hailing app-a!

#### 2. **Matching Algoritam (Vozač-Putnik)**
- Algoritam za pronalazak najbližeg dostupnog vozača
- Automatsko dodjeljivanje vožnji
- **Napomena**: Mirza radi na "pronalazak vozača" ali nije jasno da li je ovo full matching algoritam

#### 3. **Sistem Plaćanja**
- Procjena cijene unaprijed
- Potvrda cijene
- Gotovina kao metoda plaćanja
- Evidencija transakcija

#### 4. **Real-time Communication**
- Push notifikacije (vozač dolazi, vožnja počela, itd.)
- WebSocket / Firebase Realtime Database za live tracking
- In-app pozivi/chat

#### 5. **Ride Management**
- Kreiranje vožnje
- Prihvatanje/odbijanje od strane vozača
- Označavanje početka/kraja vožnje
- Status tracking (pending, accepted, in-progress, completed)

#### 6. **Driver Management**
- Uključivanje/isključivanje dostupnosti
- Primanje zahtjeva
- Navigacija
- Pregled zarada

#### 7. **Rating System**
- Ocjenjivanje vozača
- Ocjenjivanje putnika
- Evidencija rejting-a

#### 8. **Admin Dashboard**
- Kontrolna tabla za aktivne vožnje
- Upravljanje korisnicima
- Upravljanje cijenama

---

## 4. Preporuke - Sljedeći Koraci

### **IMMEDIATE (1-2 sedmice)**

1. ✅ **Završiti Authentication Flow** (U TOKU)
   - Faris: Fiksati bug, dodati UID mapping
   - Mahir: Integrisati Firebase SDK, kompletirati login/registration
   - **Rok**: Prije sastanka sa Bojanom

2. 🆕 **Google Maps Integration** (KRITIČNO - NIJE ZAPOČETO!)
   - Google Maps API setup
   - Location picker component
   - Basic map display
   - **Assigned to**: Harun ili Mahir (nakon auth-a)
   - **Dependency**: Ključno za dalje testiranje

3. 🆕 **Ride Request Flow - Backend** (KRITIČNO)
   - Firebase schema za rides collection
   - Cloud Function za kreiranje ride request-a
   - **Assigned to**: Faris
   - **Dependency**: Nakon auth sistema

### **SHORT TERM (3-4 sedmice)**

4. 🆕 **Matching Algorithm - Backend**
   - Algoritam za pronalazak najbližeg vozača
   - GeoFire / Geohashing za location queries
   - **Assigned to**: Faris (backend logic)
   - **Note**: Koordinirati sa Mirzom (frontend)

5. 🆕 **Ride Request Flow - Frontend**
   - UI za unos polaska/odredišta
   - Prikaz dostupnih vozača
   - Request ride button
   - **Assigned to**: Mahir ili Mirza
   - **Dependency**: Google Maps + Backend ride API

6. 🆕 **Driver App - Prihvatanje Vožnji**
   - UI za primanje ride requests
   - Prihvatanje/odbijanje
   - Navigacija do putnika
   - **Assigned to**: Mirza
   - **Dependency**: Ride request flow

7. 🆕 **Push Notifications**
   - Firebase Cloud Messaging setup
   - Notifikacije za ride statuse
   - **Assigned to**: Faris (backend), Mahir (frontend)

### **MEDIUM TERM (1-2 mjeseca)**

8. 🆕 **Price Calculation System**
   - Algoritam za procjenu cijene
   - Distance + time based pricing
   - Različiti tipovi vozila
   - **Assigned to**: Faris

9. 🆕 **Payment System (Gotovina)**
   - Evidencija cash plaćanja
   - Potvrde o plaćanju
   - **Assigned to**: Faris

10. 🆕 **Rating System**
    - UI za ocjenjivanje
    - Backend za čuvanje rejting-a
    - **Assigned to**: Tim (backend + frontend)

11. 🆕 **Admin Dashboard - MVP**
    - Lista aktivnih vožnji
    - Basic user management
    - **Assigned to**: Novi developer ili Harun

---

## 5. Rizici i Prepreke

### 🔴 **HIGH RISK**

1. **Google Maps Integracija nije započeta**
   - **Impact**: Bez ovoga nema core funkcionalnosti
   - **Mitigation**: Prioritizovati odmah nakon auth-a

2. **Nema jasnog plana za matching algoritam**
   - **Impact**: Ne mogu se testirati end-to-end vožnje
   - **Mitigation**: Faris mora definisati arhitekturu

3. **Push notifikacije nisu planirane**
   - **Impact**: Loše user experience bez real-time updates
   - **Mitigation**: Dodati u immediate backlog

4. **Harun nema taskova**
   - **Impact**: 25% tima nije iskorišteno
   - **Mitigation**: Dodijeliti Google Maps ili UI taskove

### 🟡 **MEDIUM RISK**

5. **Mirza radi na "pronalazak vozača" ali nije jasno šta to pokriva**
   - **Mitigation**: Razjasniti da li je to matching algoritam ili samo UI

6. **Admin panel je samo parcijalno planiran**
   - **Impact**: Ne može se testirati end-to-end bez admin funkcionalnosti
   - **Mitigation**: Definisati MVP admin dashboard

---

## 6. Timeline Projekcija za v1

**Trenutni Tempo**: ~5-10% završeno
**Pretpostavka**: 3-4 developera full-time

### Optimistična Projekcija (6-8 sedmica)
- **Sedmica 1-2**: Auth completion + Google Maps
- **Sedmica 3-4**: Ride request flow + Matching
- **Sedmica 5-6**: Driver app + Notifications
- **Sedmica 7-8**: Payments + Rating + Testing

### Realistična Projekcija (10-12 sedmica)
- **Sedmica 1-3**: Auth + Google Maps + Backend architecture
- **Sedmica 4-6**: Ride management flow (passenger side)
- **Sedmica 7-9**: Driver app + Matching algorithm
- **Sedmica 10-12**: Payments + Rating + Admin + Testing

### Pesimistična Projekcija (16-20 sedmica)
- Dodatno vrijeme za:
  - Learning curve (Firebase, Google Maps APIs)
  - Bug fixing i refactoring
  - Testing i QA
  - Nepredviđeni blokeri

---

## 7. Akcioni Plan - Immediately After Auth

**Prioritet 1: Core Ride Flow**
```
Auth System (u toku)
  └─> Google Maps Integration
      └─> Create Ride Request (Backend)
          └─> Create Ride Request (Frontend UI)
              └─> Matching Algorithm
                  └─> Driver Accept/Reject
                      └─> Navigation & Tracking
                          └─> Complete Ride
                              └─> Rating
```

**Prioritet 2: Supporting Features**
- Push Notifications (paralelno sa Ride Flow)
- Price Calculation (nakon matching-a)
- Payment System (nakon complete ride)
- Admin Dashboard (nakon što ima nešto za manage-ati)

**Prioritet 3: Nice-to-Have (v1.5 ili v2)**
- Advanced features iz documentation.md
- Offline mode
- Chat system

---

## 8. Preporuke za Bojana Sastanak

**Šta Pokazati:**
- ✅ SMS Authentication flow (ako bude završen)
- ✅ Firebase backend setup
- ✅ Admin panel za dodavanje vozača (ako bude gotovo)

**Šta Diskutovati:**
- 🔴 Neophodnost Google Maps integracije odmah nakon auth-a
- 🔴 Timeline za v1 - realna projekcija 10-12 sedmica
- 🔴 Potreba za jasnom arhitekturom matching algoritma
- 🟡 Resursi - Harun trenutno nema taskove
- 🟡 Definicija "MVP" - možda smanjiti v1 scope?

**Red Flags za Bojana:**
- Mnogo v1 funkcionalnosti nije ni započeto
- Nema plana za core features (maps, matching, payments)
- Fokus samo na auth može biti pre-mature optimization

---

## 9. Conclusion

**Trenutni Status**: Tim je na dobrom putu sa fundamentalnom infrastrukturom (Auth & Backend), ali **mnogo core funkcionalnosti još nije planirano**.

**Key Takeaway**: Nakon završetka auth sistema (1-2 sedmice), tim mora **HITNO** prioritizovati:
1. Google Maps integracija
2. Ride request flow (backend + frontend)
3. Matching algoritam

Bez ovih 3 stvari, nema funkcionalne ride-hailing aplikacije. Auth je važan, ali nije dovoljan.

**Preporuka**: Kreirati **backlog taskova** za sve v1 funkcionalnosti i početi paralelno raditi na Google Maps integration čim se auth završi.

---

**Sljedeći Review**: Nakon sastanka sa Bojanom
**Update Frequency**: Sedmično (nakon sedmičnog sync-a srijedom)
