--
--
--

CREATE OR REPLACE FUNCTION parc_parcel_nb_block()
    RETURNS trigger AS $$
BEGIN

IF (TG_OP = 'UPDATE') THEN
  IF OLD.parcel_id != NEW.parcel_id THEN
    UPDATE parc_parcel SET nb_block=nb_block-1 WHERE id=OLD.parcel_id;
    UPDATE parc_parcel SET nb_block=nb_block+1 WHERE id=NEW.parcel_id;
  END IF;
ELSIF (TG_OP = 'DELETE') THEN

  UPDATE parc_parcel SET nb_block=nb_block-1 WHERE id=OLD.parcel_id;

ELSIF (TG_OP = 'INSERT') THEN

  UPDATE parc_parcel SET nb_block=nb_block+1 WHERE id=NEW.parcel_id;

END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS parc_parcel_amg ON parc_block;
CREATE TRIGGER parc_parcel_amg
    AFTER INSERT OR UPDATE OR DELETE ON parc_block
    FOR EACH ROW
       EXECUTE PROCEDURE parc_parcel_nb_block();
