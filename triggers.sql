--
--
--
--
-- Functions appelées par les triggers
--
CREATE OR REPLACE FUNCTION map_update() RETURNS TRIGGER AS $BODY$
BEGIN
WITH all_points AS (
    SELECT pb.center
    FROM parc_block_projet pbp, parc_block pb
    WHERE projet_id IN
     (
    SELECT projet_id FROM map_map_projets WHERE map_id = NEW.map_id
    )

    AND pb.id = pbp.block_id
    AND pb.center IS NOT NULL
)

UPDATE map_map SET center= (SELECT ST_Centroid(ST_Union(center)) FROM all_points) WHERE map_map.id=NEW.map_id;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

--
-- Declaration des triggers
--
DROP TRIGGER map_map_projets_insert_trigger ON map_map_projets;
CREATE TRIGGER map_map_projets_insert_trigger
    AFTER INSERT ON map_map_projets
    FOR EACH ROW
    EXECUTE PROCEDURE map_update();

DROP TRIGGER map_map_projets_delete_trigger ON map_map_projets;
CREATE TRIGGER map_map_projets_delete_trigger
    AFTER DELETE ON map_map_projets
    FOR EACH ROW
    EXECUTE PROCEDURE map_update();

--
--
--
CREATE OR REPLACE FUNCTION site_parcel_aggregats_update() RETURNS TRIGGER AS $BODY$
BEGIN
UPDATE parc_site SET nb_parcel= (SELECT count(*) FROM parc_parcel WHERE site_id=NEW.site_id) WHERE parc_site.id=NEW.site_id;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

DROP TRIGGER parc_parcel_all_trigger ON parc_parcel;
CREATE TRIGGER parc_parcel_all_trigger
    AFTER INSERT OR UPDATE OR DELETE ON parc_parcel
    FOR EACH ROW
    EXECUTE PROCEDURE site_parcel_aggregats_update();
