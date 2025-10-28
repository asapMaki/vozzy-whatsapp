[25. 10. 2025., 11:58:10] ~ Faris: rijesio sam problem, radi sve fino ‎<This message was edited>

[25. 10. 2025., 11:59:50] ~ Faris: Uglavnom sada mozete u dokument users upisati sve ovo sa drugog screen-a (ime prezime, mail)

[25. 10. 2025., 12:00:25] ~ Faris: Mislim da nam opcija driver/user ne treba, jer bi dodavanej vozaca trebalo kroz neki admin panel a ne kroz ovaj onboarding screen

[25. 10. 2025., 12:01:00] ~ Faris: Javite ako nesto bude trebalo
[25. 10. 2025., 12:14:55] Harun: E super 🙌🏻, kakav je bio problem?

[25. 10. 2025., 12:19:12] ~ Faris: Auth servis je gadjao nepostojecu funkciju iz nekog razloga. U dropdown meniju je stajalo “Deleted” i samo je trebalo izabati ovu moju funkciju na tom before sign-in.

TLDR: Ja sam vjerovatno pokvario i popravio 😀

[27. 10. 2025., 19:19:46] ~ Faris: Momci, kako ide? Dokle smo, koji su nam sljedeci koraci? ‎<This message was edited>

[27. 10. 2025., 19:20:16] ~ Faris: Hocemo ubaciti jedan sastanak sedmicno, da damo update neki?

[27. 10. 2025., 19:20:42] ~ Faris: Volio bih iduce sedmice da se cujemo sa bojanom, pokazemo mu sta imamo i dogovorimo za dalje. Kako vam to zvuci?

[27. 10. 2025., 19:32:15] Mahir Kadic: Ne bi bilo lose da se cujemo sa Bojanom

[27. 10. 2025., 19:32:29] Mahir Kadic: A mi medjusobno, mozemo i ovako a i sastanak neki

[27. 10. 2025., 19:33:07] Mahir Kadic: Mi smo stali na onom sto smo pripremili. Sad bi mogli i krenuti dalje

[27. 10. 2025., 19:34:14] Mahir Kadic: Ciljali bi da uvezemo Login sa firebase, i da admin moze unijeti vozace

[27. 10. 2025., 19:34:21] Mahir Kadic: pa da se mogu prijavljivati

[27. 10. 2025., 19:34:46] ~ Faris: kako cemo aditi auth vozaca?

[27. 10. 2025., 19:36:18] Mahir Kadic: meni jos nije jasno kako firebase bekend funkcionise, nema endpointa nego mi koristimo firbase sdk ?

[27. 10. 2025., 19:36:57] ~ Faris: Nece vama biti puno razlike, dobit cete endpoint koji gadjate, samo mi pravimo te tkz funkcije koje obavljaju odredjene zadatke

[27. 10. 2025., 19:37:04] Mahir Kadic: moze i on na broj da ide, samo kad se vozac prvi put uloguje da se poveze tamo Firebasov user i Vozac ?

[27. 10. 2025., 19:37:38] Mahir Kadic: admin unese vozaca sa brojem, a vozac se sa SMS loginom prvi put prijavi i ne mora unositi svoje podatke

[27. 10. 2025., 19:38:25] ~ Faris: mislim da bi moglo tako

[27. 10. 2025., 19:40:40] Mahir Kadic: samo bi trebali istraziti format broja, kako se sprema kod sms auth-a i da tako mi spremamo u firebase

[27. 10. 2025., 19:41:00] Mahir Kadic: znate li vi kako se spremi ?

[27. 10. 2025., 19:41:05] ~ Faris: sekunda

[27. 10. 2025., 19:42:02] ~ Faris: ovo je kako sad spasavamo nakon sms auth

[27. 10. 2025., 19:42:14] ~ Faris: sad vi ovdje kroz sdk trebate dodati ostale podatke

[27. 10. 2025., 19:42:55] Mahir Kadic: a ima i ona tabela sms auth usera

[27. 10. 2025., 19:42:56] Mahir Kadic: sec

[27. 10. 2025., 19:43:12] ~ Faris: da, evo sta tu ima

[27. 10. 2025., 19:43:58] Mahir Kadic: super

[27. 10. 2025., 19:44:15] ~ Faris: Ja mislim da ti mozes nakon logina doci do UID usera trenutnog i preko toga upisati u bazu

[27. 10. 2025., 19:44:52] Mahir Kadic: hocete li spremati UID ?

[27. 10. 2025., 19:45:11] Mahir Kadic: bude u responseu od firebase sdka

[27. 10. 2025., 19:45:50] ~ Faris: e provjerim da li to mapira sam firebase preko broja telefona ili moramo spasiti

[27. 10. 2025., 19:45:57] ~ Faris: mislim da trebamo dodati

[27. 10. 2025., 19:46:34] ~ Faris: Mirza je na pronalasku vozaca ja mislim. @⁨~Mirza Gojak⁩ kako to ide?

[27. 10. 2025., 19:48:47] Mahir Kadic: Pocet cemo sa brojem, pa ako bude potrebe mozemo mi slati i UID, msm slat cemo ga svakako, a vi radite u funkciji sta hocete 😀

[27. 10. 2025., 19:49:41] Mahir Kadic: hajmo mi login/registration flow povezati, a s Mirzom mozemo poslije aBd

