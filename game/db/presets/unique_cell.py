from game.db.presets.base import UniqueCell

ice_portal = UniqueCell(slug='portal', properties={
    'teleportation_data' : {
        'region_id' : 2,
        'x' : 0,
        'y' : 0,
}})
forest_portal = UniqueCell(slug='portal', properties={
    'teleportation_data' : {
        'region_id' : 1,
        'x' : 0,
        'y' : 0,
}})

unique_cells = {'ice_portal' : ice_portal, 'forest_portal' : forest_portal}
