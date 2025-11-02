# Sazetak razgovora (01.11.2025)

Tehnički follow-up sastanak između **Mahira** i **Farisa** nakon glavnog sastanka sa 31.10. Razgovor se fokusirao na tehničke detalje implementacije: šemu podataka za Firebase kolekcije, admin panel funkcionalnosti, i UX flow za request ride. **Faris** je predložio da se admin kolekcija kreira odvojeno sa dodatnim permisijama, i da admin ima mapu sa svim vozačima i management opcijama (enable/disable). **Mahir** je razjasnio prioritete: prvo šema podataka, zatim admin panel za dodavanje vozača, trigger funkcija za PDF ugovor, i kalkulacija cijene. Tim je identifikovao UX problem u dizajnu: user mora vidjeti cijenu PRIJE nego što klikne "Traži vožnju", ne nakon. Dogovoreno je da se koristi Google Maps API za autocomplete adresa i konverziju koordinata, i da se real-time database koristi za GPS tracking (update svakih 10 sekundi).

---

## **Mahir Kadic**

### Što je uradio:
- Razjasnio prioritete za backend development:
  1. **Šema podataka** - kompletna šema svih Firebase kolekcija (drivers, users, rides, admins, vehicles)
  2. **Admin panel** - dodavanje vozača i vozila, enable/disable funkcionalnost
  3. **Trigger funkcija** - generisanje PDF ugovora nakon završetka vožnje i slanje na mail
  4. **Kalkulacija cijene** - API za računanje udaljenosti iz koordinata i primjena formula za cijenu
- Postavio pitanje o načinu unosa lokacije: adresa ili pin na mapi?
- Razjasnio da će backend slati koordinate (lakše za rad), frontend može prikazivati kako god želi
- Potvrdio da Google Maps API podržava konverziju adresa u koordinate i autocomplete
- Identifikovao UX problem u dizajnu: user mora vidjeti cijenu PRIJE klika na "Traži vožnju"
- Predložio izmjenu UX flow-a:
  - User unese polazak i dolazak
  - Sistem odmah prikazuje cijenu
  - User tek onda može kliknuti "Traži vožnju"
- Naglasio prioritet: **najbliži vozač** algoritam (ne svi vozači primat zahtjev)

### Što bi trebao da uradi:
- **Prioritet 1:** Kreirati kompletnu šemu podataka za sve Firebase kolekcije i poslati Farisu
- **Prioritet 2:** Fiksati postojeći bug sa SMS auth sistemom
- **Prioritet 3:** Implementirati trigger funkciju za PDF ugovor (generiše i šalje na mail nakon završetka vožnje)
- **Prioritet 4:** Implementirati API za računanje cijene vožnje (Google Maps Distance Matrix API + formula)
- Implementirati Google Maps API autocomplete za unos adresa
- Implementirati konverziju adresa u koordinate (potrebno za backend kalkulacije)
- Razjasniti sa Timurom UX izmjene: prikaz cijene prije "Traži vožnju" button-a
- Implementirati "najbliži vozač" algoritam (filtriranje po statusu i tipu vozila, sortiranje po udaljenosti)

---

## **Faris**

### Što je uradio:
- Predložio da se **admin kolekcija kreira odvojeno** (ne kao user sa rolom, već posebna kolekcija)
- Razjasnio admin funkcionalnosti:
  - Admin se loguje preko SMS-a sa testnim brojem telefona (Firebase test phone numbers)
  - Admin ne može vidjeti root routes, samo svoj admin panel
  - Admin vidi mapu sa svim vozačima (GPS tracking)
  - Admin ima dugme za management vozača: enable/disable/block (za V1 samo enable/disable)
- Potvrdio da će vozilo biti vezano za vozača (drivers kolekcija ima vozilo field)
- Predložio da se tip vozila čuva u sklopu vozača (ne posebna tabela)
  - Tip vozila: Standard, Premium, Eco (ili slični nazivi)
  - Filtriranje vozača po tipu vozila će biti lako
- Razjasnio model: vozač = vozilo (jedan vozač ima jedno vozilo, ako se mijenja vozilo, admin updatuje kroz admin panel)
- Potvrdio real-time database pristup za GPS tracking: svaki uređaj upisuje lokaciju svakih 10 sekundi
- Razjasnio da ne treba socket implementacija (Firebase real-time database rješava to)
- Potvrdio da će email trigger funkcija biti jednostavna (Firebase Cloud Function kreira PDF i šalje mail)
- Predložio da admin panel bude vizualno privlačan (mapa sa vozačima) da klijent može testirati

### Što bi trebao da uradi:
- **Prioritet 1:** Kreirati kompletnu šemu podataka za Firebase kolekcije:
  - `admins` - admin korisnici (SMS login, permisije)
  - `drivers` - vozači (broj telefona, vozilo, tip vozila, tablica, status)
  - `users` - korisnici (broj telefona, ime, prezime, email)
  - `rides` - vožnje (user, driver, polazak, dolazak, cijena, status, vrijeme)
  - Eventualno dodatne kolekcije (tarife, ugovori, itd.)
