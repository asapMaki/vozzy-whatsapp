# Sazetak razgovora (31.10.2025)

Razgovor se fokusirao na definisanje konačnog roka za Vozzy aplikaciju (**15. decembar - V1**), prioritetne funkcionalnosti, i ključne arhitekturne odluke. **Bojana** je potvrdila rok sa klijentom i predstavila izmjene u dizajnu i zahtjevima (uklonjen screen za izbor vozač/klijent, SMS auth, ugovor preko maila). **Timur** i **Mahir** su se fokusirali na **4 ključne funkcionalnosti za V1**: autentifikacija, request ride, live tracking, i driver status management. **Faris** je predložio pojednostavljeni SMS auth za sve korisnike i vozače bez dodatnih username/password kombinacija. Tim je dogovorio simplifikaciju plaćanja (cash only u V1, Monri kartično later), administraciju vozača (admin full control, vozači kao zaposleni), i GPS tracking svih vozača na admin panelu.

---

## **Bojana**

### Što je uradio:
- Potvrdila konačni rok sa klijentom: **15. decembar za V1**
- Postavila interni cilj: **10. decembar** (5 dana lufta prije roka)
- Predstavila izmjene u dizajnu i zahtjevima od klijenta:
  - Uklonjen screen za izbor vozač/klijent (vozači će imati mali "Ja sam vozač" link u menu-u)
  - Vozači se dodaju isključivo kroz admin panel (neće moći samostalno registracija)
  - Ugovor se šalje na mail korisniku i vozaču nakon potvrde vožnje
  - GPS tracking vozača kroz admin panel (zahtjev od klijenta)
- Razjasnila uslove korištenja: link na webu koji user prihvata prilikom registracije (pravno obavezujuće)
- Dostavila draft dizajna i konfirmovala zahtjeve sa klijentom
- Razjasnila plaćanje: Monri kartično plaćanje će biti naknadno (klijent tek otvara firmu), V1 će biti samo cash
- Konfirmovala terminale: **NEĆE** biti terminala u vozilima, plaćanje isključivo preko Monri mobilne app (later) ili cash (V1)
- Predstavila model rada: svi vozači su zaposleni, admin ima full control (može disable/enable vozače)
- Razjasnila tip vozila: tri tipa će postojati u sistemu, ali V1 koristi samo **Tip 1**
- Pojasnila Apple App Store challenge: klijent mora imati firmu da bi aplicirao (vjerovatno samo Android u V1)

### Što bi trebao da uradi:
- Prenijeti klijentu informaciju o Monri terminalu (postoji Monri uređaj sa Android, GPS čipom, printer-om - može cijelu aplikaciju imati)
- Provjeriti sa klijentom kako su aplicirali na Google Play (kao firma ili fizičko lice?)
- Poslati finalne dizajn screen-ove (menu sa "Ja sam vozač" opcijom) do kraja sedmice
- Koordinirati sa klijentom oko otvaranja firme za Monri nalog
- Konfirmovati sa klijentom da li admin panel treba da prikazuje samo vozače ili i korisnike (pretpostavka: samo vozače)

---

## **Timur**

### Što je uradio:
- Prenio informaciju Bojani da je razgovarao sa njom i Mahirom o roku
- Potvrdio klijentu rok: **15. decembar**
- Dogovorio sa klijentom pojednostavljeni scope za V1 (izbacili neke funkcionalnosti)
- Objavio web stranicu na Globalu (najmanji hosting paket)
- Razjasnio da se admin panelu ne koristi server (sve ide preko Firebase-a)
- Pitao za hosting potrebe i server konfiguraciju (razjašnjeno da ne treba dodatan server)

### Što bi trebao da uradi:
- Poslati ažurirani dizajn screen-ova (uključujući menu sa "Ja sam vozač" opcijom) do kraja sedmice ili u ponedjeljak
- Koordinirati sa Mahirom i Farisom oko šeme podataka
- Testirati web hosting na Firebase-u (opciono, trenutni Globul hosting radi)

---

## **Mahir Kadic**

### Što je uradio:
- Postavio interni cilj: **10. decembar** za completion
- Prihvatio prioritetnu listu funkcionalnosti za V1:
  1. SMS autentifikacija (login/registration)
  2. Request ride (odabir lokacije, destinacije, slanje zahtjeva)
  3. Live tracking (prikaz vozača i usera tokom vožnje)
  4. Driver status management (prihvati, u vožnji, završio)
- Razjasnio potrebu za email fieldom: mandatoran zbog slanja ugovora na mail nakon vožnje
- Predložio login flow: SMS kod za sve (vozači i useri), drugi step za usere je mail + ime (mandatory)
- Pitao za server potrebe (razjašnjeno da Firebase pokriva sve)
- Argumentovao protiv username/password za vozače (kompromitacija, dupli sistem)
- Predložio SMS auth kao unified pristup za sve korisnike

### Što bi trebao da uradi:
- **Prioritet 1:** Fiksati postojeći bug sa SMS autentifikacijom
- **Prioritet 2:** Kreirati šemu podataka za sve kolekcije (drivers, users, rides, vehicles, admins)
- **Prioritet 3:** Implementirati trigger funkciju: kad se vožnja završi, generiše PDF ugovor i šalje na mail (korisniku i vozaču)
- Dodati email field kao mandatory u user registration flow (drugi step nakon SMS-a)
- Implementirati kalkulaciju cijene prije "Request Ride" (API za udaljnost + formula)
- Pripremiti funkcionalnost za računanje udaljenosti između koordinata (Google Maps API)
- Razmotriti mogućnost auto-suggest adresa (Google Maps API autocomplete)
- Implementirati Firebase Cloud Function za alokaciju najbližeg vozača
- Implementirati real-time database update za GPS lokacije (svaki vozač/user updatuje lokaciju svakih 10 sekundi)

