from unit_of_work import UnitOfWork


# @cache(ttl=49)
def min_max_avg_value_product(language_id):
    with UnitOfWork() as uow:
        query = """
           WITH numeric_attributes AS (SELECT tc.name           AS name,
                                   ca.uuid           AS attribute_uuid,
                                   MIN(pv.value_int) AS min_value,
                                   MAX(pv.value_int) AS max_value,
                                   AVG(pv.value_int) AS avg_value
                            FROM attributes ca
                                     LEFT JOIN product_values pv ON pv.attribute_id = ca.uuid
                                     LEFT JOIN attributes_translate tc
                                               ON tc.attribute_id = pv.attribute_id AND tc.language = :language_id

                            WHERE pv.value_int IS NOT NULL
                            GROUP BY ca.uuid, tc.name),

     numeric_attributes_with_float AS (SELECT tc.name               AS name,
                                              ca.uuid               AS attribute_uuid,
                                              MIN(pv.value::float4) AS min_value,
                                              MAX(pv.value::float4) AS max_value,
                                              AVG(pv.value::float4) AS avg_value
                                       FROM attributes ca
                                                LEFT JOIN product_values pv ON pv.attribute_id = ca.uuid
                                                LEFT JOIN attributes_translate tc
                                                          ON tc.attribute_id = pv.attribute_id AND tc.language = :language_id

                                       WHERE pv.value ~ '^[0-9]+(\.[0-9]+)?$' -- This line checks if pv.value is numeric
                                       GROUP BY ca.uuid, tc.name),

     combined_numeric_attributes AS (SELECT *
                                     FROM numeric_attributes
                                     UNION ALL
                                     SELECT *
                                     FROM numeric_attributes_with_float)

SELECT *
FROM combined_numeric_attributes
        """
        products_attribute_values = uow.product.orm.execute(query, {"language_id": language_id}).fetchall()

    products_attribute_values_dict = {}

    for product_attribute_value in products_attribute_values:
        name = product_attribute_value[0]
        if name in products_attribute_values_dict:
            continue
        products_attribute_values_dict[name] = {
            "min": product_attribute_value[2],
            "max": product_attribute_value[3],
            "avg": product_attribute_value[4]
        }

    return products_attribute_values_dict
