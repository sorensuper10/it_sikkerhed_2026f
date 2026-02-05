03/02/2026
# Dette er et skoleprojekt på Zealand Næstved.
Unit test
<img width="1357" height="696" alt="Screenshot" src="https://github.com/user-attachments/assets/22ea4ea0-ab07-414e-a933-d70d2a3629b9" />

Mine egne unit tests

<img width="520" height="821" alt="Sceenshot1" src="https://github.com/user-attachments/assets/0c7a46bd-4063-4281-8983-67b5e884e52b" />

05/02/2026
## Valgt emne: Login- og adgangskontrolsystem (Authentication & Authorization)

Systemet er et simpelt login- og brugerhåndteringssystem med følgende funktioner:

* Login med brugernavn og adgangskode
* Kontolås efter for mange fejlede loginforsøg
* CRUD(L) på brugere (Create, Read, Update, Delete, List)

Dette emne er velegnet til IT-sikkerhed, da det berører:

* Brugerautentificering
* Adgangskontrol
* Beskyttelse mod brute-force angreb

---

## 1. Ækvivalensklasser (Equivalence Class Testing)

**Input: Adgangskode**

| Ækvivalensklasse | Beskrivelse                | Eksempel     | Forventet resultat |
| ---------------- | -------------------------- | ------------ | ------------------ |
| Gyldig           | 8–64 tegn, bogstaver + tal | `Test1234`   | Login tilladt      |
| Ugyldig          | Under 8 tegn               | `abc123`     | Login afvist       |
| Ugyldig          | Over 64 tegn               | `a...a (65)` | Login afvist       |
| Ugyldig          | Kun tal                    | `12345678`   | Login afvist       |

**Security gate:** Unit Test / Security Validation

---

## 2. Grænseværditest (Boundary Value Testing)

**Krav:** Adgangskode skal være mellem 8 og 64 tegn

| Test         | Input længde | Forventet resultat |
| ------------ | ------------ | ------------------ |
| Under grænse | 7            | Afvist             |
| Nedre grænse | 8            | Godkendt           |
| Over nedre   | 9            | Godkendt           |
| Øvre grænse  | 64           | Godkendt           |
| Over grænse  | 65           | Afvist             |

**Security gate:** Unit Test

---

## 3. CRUD(L) test (User Management)

| Operation | Testbeskrivelse    | Forventet resultat        |
| --------- | ------------------ | ------------------------- |
| Create    | Opret ny bruger    | Bruger oprettet           |
| Read      | Hent bruger via ID | Korrekt bruger returneres |
| Update    | Skift adgangskode  | Adgangskode opdateret     |
| Delete    | Slet bruger        | Bruger fjernet            |
| List      | Vis alle brugere   | Liste returneres          |

**Security gate:** Integration Test

---

## 4. Cycle Process Test (Login lifecycle)

**Proces:**

1. Bruger indtaster login
2. System validerer input
3. System tjekker credentials
4. Login godkendt eller afvist
5. Fejltæller opdateres
6. Konto låses efter 5 fejl

**Test:**

* Gentag loginforsøg 5 gange med forkert adgangskode
* Verificer at kontoen låses

**Security gate:** System Test / Security Test

---

## 5. Testpyramiden

| Lag               | Eksempel                         |
| ----------------- | -------------------------------- |
| Unit tests        | Password-validering, input-check |
| Integration tests | Login mod database               |
| System tests      | Fuldt loginflow                  |
| Manuelle tests    | Penetrationstest                 |

**Security gate:** Alle gates (Shift-left security)

---

## 6. Decision Table Test

**Login beslutningstabel**

| Brugernavn korrekt | Adgangskode korrekt | Konto låst | Resultat            |
| ------------------ | ------------------- | ---------- | ------------------- |
| Ja                 | Ja                  | Nej        | Login tilladt       |
| Ja                 | Nej                 | Nej        | Login afvist        |
| Ja                 | Nej                 | Ja         | Login afvist (låst) |
| Nej                | Ja                  | Nej        | Login afvist        |
| Nej                | Nej                 | Nej        | Login afvist        |

**Security gate:** System Test

---

## Samlet oversigt – Security Gates

| Testtype           | Security Gate    |
| ------------------ | ---------------- |
| Ækvivalensklasser  | Unit Test        |
| Grænseværditest    | Unit Test        |
| CRUD(L)            | Integration Test |
| Cycle Process Test | System Test      |
| Testpyramiden      | Alle gates       |
| Decision Table     | System Test      |
