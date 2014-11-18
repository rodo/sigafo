explain
WITH projets AS (
    SELECT projet_id FROM map_map_projets
    WHERE map_id = 3
), parcels AS (
SELECT DISTINCT(parcel_id) FROM parc_block_projets, parc_block
WHERE parc_block_projets.block_id= parc_block.id
AND projet_id IN (SELECT projet_id FROM projets)
)
SELECT parcel_id FROM parcels;
