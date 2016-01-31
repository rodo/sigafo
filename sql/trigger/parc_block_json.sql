--
-- TODO 
--
CREATE OR REPLACE FUNCTION parc_block_json()
    RETURNS trigger AS $parc_block_json$
BEGIN


--NEW.properties =
--json_build_object(
--    'surface', NEW.surface,
--   'date_start', NEW.date_debut
--    );

    NEW.map_public_info = json_append(
        ('{"parcel":' || (SELECT map_public_info FROM parc_parcel WHERE id=NEW.parcel_id) || '}')::json,
        NEW.properties);

  RETURN NEW;
END;
$parc_block_json$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_block_json ON parc_block;
CREATE TRIGGER parc_block_json
    BEFORE INSERT OR UPDATE ON parc_block
    FOR EACH ROW
       EXECUTE PROCEDURE parc_block_json();
