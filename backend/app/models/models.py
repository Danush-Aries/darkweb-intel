from tortoise import fields, models

class Keyword(models.Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "keywords"

class IntelReport(models.Model):
    id = fields.IntField(pk=True)
    keyword = fields.CharField(max_length=255, index=True)
    url = fields.CharField(max_length=500, index=True)
    content = fields.TextField()
    threat_score = fields.FloatField(default=0.0, index=True)
    ai_summary = fields.TextField(null=True)
    status = fields.CharField(max_length=50, default="pending", index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)

    # DB Optimization: Add a composite index for common query patterns (status + threat_score)
    class Meta:
        table = "intel_reports"
        # Note: Tortoise ORM doesn't support composite indexes via Meta.
        # In a production Postgres/MySQL setup, we would add a manual migration.
