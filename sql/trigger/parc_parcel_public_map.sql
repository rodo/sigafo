--
-- TODO 
--
CREATE OR REPLACE FUNCTION parc_parcel_json()
    RETURNS trigger AS $parc_parcel_json$
BEGIN

NEW.properties =
json_build_object(
    'name', NEW.name,
    'center', NEW.center,
    'experimental', NEW.experimental,
    'surface', NEW.surface
   );

NEW.map_public_info = NEW.properties;

  RETURN NEW;
END;
$parc_parcel_json$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_parcel_json ON parc_parcel;
CREATE TRIGGER parc_parcel_json
    BEFORE INSERT OR UPDATE ON parc_parcel
    FOR EACH ROW
       EXECUTE PROCEDURE parc_parcel_json();
