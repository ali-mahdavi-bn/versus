from abc import ABC

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities import Product


class AbstractProductRepository(AbstractRepository, ABC):
    def search_product(self, filter_clauses, category, language, values, values_int, limit, offset):
        return self._search_product(filter_clauses, category, language, values, values_int, limit, offset)

    def generate_histogram(self, attribute_id):
        return self._generate_histogram(attribute_id)

    def get_product(self, slug, language=2):
        return self._get_product(slug, language)

    def others_products(self):
        return self._others_products()

    def _search_product(self, filter_clauses, category, language, values, values_int, limit, offset):
        raise NotImplementedError

    def _get_product(self, slug, language=2):
        raise NotImplementedError

    def _others_products(self):
        raise NotImplementedError

    def _generate_histogram(self, attribute_id):
        raise NotImplementedError


class SqlalchemyProductRepository(AbstractProductRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Product

    def __check_selected_values(self, values, values_int):
        if values and values_int:
            combine = list(values) + list(values_int)
            return tuple(combine)
        elif values:
            return values
        elif values_int:
            return values_int
        else:
            return ()

    def _generate_histogram(self, attribute_id):
        histogram = self.orm.execute(
            """
           with min_max_avg as (SELECT ca.uuid           AS uuid,
                            MIN(pv.value_int) AS min,
                            MAX(pv.value_int) AS max,
                            AVG(pv.value_int) AS avg
                     FROM attributes ca
                              LEFT JOIN product_values pv ON pv.attribute_id = ca.uuid
                     where ca.uuid = :attribute_id
                     GROUP BY ca.uuid),
     fake_g2 as (select generate_series(min, max, (max - min) / 24) b2
                 from min_max_avg),
     fake_g as (select distinct width_bucket(b2, min, max * 1.1, 12) b1, min, max, (max * 1.1 - min) / 12 step_size
                from fake_g2,
                     min_max_avg),
--select * from fake_g;
     histogram as (select width_bucket(pv.value_int, min, max * 1.1, 12) as bucket,
                          (max * 1.1 - min) / 12                            step_size,
                          min,
                          count(*)                                       as freq
                   from product_values pv
                            right join min_max_avg ON pv.attribute_id = min_max_avg.uuid
                   where pv.attribute_id = :attribute_id
                     and min != max

                   group by bucket, min, step_size
                   order by bucket)

select b1,
       bucket,
       freq,
       f.b1 * f.step_size + f.min,
       (f.b1 + 1) * f.step_size + f.min,
       f.step_size
from histogram h
         right join fake_g f on f.b1 = h.bucket
            """, {
                'attribute_id': attribute_id,
            }
        ).fetchall()
        histogram = [{
            "bucket": bucket1,
            "freq": freq,
            "start_range": start_range,
            "end_range": end_range,
            "step_size": step_size,
        } for bucket1, bucket2, freq, start_range, end_range, step_size in histogram]
        return histogram

    def _search_product(self, filter_clauses, category, language, values, values_int, limit, offset):
        selected_value = self.__check_selected_values(values, values_int)
        products = self.orm.execute("""
       WITH ca AS (SELECT ca.uuid AS uuid, tc.name AS name
            FROM attributes ca
                     LEFT JOIN attributes_translate tc ON ca.uuid = tc.attribute_id and tc.language = :language
            WHERE ca.id = :category_attributes_id
            AND ca.category_id = :category_id),
     av_raw AS (SELECT tp.uuid                                        AS tpuuid,
                       tp.name                                        AS name,
                       p.id                                           AS product_id,
                       json_build_object('name', tct.name, 'show_name', tct.show_name, 'value',
                                         json_build_object('value', pvp.value, 'value_int', pvp.value_int, 'unit',
                                                           pvp.unit)) AS value
                FROM ca
                         LEFT JOIN product_values AS pv ON pv.attribute_id = ca.uuid AND
                                                           (pv.value IN :value OR pv.value_int IN :value_int)
                         LEFT JOIN products p ON p.uuid = pv.product_id
                         LEFT JOIN product_values AS pvp ON pvp.product_id = p.uuid
                         LEFT JOIN attributes cac ON pvp.attribute_id = cac.uuid
                         LEFT JOIN attributes_translate tct ON tct.attribute_id = cac.uuid and tct.language = :language
                         LEFT JOIN products_translate tp ON tp.product_id = p.uuid and tp.language = :language),
     av_ranked AS (SELECT *,
                          ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY name) AS rn
                   FROM av_raw)
SELECT json_build_object('name', name, 'product_id', product_id, 'values', json_agg(value))
FROM av_ranked
WHERE rn <= 3
GROUP BY name, product_id;
                    """, {
            "category_attributes_id": filter_clauses,
            "category_id": category,
            "value_selected": selected_value,
            "attribute_id": filter_clauses,
            "value": values,
            "value_int": values_int,
            "limit": limit,
            "language": language,
            "offset": offset,
        }).fetchall()

        products = [i[0] for i in products]
        return products

    def _get_product(self, slug, language=2):
        product = self.orm.execute("""
select json_build_object(
               'id', p.id,
               'name', p.slug,
               'attributes', json_agg(
                       json_build_object(
                               'id', pv.id,
                               'ca', ca.uuid,
                               'name', tc.name,
                               -- 'type', ca.type,
                               'value', pv.value,
                               'value_int', pv.value_int,
                               'unit', pv.unit
                       )
                      )
       )
from product_values pv
         join products p on p.slug=:product_slug and p.uuid = pv.product_id
         join attributes_translate tc on tc.attribute_id = pv.attribute_id and tc.language=:language
         join attributes ca on ca.uuid=pv.attribute_id
group by p.slug, p.id""", {
            "product_slug": slug,
            "language": language

        }).fetchall()
        print(slug)
        print(product)
        return product[0][0] if product else None

    def _others_products(self):
        products = self.orm.execute("""
                    SELECT json_build_object(
               'name', sub.name,
               'description', sub.description,
               'att', json_agg(
                       json_build_object(
                               'name', sub.tc_name,
                               'show_name', sub.show_name,
                               'description', sub.tc_description,
                               'value', sub.value,
                               'value_int', sub.value_int,
                               'group', sub.ga_name
                       )
                      )
       )
FROM (SELECT p.uuid,
             tp.name,
             tp.description,
             pv.value,
             pv.value_int,
             ca.uuid                                                  AS ca_uuid,
             tc.name                                                  AS tc_name,
             tc.show_name,
             tc.description                                           AS tc_description,
             ga.name                                                  AS ga_name,
             ROW_NUMBER() OVER (PARTITION BY p.uuid ORDER BY ca.uuid) AS rn
      FROM products p
               JOIN products_translate tp ON tp.product_id = p.uuid
               JOIN product_values pv ON pv.product_id = p.uuid
               JOIN attributes ca ON ca.uuid = pv.attribute_id
               JOIN group_attributes ga ON ga.uuid = ca.group_attribute_id
               JOIN attributes_translate tc ON tc.attribute_id = ca.uuid) AS sub
WHERE rn <= 3
GROUP BY sub.uuid, sub.name, sub.description
LIMIT 10;""").fetchall()
        return products[0][0] if products else None
