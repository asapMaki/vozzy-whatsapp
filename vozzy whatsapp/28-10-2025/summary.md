# Sazetak razgovora (25.10 - 27.10.2025)

Razgovor se vrti oko rješavanja auth problema i planiranja sljedećih koraka za Vozzy app. **Faris** je riješio problem sa Firebase Auth servisom i predložio SMS auth flow za sve korisnike. **Mahir** je definisao sljedeće korake: povezivanje login/registration sa Firebase i admin panel za unos vozača. Dogovoreno je da se održi sedmični sync sastanak srijedom u 18:00 i da se organizuje sastanak sa Bojanom sljedeće sedmice.

---

## **Faris**

### Što je uradio:
- Riješio problem sa Firebase Auth servisom - dropdown je pokazivao "Deleted", izabrao pravu funkciju na "before sign-in" triggeru
- Omogućio unos user podataka (ime, prezime, mail) u Firestore dokument "users"
- Utvrdio da opcija driver/user nije potrebna na onboarding screen-u (vozači bi trebali biti dodavani kroz admin panel)
- Kreirao blocking funkciju koja se automatski "kači" na Auth servis i osluškuje registracije
- Predložio SMS auth preko broja telefona kao primarni način autentifikacije (siguran, besplatan, user-friendly)
- Predložio sedmični sync sastanak srijedom oko 18:00

### Što bi trebao da uradi:
- Fiksati bug sa auth sistemom koji je identificirao
- Organizovati sastanak sa Bojanom sljedeće sedmice da se prikaže napredak
- Dodati UID mapping u bazu podataka za SMS auth (provjeriti da li Firebase automatski mapira preko broja ili treba ručno spasiti)
- Kreirati Firebase funkcije za kompleksniju logiku (kalkulacije, routing vozača)
- Pripremiti dokumentaciju/primjere funkcija za frontend tim

---

## **Mahir Kadic**

### Što je uradio:
- Prihvatio ideju sastanka sa Bojanom i sedmičnog sync-a (srijeda 18:00-18:30)
- Definisao sljedeće korake: povezati Login sa Firebase i omogućiti admin-u da unosi vozače
- Predložio SMS auth flow: admin unosi vozača sa brojem telefona, vozač se prvi put loguje SMS-om i automatski se povezuje Firebase user sa Driver dokumentom u Firestore
- Argumentovao za SMS auth: broj teže lažirati nego mail + operater može pronaći lokaciju u slučaju prevare
- Razjasnio Firebase arhitekturu: za basic stvari se koristi Firestore SDK direktno, za kompleksnije operacije backend kreira funkcije

### Što bi trebao da uradi:
- Istražiti format broja kod Firebase SMS auth-a (kako se sprema u bazi)
- Integrisati Login/Registration flow sa Firebase SDK
- Implementirati funkcionalnost da se nakon SMS logina dodaju dodatni podaci usera preko SDK-a
- Slati broj telefona i UID u Firebase funkcije (backend radi sa tim podacima)
- Kompletirati auth flow prije nego što se krene na sljedeću funkcionalnost

---

## **Harun**

### Što je uradio:
- Pratio rješavanje problema i pitao za detalje o auth bug-u

### Što bi trebao da uradi:
- (Nema specifičnih action items za njega u ovom razgovoru)

---

## **Mirza Gojak**

### Što je uradio:
- Radi na funkcionalnosti za pronalazak vozača (spomenuto)

### Što bi trebao da uradi:
- Nastaviti rad na "pronalazak vozača" feature-u
- Koordinirati sa Farisom i Mahirom nakon što se auth flow kompletira

---

## **Ključne odluke:**

- **SMS Auth za sve korisnike:** Primarni način autentifikacije preko broja telefona (besplatno, sigurno, user-friendly)
- **Admin panel za vozače:** Vozači neće biti dodavani kroz onboarding screen već kroz admin panel
- **Sedmični sync:** Srijeda u 18:00-18:30
- **Sastanak sa Bojanom:** Planiran za sljedeću sedmicu
- **Arhitektura:** Basic operacije preko Firestore SDK, kompleksne preko Firebase Cloud Functions
