
WITH points AS (
    SELECT pb.center
    FROM parc_block_projet pbp, parc_block pb
    WHERE projet_id IN
     (  
    SELECT projet_id FROM map_map_projets WHERE map_id = 1
    )

    AND pb.id = pbp.block_id
    AND pb.center IS NOT NULL
)

SELECT ST_Centroid(ST_Union(center)) FROM points;
