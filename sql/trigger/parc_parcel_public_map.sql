--
-- TODO 
--
CREATE OR REPLACE FUNCTION parc_parcel_json()
    RETURNS trigger AS $parc_parcel_json$
BEGIN


DELETE FROM map_parcelmap WHERE parcel_id = NEW.id;

INSERT INTO map_parcelmap (parcel_id, map_id, map_public_info) VALUES
(NEW.id, 1, (SELECT map_public_info FROM v_map_1_parcel WHERE id=NEW.id) );


NEW.properties =
json_build_object(
    'name', NEW.name,
    'center', ('{"geometry":' || ST_AsGeoJSON(NEW.center) || '}')::json,
    'experimental', NEW.experimental,
    'surface', NEW.surface,
    'icon_url', NEW.icon_url
   );

NEW.map_public_info = json_append(
    ('{"site":' || (SELECT map_public_info FROM parc_site WHERE id=NEW.site_id) || '}')::json,
    NEW.properties);

RETURN NEW;

END;
$parc_parcel_json$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_parcel_json ON parc_parcel;
CREATE TRIGGER parc_parcel_json
    BEFORE INSERT OR UPDATE ON parc_parcel
    FOR EACH ROW
       EXECUTE PROCEDURE parc_parcel_json();
