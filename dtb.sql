-- launch sqlite3
.databases

create table Membres (
    licence text primary key,
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
    nom_ev text primary key,
    club_id text,
    categorie text,
    date_e text,
    heure_e text,
    nb_places text,
    etat text,
    adresse text,
    description text,
    lien_image text,
    FOREIGN KEY(club_id) REFERENCES Membres(club_id)
    FOREIGN KEY(categorie) REFERENCES Liste_Categorie(categorie) );
    
create table Inscriptions (
    licence text,
    nom_ev text,
    FOREIGN KEY(licence) REFERENCES Membres(licence),
    FOREIGN KEY(nom_ev) REFERENCES Evenements(nom_ev) );
    
create table Suivis (
    licence text,
    club_id text,
    FOREIGN KEY(licence) REFERENCES Membres(licence),
    FOREIGN KEY(club_id) REFERENCES Clubs(club_id)) ;
 																					
create table Categories (
    licence text,
    categorie text,
    FOREIGN KEY(categorie) REFERENCES Liste_Categorie(categorie),
    FOREIGN KEY(licence) REFERENCES Membres(licence)) ;
    
create table Connex_Club (
    login_club text primary key,
    mdp_club text,
    club_id text,
    FOREIGN KEY(club_id) REFERENCES Clubs(club_id)) ;
    
create table Connex_Membre (
    login_membre text primary key,
    mdp_membre text,
    licence text,
    FOREIGN KEY(licence) REFERENCES Membres(licence)) ;
    
create table Liste_Categories (
	categorie text primary key );
        
.tables

.schema table

/*insert into Liste_Categories(categorie)  /*nom des catégories all poussin ado jeune senior */
/*values ("all"), ("poussin"), ("ado"), ("jeune"), ("senior");*/

insert into Membres(licence,nom,prenom,date_n,email,club_id)
values ("12345678","Martini", "Lisa","12-05-1994","martini.lisa14@gmail.com","026159");
/*
insert into Clubs(club_id,nom_club,ville,email)
values ("3","martiniclub","lyon","martiniclub@gmail.com"), ("4","cecileclub","paris","cecileclub@gmail.com");

insert into Connex_Membre(login_membre, mdp_membre, licence)
values ("lisa", "moi", "1"), ("jean-louis", "plop", "2");

insert into Connex_Club(login_club, mdp_club, club_id)
values ("cecileclub", "azerty", "4"), ("martiniclub", "mdp", "3");

insert into Evenements(nom_ev,club_id,categorie,date_e,heure_e,nb_places,etat,adresse,description, lien_image)
values ("coupe normandie handball","3","all","19022017","1600","50","disponible","30, avenue de gaulle,Havre"," événement handball organisé par martiniclub accès publique", "https://drive.google.com/open?id=0B39DIRT6d2sGLUQwb2RsbmU0VHM");

insert into Evenements(nom_ev,club_id,categorie,date_e,heure_e,nb_places,etat,adresse,description, lien_image)
values("equitation trophy","4","jeune","15062016","1200","15","complet","2, rue des arts villeurbanne","compétition déquitation sur le campus de la DOUA", "https://drive.google.com/open?id=0B39DIRT6d2sGUlR3a3B5T0V4VzQ");

insert into Inscriptions(licence,nom_ev)
values ("1","coupe normandie handball");

values("equitation trophy","4","jeune","15062016","1200","15","complet","2, rue des arts villeurbanne","compétition déquitation sur le campus de la DOUA", "https://drive.google.com/open?id=0B39DIRT6d2sGUlR3a3B5T0V4VzQ"),
	("coupe normandie handball","3","all","19022017","1600","50","disponible","30, avenue de gaulle,Havre"," événement handball organisé par martiniclub accès publique", "https://drive.google.com/open?id=0B39DIRT6d2sGLUQwb2RsbmU0VHM");

insert into Inscriptions(licence,nom_ev)
values ("2","coupe normandie handball"), ("1","equitation trophy"), ("1","coupe normandie handball");

insert into Suivis(licence,club_id)
values("1","3"), ("2","3"), ("1","4");

insert into Categories(licence,categorie)
values("2","jeune"), ("1","senior"), ("5", "senior");*/