---

## **Faris**

### Što je uradio:
- Predložio pojednostavljeni pristup: SMS auth za sve (vozači i useri), bez username/password
- Argumentovao prednosti SMS auth-a: jedan unified login screen, smanjenje broja screen-ova, user-friendly
- Razjasnio Firebase arhitekturu: real-time database za GPS tracking (vozači i useri upisuju lokaciju svakih 10 sekundi)
- Predložio da se izbaci "Registracija/Prijava" izbor, direktno SMS unos - sistem prepoznaje da li je user nov ili postojeći
- Pojasnio da email može biti mandatory u drugom koraku (nakon SMS verifikacije)
- Razjasnio trigger funkciju: kad se vožnja završi, automatski generiše PDF i šalje na mail
- Potvrdio da Google Maps API podržava konverziju koordinata u adrese i autocomplete

### Što bi trebao da uradi:
- **Prioritet 1:** Kreirati šemu podataka za sve Firebase kolekcije (koordinirati sa Mahirom)
- **Prioritet 2:** Implementirati admin panel funkcionalnost:
  - Dodavanje vozača (email, broj telefona, password, tip vozila, broj tablice)
  - Enable/Disable vozača
  - Mapa sa svim vozačima (live GPS tracking)
  - Indikator statusa vozača na mapi (aktivan, u vožnji, neaktivan - različite boje)
- Implementirati Firebase trigger za PDF generisanje nakon završetka vožnje
- Kreirati Firebase funkciju za alokaciju najbližeg vozača (filtrira po statusu i tipu vozila)
- Postaviti real-time database tracking za GPS (vozači i useri)
- Koordinirati sa Mahirom oko API poziva za računanje udaljenosti i cijene

---

## **Mirza Gojak**

### Što je uradio:
- Razgovarao sa Mahirom i Farisom oko detalja implementacije (after call)
- Komentarisao na dizajn screen-ove i UX flow
- Predložio izmjene u dizajnu: izbaciti "Traži vožnju" button sa početnog screen-a, zamijeniti sa "Unesi lokaciju"
- Argumentovao za prikaz cijene prije Request Ride button-a (user mora vidjeti cijenu prije nego što potvrdi)
- Identifikovao konfuziju u dizajnu: "Traži vožnju" dugme se pojavljuje prije nego što su unesene sve informacije

### Što bi trebao da uradi:
- Koordinirati sa Timurom oko korekcija dizajna (ukloniti dupli "Traži vožnju" button, dodati prikaz cijene prije potvrde)
- Nastaviti rad na rute/route funkcionalnosti (spomenuto u razgovoru)
- Diskutovati sa timom oko UX flow-a: adresa vs koordinate (pinovi na mapi)

---

## **Ključne odluke:**

- **Rok:** 15. decembar za V1 (interni cilj: 10. decembar)
- **Prioritet funkcionalnosti za V1:**
  1. SMS autentifikacija
  2. Request ride (biranje lokacije, destinacije, prikaz cijene, slanje zahtjeva)
  3. Live tracking (prikaz vozača tokom vožnje na mapi)
  4. Driver status management (admin može enable/disable, vozač automatski prelazi kroz statuse)
- **Arhitektura:**
  - Firebase za sve (backend, autentifikacija, baza, real-time database)
  - Hosting: trenutni Globul OK, može Firebase Hosting za web (optional)
- **SMS Auth za SVE:** Unified login screen, broj telefona je primary ID
  - Useri: SMS → ime, prezime, email (mandatory)
  - Vozači: SMS → admin prethodno unio sve podatke
- **Ugovor:** PDF generisan nakon vožnje, šalje se na mail korisniku i vozaču (Firebase trigger funkcija)
- **Plaćanje u V1:** SAMO cash (Monri kartično kasnije kad klijent otvori firmu)
- **Terminali:** NE (možda Monri Android uređaj kasnije)
- **Vozači:** Admin ima full control, vozači su zaposleni, admin dodaje vozače kroz admin panel
- **GPS Tracking:** Real-time database (vozači updatuju lokaciju svakih 10 sekundi), admin vidi sve vozače na mapi
- **Tipovi vozila:** Sistem podržava 3 tipa, V1 koristi samo Tip 1
- **Dizajn izmjene:**
  - Uklonjen screen za izbor vozač/klijent
  - "Ja sam vozač" link u menu-u (mali tekst)
  - Prikaz cijene prije "Zatraži vožnju" button-a
  - Uslovi korištenja: link na webu (user prihvata prilikom registracije)
- **Apple App Store:** Vjerovatno nećemo biti dostupni na iOS u V1 (klijent mora imati firmu)
- **Šema podataka:** Faris i Mahir kreiraju kompletan spisak kolekcija sa poljima
- **Algoritam alokacije:** Najbliži dostupan vozač (po koordinatama) sa odgovarajućim tipom vozila

---

## **Action items - HITNO:**

1. **Mahir:** Fiksati SMS auth bug
2. **Faris i Mahir:** Kreirati šemu podataka (sve kolekcije)
3. **Faris:** Admin panel - dodavanje vozača i vozila
4. **Mahir:** Trigger funkcija za PDF ugovor + email
5. **Timur:** Poslati finalne dizajn screen-ove
6. **Bojana:** Konfirmovati sa klijentom oko Google Play aplikacije (firma vs fizičko lice)
