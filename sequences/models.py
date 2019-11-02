import re

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sequence(models.Model):

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100,
        primary_key=True,
    )

    last = models.PositiveIntegerField(
        verbose_name=_("last value"),
    )

    class Meta:
        verbose_name = _("sequence")
        verbose_name_plural = _("sequences")

    def __str__(self):
        return "Sequence(name={}, last={})".format(
            repr(self.name), repr(self.last))


def prepare_query(query):
    query = query.format(db_table=Sequence._meta.db_table)
    return re.sub(r'\s+', ' ', query).strip()


SELECT = prepare_query("""
             SELECT last
               FROM {db_table}
              WHERE name = %s
""")

POSTGRESQL_UPSERT = prepare_query("""
        INSERT INTO {db_table} (name, last)
             VALUES (%s, %s)
        ON CONFLICT (name)
      DO UPDATE SET last = {db_table}.last + 1
          RETURNING last
""")

MYSQL_UPSERT = prepare_query("""
        INSERT INTO {db_table} (name, last)
             VALUES (%s, %s)
   ON DUPLICATE KEY
             UPDATE last = {db_table}.last + 1
""")
