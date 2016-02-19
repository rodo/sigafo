--
--
-- Nom
-- Nature
-- Année de début
-- Mode de conduite
-- Projets
-- Lien Image
--

DROP VIEW IF EXISTS v_map_1_block;

CREATE VIEW v_map_1_block AS

SELECT id, json_build_object(
        'name', name,
        'start_year', date_debut,
        'projets', (SELECT ARRAY(select p.name FROM parc_block_projets bp, projet_projet p where p.id=bp.projet_id AND block_id=parc_block.id)),
        'natures', (SELECT ARRAY(select nb.name FROM referentiel_natureblock nb, parc_block_nature bn where bn.natureblock_id = nb.id AND bn.block_id=parc_block.id)),
        'mode_conduites', (SELECT ARRAY(select nb.name FROM referentiel_modeconduite nb, parc_block_conduites bn where bn.modeconduite_id = nb.id AND bn.block_id=parc_block.id))
        ) as map_public_info

FROM parc_block;

--
--
--
DROP VIEW IF EXISTS v_map_1_site;

CREATE VIEW v_map_1_site AS

SELECT id, json_build_object(
        'name', name,
        'commune', commune,
        'referent', (SELECT firstname || ' ' || lastname FROM contact_contact WHERE id = parc_site.referent_id)
        ) as map_public_info

FROM parc_site;

--
--
--
DROP VIEW IF EXISTS v_map_1_parcel;

CREATE VIEW v_map_1_parcel AS

SELECT id, json_build_object(
        'name', name,
        'surface', surface,
        'system', (SELECT name FROM referentiel_systemprod WHERE id = parc_parcel.systemprod_id),
        'center', center
        ) as map_public_info

FROM parc_parcel;
