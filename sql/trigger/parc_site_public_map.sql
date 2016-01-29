--
-- JSON Support for 1.8.8
--
CREATE OR REPLACE FUNCTION parc_site_public_map()
    RETURNS trigger AS $parc_site_public_map$
BEGIN

NEW.map_public_info = NEW.properties;


  RETURN NEW;
END;
$parc_site_public_map$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_site_public_map ON parc_site;
CREATE TRIGGER parc_site_public_map
    BEFORE INSERT OR UPDATE ON parc_site
    FOR EACH ROW
       EXECUTE PROCEDURE parc_site_public_map();

--
--
-- denormalization
--
CREATE OR REPLACE FUNCTION parc_block_nb_amg()
    RETURNS trigger AS $$
BEGIN

IF (TG_OP = 'UPDATE') THEN
  IF OLD.block_id != NEW.block_id THEN
    UPDATE parc_block SET nb_amg=nb_amg-1 WHERE id=OLD.block_id;
    UPDATE parc_block SET nb_amg=nb_amg+1 WHERE id=NEW.block_id;
  END IF;
ELSIF (TG_OP = 'DELETE') THEN

  UPDATE parc_block SET nb_amg=nb_amg-1 WHERE id=OLD.block_id;

ELSIF (TG_OP = 'INSERT') THEN

  UPDATE parc_block SET nb_amg=nb_amg+1 WHERE id=NEW.block_id;

END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_block_amg ON agrof_amenagement;
CREATE TRIGGER parc_block_amg
    AFTER INSERT OR UPDATE OR DELETE ON agrof_amenagement
    FOR EACH ROW
       EXECUTE PROCEDURE parc_block_nb_amg();
