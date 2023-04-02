CREATE VIEW all_flats_last_price AS
    SELECT flats.flat_id, flats.address, flats.floor, flats.rooms, flats.area, flats.finishing, flats.settlement_date, flats.url_suffix,
        projects.project_id, projects.name, projects.city, projects.url,
        prices.price, prices.booking_status
    FROM flats
    INNER JOIN projects ON flats.project_id = projects.project_id
    INNER JOIN prices ON prices.flat_id = flats.flat_id
    INNER JOIN (
        SELECT flat_id, max(data_created) AS max_data
        FROM prices
        GROUP BY flat_id
    ) AS last_price ON last_price.flat_id = prices.flat_id
    WHERE prices.data_created = last_price.max_data;
