-- launch sqlite3
.databases

create table Membres (
    license text primary key,
    nom text,
    prenom text,
    date_n text,
    email text,
    club_id text) ;
    
create table Clubs (
    club_id text primary key,
    nom_club text,
    ville text,
    email text) ;
    
create table Evenements (
    ev_id text primary key,
    club_id text,
    categorie text,
    date_e text,
    heure_e text,
    nb_places text,
    etat text,
    adresse text,
    description text,
    FOREIGN KEY(club_id) REFERENCES Membres(club_id)) ;
    
create table Inscriptions (
    license text,
    ev_id text,
    FOREIGN KEY(license) REFERENCES Membres(license),
    FOREIGN KEY(ev_id) REFERENCES Evenements(ev_id) );
    
create table Suivits (
    license text,
    club_id text,
     FOREIGN KEY(license) REFERENCES Membres(license),
    FOREIGN KEY(club_id) REFERENCES Membres(club_id)) ;
    
create table Categories (
    license text,
    groupe_id text primary key,
    FOREIGN KEY(license) REFERENCES Membres(license)) ;
    
create table Connex_Club (
    login_club text primary key,
    mdp_club text,
    club_id text,
    FOREIGN KEY(club_id) REFERENCES Membres(club_id)) ;
    
create table Connex_Membre (
    login_membre text primary key,
    mdp_membre text,
    license text,
    FOREIGN KEY(license) REFERENCES Membres(license)) ;
    
.tables

.schema table

insert into Membres(license,nom,prenom,date_n,email,club_id)
values ("12345678","olivier", "rger","01021994","hgjhegf@gmail.com",1234567) ;

insert into Membres(license,nom,prenom,date_n,email,club_id)
values ("987654","jean-louis", "jhgjh","020318995","hffx@gmail.com",123);

insert into Clubs(club_id,nom,ville,email)
values ("1a","martiniclub","lyon",martiniclub@gmail.com);

insert into Clubs(club_id,nom_club,ville,email)
values ("1b","cecileclub","paris",cecileclub@gmail.com);






























