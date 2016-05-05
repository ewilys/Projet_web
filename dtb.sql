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
    ev_id integer primary key AUTOINCREMENT,
    nom_ev text,
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


    
create table Suivis (
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
values ("12345678","martini", "lisa","12051994","martini.lisa14@gmail.com",026159) ; /*nom des catégories all poussinado jeune senior */

insert into Connex_Membre(login_membre, mdp_membre, license)
values ("lisa","moi","12345678")

insert into Membres(license,nom,prenom,date_n,email,club_id)
values ("89987654","jean-louis", "jhgjh","020318995","hffx@gmail.com",123);

insert into Clubs(club_id,nom_club,ville,email)
values ("568423","martiniclub","lyon","martiniclub@gmail.com");

insert into Clubs(club_id,nom_club,ville,email)
values ("547634","cecileclub","paris","cecileclub@gmail.com");

insert into Connex_Membre(login_membre, mdp_membre, license)
values ("lisa", "moi", "12345678");

insert into Evenements(nom_ev,club_id,categorie,date_e,heure_e,nb_places,etat,adresse,description)
values ("coupe normandie handball","martiniclub","all","19022017","1600","50","disponible","30, avenue de gaulle,Havre"," événement handball organisé par martiniclub accès publique");


insert into Evenements(nom_ev,club_id,categorie,date_e,heure_e,nb_places,etat,adresse,description)
values("equitation trophy","cecileclub","jeune",15062016,"1200","15","complet","2, rue des arts villeurbanneé","compétition déquitation sur le campus de la DOUA");

insert into Inscriptions(license,ev_id)
values ("89987654","2");


insert into Inscriptions(license,ev_id)
values ("50123456","1");

insert into Inscriptions(license,ev_id)
values ("50123456","2");

insert into Suivis(license,club_id)
values("50123456","547634");


insert into Suivis(license,club_id)
values("50123456","568423");


insert into Suivis(license,club_id)
values("89987654","568423");

insert into Categories(license,groupe_id)
values("89987654","jeune");

insert into Categories(license,groupe_id)
values("50123456","senior");















