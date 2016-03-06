
--
-- Amenagement
--
DROP VIEW IF EXISTS v_map_2_site;
DROP VIEW IF EXISTS v_map_2_parcel;
DROP VIEW IF EXISTS v_map_2_block;
DROP VIEW IF EXISTS v_map_2_amenagement;

CREATE VIEW v_map_2_amenagement AS

SELECT id, block_id, json_build_object(
        'nature', (SELECT name FROM referentiel_natureblock WHERE id=nature_id),
        'density', density,
        'dist_inter_line', dist_inter_line,
        'essences', (SELECT ARRAY(
            SELECT e.name
            FROM referentiel_amessence e, agrof_amenagement_essences aae
            WHERE aae.amenagement_id=agrof_amenagement.id
                AND aae.amessence_id=e.id))
        )::jsonb as map_public_info

FROM agrof_amenagement;

--
--
-- Nom
-- Nature
-- Année de début
-- Mode de conduite
-- Projets
-- Lien Image
--
CREATE VIEW v_map_2_block AS

SELECT id, parcel_id, json_build_object(
        'name', name,
        'uuid', uuid,
        'start_year', year_start,
        'projets', (SELECT ARRAY(
            SELECT p.name
            FROM parc_block_projets bp, projet_projet p
            WHERE p.id=bp.projet_id
                AND block_id=parc_block.id)),
        'natures', (SELECT ARRAY(
            select nb.name
            FROM referentiel_natureblock nb, parc_block_nature bn
            WHERE bn.natureblock_id = nb.id
                AND bn.block_id=parc_block.id)),
        'mode_conduites', (SELECT ARRAY(
            SELECT nb.name
            FROM referentiel_modeconduite nb, parc_block_conduites bn
            WHERE bn.modeconduite_id = nb.id
                AND bn.block_id=parc_block.id)),
        'image_url', map_public_info->'image_url',
        'amenagements', (SELECT ARRAY(
            SELECT v_map_2_amenagement.map_public_info
            FROM v_map_2_amenagement, parc_block
            WHERE parc_block.parcel_id = parcel_id
                AND v_map_2_amenagement.block_id= parc_block.id
                )
            )
        )::jsonb AS map_public_info

FROM parc_block
WHERE map_ids @> ARRAY[2];

--
-- Parcelle
--
CREATE VIEW v_map_2_parcel AS

SELECT id, json_build_object(
        'name', name,
        'surface', surface,
        'system', (SELECT name
        FROM referentiel_systemprod
        WHERE id = parc_parcel.systemprod_id),
        'center', center,
        'icon_url', icon_url,
        'blocks', (SELECT ARRAY(
            SELECT map_public_info
            FROM v_map_2_block
            WHERE v_map_2_block.parcel_id = parc_parcel.id)
            )
        ) as map_public_info

FROM parc_parcel;

--
-- Site
--
CREATE VIEW v_map_2_site AS

SELECT id, json_build_object(
        'name', name,
        'commune', commune,
        'referent', (
        SELECT firstname || ' ' || lastname
        FROM contact_contact
        WHERE id = parc_site.referent_id)
        ) as map_public_info

FROM parc_site;


