--
--
--
CREATE OR REPLACE FUNCTION agrof_amenagement_json()
    RETURNS trigger AS $agrof_amenagement_json$
BEGIN

NEW.properties =
json_build_object(
    'localisation_id', NEW.localisation,
    'nature', (SELECT name FROM referentiel_amnature WHERE id=NEW.nature_id),
    'essences', (SELECT array_agg(essence) FROM v_amenagement_essences WHERE amenagement_id = NEW.id),
    'dist_on_line', NEW.dist_on_line,
    'density', NEW.density
    );

NEW.map_public_info = NEW.properties;

  RETURN NEW;
END;
$agrof_amenagement_json$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS agrof_amenagement_json ON agrof_amenagement;
CREATE TRIGGER agrof_amenagement_json
    BEFORE INSERT OR UPDATE ON agrof_amenagement
    FOR EACH ROW
       EXECUTE PROCEDURE agrof_amenagement_json();
--
--
-- denormalization
--
