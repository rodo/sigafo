BEGIN;

DROP TABLE "agrof_measure" CASCADE;
DROP TABLE "agrof_indicator" CASCADE;

DROP TABLE "agrof_peuplement" CASCADE;
DROP TABLE "agrof_peuplement_essences" CASCADE;
DROP TABLE "agrof_essence" CASCADE;

DROP TABLE "projet_projet" CASCADE;

DROP TABLE "parc_parcel" CASCADE;
DROP TABLE "parc_parcel_projet" CASCADE;
DROP TABLE "parc_champ" CASCADE;
DROP TABLE "parc_site" CASCADE;

DROP TABLE "contact_contact" CASCADE;
DROP TABLE "contact_activite" CASCADE;
COMMIT;
