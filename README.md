# Prosjektbeskrivelse og dokumentasjon
## Neglesalong – Timebestillingssystem

## 1. Prosjektidé og problemstilling
Hva er prosjektet ditt?
Prosjektet er en nettside der kunder kan bestille negletime direkte hos salongen. Nettsiden samler timebestilling på ett sted og gjør prosessen enkel og oversiktlig.
I dag må mange kunder bestille time ved å sende DM på Instagram. Dette kan føre til lang ventetid, misforståelser og tapte henvendelser, både for kunden og negleteknikeren. Løsningen gjør timebestilling raskere, mer effektiv og mer oversiktlig. Kundene kan bestille time når det passer dem, og negleteknikeren får bedre kontroll over timeplanen sin.
Målgruppen er personer som regelmessig tar manikyr eller andre neglbehandlinger. Løsningen er laget for både kunder og negleteknikere, siden den forenkler kommunikasjon, sparer tid og gir en bedre opplevelse for begge parter.


## Hva jeg skal gjøre på eksamensdagen
Jeg skal lage en admin og brukerside, sørge for at man må være innlogget for å sende inn spørsmål, oppdatere FAQ, implementere GDPR-funksjonalitet (mulighet for å slette sin egen bruker).
[Kanban board](https://github.com/users/heleneliasi/projects/4)


### Systemet skal ha følgende funksjoner:
Vise tilgjengelige timer
Bestille negletime
Lagre kundeinformasjon
Administrere timeplan for negletekniker
Admin og brukerside med innlogging
FAQ-administrasjon
GDPR (sletting av brukerdata)


## 2. Systembeskrivelse
### Formål med applikasjonen:
Applikasjonen skal digitalisere timebestillingsprosessen for en neglesalong. Målet er å erstatte manuell kontakt via sosiale medier med et strukturert og brukervennlig bookingsystem.
### Brukerflyt:
Brukeren åpner nettsiden og kan se tilgjengelige tjenester og ledige timer. Deretter registrerer eller logger brukeren seg inn, velger ønsket behandling og tidspunkt, og bekrefter bestillingen. Negleteknikeren (admin) kan logge inn på adminsiden for å se og administrere timeplanen.


### Teknologier brukt:
Python/Flask
MariaDB
HTML/CSS/JS
Waitress


## 3. Server-, infrastruktur- og nettverksoppsett
### Servermiljø
Raspberry Pi med Debian OS
Flask-applikasjonen kjøres med Waitress på port 8080


### Nettverksoppsett
Nettverksdiagram: Klient (nettleser) -> Raspberry Pi (flask/waitress port 8080) -> MariaDB (port 3306)
IP-adresser: (10.200.14.17)
Porter:
22 (ssh)
80 (http)
3306 (mariadb)
samba (fildeling)
8080 (flask/waitress)
Brannmurregler: Konfigurert med ufw. Tillatte porter: 22, 80, 3306, samba, 8080


### Tjenestekonfigurasjon
Webserver: Waitress kjører flask-applikasjonen på port 8080
Database: Mariadb kjører på port 3306
Miljøvariabler: Lagret i .env fil
Filrettigheter: .env og venv er ekskludert fra github via .gitignore


## 4. Prosjektstyring – GitHub Projects (Kanban)
[Kanban board](https://github.com/users/heleneliasi/projects/4)
<img width="1919" height="908" alt="image" src="https://github.com/user-attachments/assets/ee7fd110-6202-44ca-9292-8fafa0d32499" />
Refleksjon: Kanban boardet hjelper meg å holde oversikt over hvilke oppgaver som var gjort og hva som gjenstod, jeg kan ser arbeidsprosessen visuelt. Det gjorde det enklere å prioritere arbeidet og se fremgangen underveis. 

## 5. Databasebeskrivelse
### Databasenavn: neglesalong
### Oversikt over tabeller
**Tabell 1**
- Navn: users 
- Beskrivelse: Lagrer informasjon om kunder og admin

**Tabell 2**
- Navn: appointment  
- Beskrivelse: Lagrer informasjon om bookende timer

**Tabell 3**
- Navn: service  
- Beskrivelse: Lagrer informasjon om ulike neglbehandlinger

**Tabell 4**
- Navn: questions 
- Beskrivelse: Lagrer innsendte spørsmål fra brukere

### Tabeller:
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(6,2) NOT NULL
);

CREATE TABLE appointment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES service(id)
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) DEFAULT NULL,
    email VARCHAR(150) DEFAULT NULL,
    question TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);


## 6. Programstruktur
neglesalong-eksamen/
 ├── app.py
 ├── db.py
 ├── neglesalong.sql
 ├── requirements.txt
 ├── .env
 ├── .gitignore
 ├── templates/
 │   ├── book.html
 │   ├── confirmation.html
 │   ├── faq.html
 │   ├── index.html
 │   ├── login.html
 │   ├── registrer.html
 │   ├── sendinn.html
 │   └── services.html
 └── static/
     ├── images/
     ├── script.js
     └── style.css

Databasestrøm:
Bruker fyller inn skjema (HTML) -> flask mottar data -> mariadb lagrer/henter data -> flask sender data tilbake -> HTML viser resultatet
