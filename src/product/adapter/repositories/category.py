from abc import ABC

from sqlalchemy import text

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities import Category


class AbstractCategoryRepository(AbstractRepository, ABC):
    def get_all_category(self):
        return self._get_all_category()

    def _get_all_category(self):
        raise NotImplementedError

    def get_attributes_category(self, id, attribute_id):
        return self._get_attributes_category(id, attribute_id)

    def _get_attributes_category(self, id, attribute_id):
        raise NotImplementedError


class SqlalchemyCategoryRepository(AbstractCategoryRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Category

    def _get_all_category(self):
        categories = self.session.execute(text("""
        select json_build_object(
    'id', c.id,
    'name', c.name,
    'childs', json_agg(
             json_build_object(
             'id',ca.id,
             'name',ca.name
             )
             ))
from categories c
left join categories ca on ca.subset = c.uuid
where c.subset is null
group by c.id;
        """)).fetchall()
        categories = [i[0] for i in categories]
        return categories or None

    def _get_attributes_category(self, id, attribute_id):
        category_attribute = self.session.execute(text(f"""
WITH distencted_attr AS (SELECT DISTINCT ON (ca.id::text || pv.value::text) ca.id,
                                                                            pv.value,
                                                                            pv.unit
                         FROM attributes ca
                                  JOIN products_value pv ON ca.uuid = pv.attribute_id
                         WHERE pv.value IS NOT NULL
                           AND ca.category_id = :category_id),
     distencted_attr_int AS (SELECT DISTINCT ON (ca.id::text || pv.value_int::text) ca.id,
                                                                                    pv.value_int,
                                                                                    pv.unit
                             FROM attributes ca
                                      JOIN products_value pv ON ca.uuid = pv.attribute_id
                             WHERE pv.value_int IS NOT NULL
                               AND ca.category_id = :category_id),

     values as (SELECT id,
                       json_agg(
                               json_build_object(
                                       'value', value,
                                       'unit', unit
                               )
                       ) AS value
                FROM (SELECT id, value, unit
                      FROM distencted_attr
                      UNION
                      SELECT id, value_int::varchar AS value, unit AS unit
                      FROM distencted_attr_int) AS combined_data
                GROUP BY id)
select json_build_object(
               'group_name', ga.name,
               'att', json_agg(
                       json_build_object(
                               'show_name', tc.show_name,
                               'att_id', ca.id,
                               'selected', ca.id in :attribute_id,
                               'type', ca.type,
                               'values', (select v.value

                                          from values v
                                          where v.id = ca.id)
                       )
                      )
       )
from categories c
         join attributes ca on ca.category_id = c.uuid
         join group_attributes ga on ga.uuid = ca.group_attribute_id
         join attributes_translate tc on tc.attribute_id = ca.uuid
group by ga.name;
        """), {
            'category_id': id,
            # 'category_id': '49a53f0d-2ad4-41b5-9bba-6c5d2476c0f0',
            'attribute_id': attribute_id,
        }).fetchall()

        category_attribute = [i[0] for i in category_attribute]
        return category_attribute

# """
# select json_build_object(
#                'group_name', ga.name,
#                'att', json_agg(
#                        json_build_object(
#                                'show_name', tc.show_name,
#                                 'att_id', ca.id,
#                                 'selected', ca.id in :attribute_id,
#                                'type', ca.type,
#                                'values', (select json_agg(
#                                                       json_build_object(
#                                                       'value',pv.value,
#                                                       'value_int',pv.value_int,
#                                                       'unit',pv.unit
#                                                       )
#
#                                               )
#                                        from product_values pv
#                                        where pv.category_attribute_id=ca.uuid
#
#                                        )
#                        )
#                       )
#        )
# from categories c
#          join category_attributes ca on ca.category_id = c.uuid
#          join group_attributes ga on ga.uuid = ca.group_attribute_id
#          join translate_categories tc on tc.category_attribute_id = ca.uuid
# {"where c.id=:category_id" if id else ''}
# group by ga.name;
#         """