[27. 10. 2025., 19:50:13] Mahir Kadic: imas li primjer funkcije za ovo slanje podataka od usera i od vozaca

[27. 10. 2025., 19:53:26] ~ Faris: Bolje je ja mislim da tu ide

[27. 10. 2025., 19:54:15] ~ Faris: ova funkcija koju sam pisao je blocking funkcija koja ide direktno na auth servis, ne mozete joj vi pristupiti

[27. 10. 2025., 19:54:23] ~ Faris: i okida se automatski

[27. 10. 2025., 19:54:45] ~ Faris: Sta je sljedece sto vama treba sa be

[27. 10. 2025., 19:54:55] ~ Faris: malo sam umoran nemoj zamjeriti, slab fokus 😀

[27. 10. 2025., 19:58:58] Mahir Kadic: razumijemo se 😀 ponedeljak uzme svoje

[27. 10. 2025., 19:59:09] Mahir Kadic: pa ne znam iskreno sta bi nam sljedece trebalo

[27. 10. 2025., 19:59:41] ~ Faris: sta mislite da probamo sa flow za odabir rute i pronalazak vozaca?

[27. 10. 2025., 19:59:55] Mahir Kadic: uglavnom prvi cilj neka bude jednostavan, vi ste mozda i rjesili s ovim login i registraciju?

[27. 10. 2025., 20:00:25] ~ Faris: Ja bih predlzi da ostavimo sve preko boja telefona da ide

[27. 10. 2025., 20:00:33] Mahir Kadic: slazem se

[27. 10. 2025., 20:00:34] ~ Faris: prvi put kad uneses odradis registraciju, svaki iduci radis login

[27. 10. 2025., 20:00:44] ~ Faris: to nije skupo, imamo fore bas dosta besplatnih auth mjesecno

[27. 10. 2025., 20:00:52] ~ Faris: najlakse i najsigurnije po meni

[27. 10. 2025., 20:01:01] Mahir Kadic: mail se moze lažirati, a broj malo teže plus operater moze pronaci lokaciju u slucaju prevara

[27. 10. 2025., 20:01:01] ~ Faris: a i kao user to volim najvise 😀

[27. 10. 2025., 20:01:10] ~ Faris: tako je, i ne moram razmisljat o sifri kao user

[27. 10. 2025., 20:01:39] Mahir Kadic: hajmo to kompletirati, pa onda vidjeti sljedece sta je

[27. 10. 2025., 20:01:55] ~ Faris: ja sam skontao da imam jedan bug sad za auth, to cu fiksati bzo

[27. 10. 2025., 20:02:31] Mahir Kadic: uglavnom ako ste vi svoj dio zavrsili, posaljite nam ekvivalent swaggera za firebase 😀

[27. 10. 2025., 20:02:53] ~ Faris: Negdje se razilazimo 😀

[27. 10. 2025., 20:03:10] ~ Faris: sto se tice dodavanja vozaca, to ide preko sdk, collection drivers

[27. 10. 2025., 20:03:34] Mahir Kadic: ugl nesto da imamo standardizovane tipove podataka i dokumentaciju ruta

[27. 10. 2025., 20:03:38] ~ Faris: tu mi ne moramo nista dodavati

[27. 10. 2025., 20:03:50] Mahir Kadic: buni me firebase hahah

[27. 10. 2025., 20:04:09] ~ Faris: razumijem, drugacije je od standardnog apija

[27. 10. 2025., 20:04:17] Mahir Kadic: msm razumijem ga, ali dok ne odradimo koju funkciju

[27. 10. 2025., 20:04:45] Mahir Kadic: a za sta je onda funkcija za sms login, tj unos onih podataka naknadno

[27. 10. 2025., 20:04:51] Mahir Kadic: i to mozemo preko sdk 😀

[27. 10. 2025., 20:04:59] ~ Faris: e cek, evo da vidis kako ce izgledati funkcija jedna

[27. 10. 2025., 20:05:01] Mahir Kadic: tu se ja malo razilazim

[27. 10. 2025., 20:05:02] ~ Faris: sve ce ti biti jasno

[27. 10. 2025., 20:05:09] Mahir Kadic: hajde

[27. 10. 2025., 20:14:05] ~ Faris: dok ova sad funkcija koju sam napravio u sustini se ‘kaci’ na Auth servis, osluskuje registracije i upisuje u bazu

[27. 10. 2025., 20:14:16] ~ Faris: uglavnom nikakva pamet 😀

[27. 10. 2025., 20:14:46] ~ Faris: Za kompleksnijju logiku mi pisemo funkcije, za basic stvari vi direktno idete u firestore ‎<This message was edited>

[27. 10. 2025., 20:15:47] ~ Faris: ako treba bilo sta objasniti pisi

[27. 10. 2025., 20:15:53] ~ Faris: tu sam

[27. 10. 2025., 20:16:21] ~ Faris: Da li bi vam odgovarao neki seemicno sync srijedom oko pola 6?

[27. 10. 2025., 20:22:04] Mahir Kadic: Eh to je to, moja je briga najveca bila, kalkulacije na uredjajima, ako mozemo preko funkcija rjesiti, onda super.

[27. 10. 2025., 20:22:40] ~ Faris: to ide nama, da nam useri ne hodaju sa eksternim baterijama 😂

[27. 10. 2025., 20:22:40] Mahir Kadic: mozemo neki kratki od pola 6 do 6
