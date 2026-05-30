# Prosjektbeskrivelse og dokumentasjon
## Neglesalong – Timebestillingssystem

## 1. Prosjektidé og problemstilling
Hva er prosjektet ditt?
Prosjektet er en nettside der kunder kan bestille negletime direkte hos salongen. Nettsiden samler timebestilling på ett sted og gjør prosessen enkel og oversiktlig.
I dag må mange kunder bestille time ved å sende DM på Instagram. Dette kan føre til lang ventetid, misforståelser og tapte henvendelser, både for kunden og negleteknikeren. Løsningen gjør timebestilling raskere, mer effektiv og mer oversiktlig. Kundene kan bestille time når det passer dem, og negleteknikeren får bedre kontroll over timeplanen sin.
Målgruppen er personer som regelmessig tar manikyr eller andre neglbehandlinger. Løsningen er laget for både kunder og negleteknikere, siden den forenkler kommunikasjon, sparer tid og gir en bedre opplevelse for begge parter.


## Hva jeg skal gjøre på eksamensdagen
Jeg skal lage en admin og brukerside, sørge for at man må være innlogget for å sende inn spørsmål, oppdatere FAQ, implementere GDPR-funksjonalitet (mulighet for å slette sin egen bruker).
(legg til link til ferdig kanban for eksamensdagen)

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
F.eks.: Ubuntu VM, Docker, fysisk server – fyll inn her.

### Nettverksoppsett
Nettverksdiagram: (sett inn diagram)
IP-adresser: ()
Porter: ()
Brannmurregler: ()

Klient -> Flask/Waitress -> MariaDB

### Tjenestekonfigurasjon
systemctl
Filrettigheter
Miljøvariabler (.env)


## 4. Prosjektstyring – GitHub Projects (Kanban)

To Do/In Progress/Done
Issues
(skjermbilde)

Refleksjon: Hvordan hjalp kanban arbeidet?

## 5. Databasebeskrivelse
### Databasenavn: neglesalong
### Oversikt over tabeller
**Tabell 1**
- Navn: User  
- Beskrivelse: Lagrer informasjon om kunder og negleteknikere

**Tabell 2**
- Navn: Appointment  
- Beskrivelse: Lagrer informasjon om bookede timer

**Tabell 3**
- Navn: Service  
- Beskrivelse: Lagrer informasjon om ulike neglbehandlinger

### Tabeller:
CREATE TABLE User (
    id       INT          AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email    VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE Appointment (
    id      INT  AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date    DATE,
    time    TIME,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Service (
    id    INT           AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    question TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## 6. Programstruktur
neglesalong/
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
     └── style.css
Databasestrøm:
HTML → Flask → MariaDB → Flask → HTML-tabell
