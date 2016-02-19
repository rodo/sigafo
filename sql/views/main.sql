--
--
--
DROP VIEW IF EXISTS v_amenagement_essences;

CREATE VIEW v_amenagement_essences AS
SELECT c.name as amenagement, b.name as essence,
    b.id as essence_id,
c.id as amenagement_id
FROM agrof_amenagement_essences AS a
INNER JOIN referentiel_amessence AS b ON b.id = a.amessence_id
INNER JOIN agrof_amenagement AS c ON c.id = a.amenagement_id
;
--
--
--
CREATE OR REPLACE VIEW dba_triggers AS
select relname,tgname,tgtype,tgconstrrelid
from pg_trigger,pg_class where pg_class.oid=pg_trigger.tgrelid order by tgname;