- **Prioritet 2:** Implementirati admin panel funkcionalnosti:
  - Dodavanje vozača (broj telefona, vozilo, tip vozila, tablica)
  - Dodavanje vozila (tip, tablica, vezati za vozača)
  - Enable/Disable vozača
  - Mapa sa svim vozačima (live GPS tracking)
  - Vizualni indikatori statusa vozača na mapi (aktivan, u vožnji, neaktivan - različite boje)
- **Prioritet 3:** Implementirati real-time database za GPS tracking
  - Vozači i useri upisuju lokaciju svakih 10 sekundi
  - Admin panel čita lokacije iz real-time database i prikazuje na mapi
- Koordinirati sa Mahirom oko šeme podataka (sinhronizovati field names: surname vs last_name, itd.)
- Implementirati Firebase Cloud Function trigger za PDF generisanje i email

---

## **Mirza Gojak**

### Što je uradio:
- Identifikovao kritični UX problem u dizajnu: user ne može vidjeti cijenu PRIJE nego što klikne "Traži vožnju"
- Predložio izmjenu UX flow-a:
  - **Screen 1:** "Pozdrav, [ime]" → Dugme: "Unesi lokaciju" (NE "Traži vožnju")
  - **Screen 2:** Bottom sheet sa input poljima: Polazak + Dolazak
  - **Screen 3:** Nakon popunjavanja → Prikaz cijene + Dugme "Bira tip vozila"
  - **Screen 4:** Odabir tipa vozila → Finalno "Traži vožnju"
- Argumentovao zašto je ovo problem: user ne može donijeti informisanu odluku bez cijene
- Predložio alternativni flow: umjesto "Traži vožnju" na početnom screen-u → "Unesi lokaciju"
- Razjasnio dizajn konfuziju: trenutni dizajn ima dupli "Traži vožnju" button (jedan prije unosa lokacije, jedan nakon)

### Što bi trebao da uradi:
- Ažurirati UX flow dizajn prema dogovorenim izmjenama:
  - Izbaciti "Traži vožnju" button sa početnog screen-a
  - Dodati "Unesi lokaciju" button
  - Dodati prikaz cijene nakon unosa polazka i dolazka (PRIJE "Traži vožnju")
  - Dodati step za biranje tipa vozila (sa cijenama)
- Komunicirati sa Timurom oko finalizacije dizajna
- Razjasniti sa klijentom da li prikazivanje svih vozača na mapi (user vidi sve dostupne vozače) ili samo najbližeg

---

## **Ključne odluke:**

- **Admin kolekcija:** Odvojena kolekcija (ne user sa rolom), SMS login sa testnim brojem
- **Admin funkcionalnosti:**
  - Dodavanje vozača i vozila
  - Enable/Disable vozača
  - Mapa sa live GPS tracking svih vozača (indikatori statusa: aktivan, u vožnji, neaktivan)
- **Vozilo model:** Vozilo je property vozača (drivers kolekcija), ne posebna tabela
  - Tip vozila: Standard/Premium/Eco (stored u driver fieldu)
  - Jedan vozač = jedno vozilo (promjena vozila se radi kroz admin panel)
- **GPS Tracking:** Real-time database, update svakih 10 sekundi (vozači i useri)
- **Šema podataka:** Prvi prioritet - kompletna šema svih Firebase kolekcija
- **UX Flow izmjene:**
  - Početni screen: "Unesi lokaciju" (NE "Traži vožnju")
  - Prikaz cijene PRIJE "Traži vožnju" button-a
  - Bottom sheet za unos polazka i dolazka
  - Odabir tipa vozila sa prikazom cijene
- **Google Maps API:** Autocomplete za adrese + konverziju adresa u koordinate
- **Backend prioriteti:**
  1. Šema podataka
  2. SMS auth bug fix
  3. Admin panel (dodavanje vozača/vozila, enable/disable)
  4. Trigger funkcija (PDF ugovor + email)
  5. Kalkulacija cijene (Distance Matrix API + formula)
- **Algoritam alokacije:** Najbliži vozač (ne svi vozači primat zahtjev)

---

## **Action items - HITNO:**

1. **Mahir i Faris:** Kreirati kompletnu šemu podataka za sve Firebase kolekcije (sinhronizovati field names)
2. **Mahir:** Fiksati SMS auth bug
3. **Faris:** Admin panel - dodavanje vozača/vozila, enable/disable, mapa sa GPS tracking
4. **Mahir:** Trigger funkcija za PDF ugovor + email nakon završetka vožnje
5. **Mahir:** API za kalkulaciju cijene (Google Maps Distance Matrix + formula)
6. **Mirza:** Ažurirati UX flow dizajn (prikaz cijene prije "Traži vožnju")
7. **Tim:** Razjasniti sa Timurom i klijentom da li user vidi sve vozače ili samo najbližeg
