--
--
--
--
-- Functions appelées par les triggers
--
CREATE OR REPLACE FUNCTION map_update() RETURNS TRIGGER AS $BODY$
BEGIN
IF TG_OP = 'INSERT' then
WITH all_points AS (
    SELECT pb.center
    FROM parc_block_projets pbp, parc_block pb
    WHERE projet_id IN
     (
    SELECT projet_id FROM map_map_projets WHERE map_id = NEW.map_id
    )

    AND pb.id = pbp.block_id
    AND pb.center IS NOT NULL
)

UPDATE map_map SET center= (SELECT ST_Centroid(ST_Union(center)) FROM all_points) WHERE map_map.id=NEW.map_id;
ELSIF TG_OP = 'DELETE' then
WITH all_points AS (
    SELECT pb.center
    FROM parc_block_projets pbp, parc_block pb
    WHERE projet_id IN
     (
    SELECT projet_id FROM map_map_projets WHERE map_id = OLD.map_id
    )

    AND pb.id = pbp.block_id
    AND pb.center IS NOT NULL
)

UPDATE map_map SET center= (SELECT ST_Centroid(ST_Union(center)) FROM all_points) WHERE map_map.id=OLD.map_id;
END IF;

RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$BODY$ LANGUAGE plpgsql;

--
-- Declaration des triggers
--
DROP TRIGGER map_map_projets_all_trigger ON map_map_projets;
CREATE TRIGGER map_map_projets_all_trigger
    AFTER INSERT OR DELETE ON map_map_projets
    FOR EACH ROW
    EXECUTE PROCEDURE map_update();
--
--
--
CREATE OR REPLACE FUNCTION site_parcel_aggregats_update() RETURNS TRIGGER AS $BODY$
BEGIN
IF TG_OP = 'INSERT' then
    UPDATE parc_site SET
     nb_parcel= (SELECT count(*) FROM parc_parcel WHERE site_id=NEW.site_id),
     nb_block= (SELECT sum(nb_block) FROM parc_parcel WHERE site_id=NEW.site_id) WHERE parc_site.id=NEW.site_id;
ELSIF TG_OP = 'UPDATE' then
    UPDATE parc_site SET
     nb_parcel= (SELECT count(*) FROM parc_parcel WHERE site_id=NEW.site_id),
     nb_block= (SELECT sum(nb_block) FROM parc_parcel WHERE site_id=NEW.site_id) WHERE parc_site.id=NEW.site_id;
ELSIF TG_OP = 'DELETE' then
    UPDATE parc_site SET nb_parcel= (SELECT count(*) FROM parc_parcel WHERE site_id=OLD.site_id) WHERE parc_site.id=OLD.site_id;

END IF;    
RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$BODY$ LANGUAGE plpgsql;

DROP TRIGGER parc_parcel_all_trigger ON parc_parcel;
CREATE TRIGGER parc_parcel_all_trigger
    AFTER INSERT OR UPDATE OR DELETE ON parc_parcel
    FOR EACH ROW
    EXECUTE PROCEDURE site_parcel_aggregats_update();

--
--
--
CREATE OR REPLACE FUNCTION parc_block_aggregats_update() RETURNS TRIGGER AS $BODY$
BEGIN
IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' then
    UPDATE parc_parcel SET nb_block= (SELECT count(*) FROM parc_block WHERE parcel_id=NEW.parcel_id) WHERE parc_parcel.id=NEW.parcel_id;
ELSIF TG_OP = 'DELETE' then
    UPDATE parc_parcel SET nb_block= (SELECT count(*) FROM parc_block WHERE parcel_id=OLD.parcel_id) WHERE parc_parcel.id=OLD.parcel_id;

END IF;    
RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$BODY$ LANGUAGE plpgsql;

DROP TRIGGER parc_block_all_trigger ON parc_block;
CREATE TRIGGER parc_block_all_trigger
    AFTER INSERT OR UPDATE OR DELETE ON parc_block
    FOR EACH ROW
    EXECUTE PROCEDURE parc_block_aggregats_update();
