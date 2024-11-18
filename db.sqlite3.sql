BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "tva_tva" (
	"id"	integer NOT NULL,
	"taux_tva"	decimal NOT NULL,
	"description"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "article_article" (
	"id"	integer NOT NULL,
	"code_article"	varchar(50) NOT NULL UNIQUE,
	"nom"	varchar(100) NOT NULL,
	"description"	text NOT NULL,
	"prix_unitaire"	decimal NOT NULL,
	"stock"	integer NOT NULL,
	"categorie_id"	bigint NOT NULL,
	"tva_id"	bigint NOT NULL,
	FOREIGN KEY("tva_id") REFERENCES "tva_tva"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("categorie_id") REFERENCES "categorie_article_categoriearticle"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "client_client" (
	"id"	integer NOT NULL,
	"code_client"	varchar(50) NOT NULL UNIQUE,
	"nom"	varchar(100) NOT NULL,
	"adresse"	varchar(255) NOT NULL,
	"email"	varchar(100) NOT NULL UNIQUE,
	"telephone"	varchar(20) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ligne_facture_lignefacture" (
	"id"	integer NOT NULL,
	"quantite"	integer NOT NULL,
	"prix_unitaire"	decimal NOT NULL,
	"taux_remise"	decimal NOT NULL,
	"montant_ht"	decimal NOT NULL,
	"montant_tva"	decimal NOT NULL,
	"montant_ttc"	decimal NOT NULL,
	"article_id"	bigint NOT NULL,
	"facture_id"	bigint NOT NULL,
	FOREIGN KEY("article_id") REFERENCES "article_article"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("facture_id") REFERENCES "facture_facture"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "tva_facture_tva_facture" (
	"id"	integer NOT NULL,
	"montant_total_tva"	decimal NOT NULL,
	"facture_id"	bigint NOT NULL,
	"taux_tva_id"	bigint NOT NULL,
	FOREIGN KEY("taux_tva_id") REFERENCES "tva_tva"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("facture_id") REFERENCES "facture_facture"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "facture_lignefacture" (
	"id"	integer NOT NULL,
	"quantite"	integer NOT NULL,
	"prix_unitaire"	decimal NOT NULL,
	"taux_remise"	decimal NOT NULL,
	"montant_ht"	decimal NOT NULL,
	"montant_tva"	decimal NOT NULL,
	"montant_ttc"	decimal NOT NULL,
	"article_id"	bigint NOT NULL,
	"facture_id"	bigint NOT NULL,
	"montant_remise"	decimal NOT NULL,
	FOREIGN KEY("facture_id") REFERENCES "facture_facture"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("article_id") REFERENCES "article_article"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "categorie_article_categoriearticle" (
	"id"	integer NOT NULL,
	"nom"	varchar(100) NOT NULL,
	"taux_tva"	decimal NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "facture_facture" (
	"id"	integer NOT NULL,
	"numero_facture"	varchar(100) NOT NULL,
	"date_facture"	date NOT NULL,
	"total_ht"	decimal NOT NULL,
	"total_ttc"	decimal NOT NULL,
	"total_tva"	decimal NOT NULL,
	"client_id"	bigint NOT NULL,
	"etat"	varchar(20) NOT NULL,
	FOREIGN KEY("client_id") REFERENCES "client_client"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2024-10-09 20:02:17.000872'),
 (2,'auth','0001_initial','2024-10-09 20:02:17.031768'),
 (3,'admin','0001_initial','2024-10-09 20:02:17.053945'),
 (4,'admin','0002_logentry_remove_auto_add','2024-10-09 20:02:17.072079'),
 (5,'admin','0003_logentry_add_action_flag_choices','2024-10-09 20:02:17.093182'),
 (6,'tva','0001_initial','2024-10-09 20:02:17.100538'),
 (7,'categorie_article','0001_initial','2024-10-09 20:02:17.107659'),
 (8,'article','0001_initial','2024-10-09 20:02:17.124805'),
 (9,'contenttypes','0002_remove_content_type_name','2024-10-09 20:02:17.153734'),
 (10,'auth','0002_alter_permission_name_max_length','2024-10-09 20:02:17.172735'),
 (11,'auth','0003_alter_user_email_max_length','2024-10-09 20:02:17.190785'),
 (12,'auth','0004_alter_user_username_opts','2024-10-09 20:02:17.204629'),
 (13,'auth','0005_alter_user_last_login_null','2024-10-09 20:02:17.220987'),
 (14,'auth','0006_require_contenttypes_0002','2024-10-09 20:02:17.227182'),
 (15,'auth','0007_alter_validators_add_error_messages','2024-10-09 20:02:17.240481'),
 (16,'auth','0008_alter_user_username_max_length','2024-10-09 20:02:17.258521'),
 (17,'auth','0009_alter_user_last_name_max_length','2024-10-09 20:02:17.276553'),
 (18,'auth','0010_alter_group_name_max_length','2024-10-09 20:02:17.294768'),
 (19,'auth','0011_update_proxy_permissions','2024-10-09 20:02:17.311622'),
 (20,'auth','0012_alter_user_first_name_max_length','2024-10-09 20:02:17.330640'),
 (21,'client','0001_initial','2024-10-09 20:02:17.338951'),
 (22,'facture','0001_initial','2024-10-09 20:02:17.364614'),
 (23,'ligne_facture','0001_initial','2024-10-09 20:02:17.384954'),
 (24,'sessions','0001_initial','2024-10-09 20:02:17.400554'),
 (25,'tva_facture','0001_initial','2024-10-09 20:02:17.421507'),
 (26,'facture','0002_remove_facture_total_remise','2024-10-10 20:12:43.659711'),
 (27,'facture','0003_auto_20241012_2144','2024-10-12 21:44:26.158114'),
 (28,'categorie_article','0002_categoriearticle_taux_tva','2024-10-16 19:30:33.284627'),
 (29,'facture','0004_delete_categoriearticle','2024-10-16 19:30:33.306836'),
 (30,'facture','0005_categoriearticle','2024-10-16 19:47:56.053565'),
 (31,'facture','0006_delete_categoriearticle','2024-10-16 19:52:53.718438'),
 (32,'facture','0007_alter_facture_etat','2024-10-23 12:02:30.995922'),
 (33,'facture','0008_alter_facture_etat','2024-10-23 21:19:16.599018');
INSERT INTO "tva_tva" ("id","taux_tva","description") VALUES (1,7,'7%'),
 (2,10,'10%'),
 (3,19,'19%');
INSERT INTO "article_article" ("id","code_article","nom","description","prix_unitaire","stock","categorie_id","tva_id") VALUES (11,'ART001','PC de Bureau','Pcs',1000,10,13,1),
 (12,'ART002','Imprimante HP deskjet 315','Printers',500,10,14,1),
 (13,'ART003','Toners Sharp 6031','toners',350,10,12,3),
 (14,'ART004','Encre DX 2430','encres',10,100,11,3),
 (15,'ART005','Claviers','claviers',15,10,15,1);
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry'),
 (2,'auth','permission'),
 (3,'auth','group'),
 (4,'auth','user'),
 (5,'contenttypes','contenttype'),
 (6,'sessions','session'),
 (7,'client','client'),
 (8,'article','article'),
 (9,'categorie_article','categoriearticle'),
 (10,'tva','tva'),
 (11,'facture','categoriearticle'),
 (12,'facture','facture'),
 (13,'facture','lignefacture'),
 (14,'ligne_facture','lignefacture'),
 (15,'tva_facture','tva_facture');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_user','Can add user'),
 (14,4,'change_user','Can change user'),
 (15,4,'delete_user','Can delete user'),
 (16,4,'view_user','Can view user'),
 (17,5,'add_contenttype','Can add content type'),
 (18,5,'change_contenttype','Can change content type'),
 (19,5,'delete_contenttype','Can delete content type'),
 (20,5,'view_contenttype','Can view content type'),
 (21,6,'add_session','Can add session'),
 (22,6,'change_session','Can change session'),
 (23,6,'delete_session','Can delete session'),
 (24,6,'view_session','Can view session'),
 (25,7,'add_client','Can add client'),
 (26,7,'change_client','Can change client'),
 (27,7,'delete_client','Can delete client'),
 (28,7,'view_client','Can view client'),
 (29,8,'add_article','Can add article'),
 (30,8,'change_article','Can change article'),
 (31,8,'delete_article','Can delete article'),
 (32,8,'view_article','Can view article'),
 (33,9,'add_categoriearticle','Can add categorie article'),
 (34,9,'change_categoriearticle','Can change categorie article'),
 (35,9,'delete_categoriearticle','Can delete categorie article'),
 (36,9,'view_categoriearticle','Can view categorie article'),
 (37,10,'add_tva','Can add tva'),
 (38,10,'change_tva','Can change tva'),
 (39,10,'delete_tva','Can delete tva'),
 (40,10,'view_tva','Can view tva'),
 (41,11,'add_categoriearticle','Can add categorie article'),
 (42,11,'change_categoriearticle','Can change categorie article'),
 (43,11,'delete_categoriearticle','Can delete categorie article'),
 (44,11,'view_categoriearticle','Can view categorie article'),
 (45,12,'add_facture','Can add facture'),
 (46,12,'change_facture','Can change facture'),
 (47,12,'delete_facture','Can delete facture'),
 (48,12,'view_facture','Can view facture'),
 (49,13,'add_lignefacture','Can add ligne facture'),
 (50,13,'change_lignefacture','Can change ligne facture'),
 (51,13,'delete_lignefacture','Can delete ligne facture'),
 (52,13,'view_lignefacture','Can view ligne facture'),
 (53,14,'add_lignefacture','Can add ligne facture'),
 (54,14,'change_lignefacture','Can change ligne facture'),
 (55,14,'delete_lignefacture','Can delete ligne facture'),
 (56,14,'view_lignefacture','Can view ligne facture'),
 (57,15,'add_tva_facture','Can add tv a_ facture'),
 (58,15,'change_tva_facture','Can change tv a_ facture'),
 (59,15,'delete_tva_facture','Can delete tv a_ facture'),
 (60,15,'view_tva_facture','Can view tv a_ facture');
INSERT INTO "client_client" ("id","code_client","nom","adresse","email","telephone") VALUES (1,'C001','Société Alpha Ben Beta Ben Gamma Ben ZETA','123 Rue Principale, Paris','contact@alpha.com','01 23 45 67 89'),
 (2,'C002','Société Bêta','456 Avenue de Exemple, Lyon','info@beta.com','01 98 76 54 32'),
 (3,'C003','Société Gamma','789 Boulevard des Exemples, Marseille','service@gamma.com','04 12 34 56 78'),
 (4,'C004','Société Delta','321 Rue des Innovations, Toulouse','support@delta.com','05 12 34 56 78'),
 (5,'C005','Société Epsilon','654 Route du Progrès, Nice','contact@epsilon.com','06 12 34 56 78'),
 (6,'C006','Société Zeta','159 Chemin de la Réussite, Nantes','info@zeta.com','02 12 34 56 78'),
 (7,'C007','Société Eta','753 Rue de la Confiance, Lille','service@eta.com','03 12 34 56 78'),
 (8,'C008','Société Thêta','852 Avenue des Projets, Strasbourg','support@theta.com','04 56 78 90 12'),
 (9,'C009','Société Iota','963 Boulevard des Rêves, Bordeaux','contact@iota.com','05 98 76 54 32'),
 (10,'C010','Société Kappa','159 Rue de la Stratégie, Montpellier','info@kappa.com','06 45 67 89 12');
INSERT INTO "facture_lignefacture" ("id","quantite","prix_unitaire","taux_remise","montant_ht","montant_tva","montant_ttc","article_id","facture_id","montant_remise") VALUES (180,2,1000,10,1800,126,1926,11,114,200),
 (181,10,10,5,95,18.05,113.05,14,114,5);
INSERT INTO "categorie_article_categoriearticle" ("id","nom","taux_tva") VALUES (11,'Encre',0),
 (12,'Toners',0),
 (13,'PCs',0),
 (14,'Printers',0),
 (15,'Accessoires',0);
INSERT INTO "facture_facture" ("id","numero_facture","date_facture","total_ht","total_ttc","total_tva","client_id","etat") VALUES (114,'FCT-114','2024-11-02',1895,2039.05,144.05,3,'impayee');
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "article_article_categorie_id_43e274f0" ON "article_article" (
	"categorie_id"
);
CREATE INDEX IF NOT EXISTS "article_article_tva_id_49a87721" ON "article_article" (
	"tva_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "ligne_facture_lignefacture_article_id_3f7ce04c" ON "ligne_facture_lignefacture" (
	"article_id"
);
CREATE INDEX IF NOT EXISTS "ligne_facture_lignefacture_facture_id_bf5a0f93" ON "ligne_facture_lignefacture" (
	"facture_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "tva_facture_tva_facture_facture_id_c6617353" ON "tva_facture_tva_facture" (
	"facture_id"
);
CREATE INDEX IF NOT EXISTS "tva_facture_tva_facture_taux_tva_id_01594890" ON "tva_facture_tva_facture" (
	"taux_tva_id"
);
CREATE INDEX IF NOT EXISTS "facture_lignefacture_article_id_bf400621" ON "facture_lignefacture" (
	"article_id"
);
CREATE INDEX IF NOT EXISTS "facture_lignefacture_facture_id_de954059" ON "facture_lignefacture" (
	"facture_id"
);
CREATE INDEX IF NOT EXISTS "facture_facture_client_id_eceaee6f" ON "facture_facture" (
	"client_id"
);
COMMIT;
