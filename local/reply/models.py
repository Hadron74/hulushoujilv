from django.db import models


class Reply(models.Model):
    """ Reply main class
    """
    id = models.BigIntegerField(primary_key=True)
    ip = models.CharField(max_length=50)
    nc = models.CharField(max_length=50)
    ti = models.DateTimeField()
    te = models.TextField()
    ud = models.BigIntegerField()


class Link(models.Model):
    """ Reply link
    """
    reply = models.ForeignKey(Reply, primary_key=True)
    root_id = models.BigIntegerField()


class CategoryName(models.Model):
    """Category Name"""
    category = models.CharField(max_length=255)


class Category(models.Model):
    """ Reply Category
    """
    reply = models.ForeignKey(Reply, primary_key=True)
    category_id = models.BigIntegerField()


class KeywordName(models.Model):
    """Keyword Name
    """
    keyword = models.CharField(max_length=255)


class Keyword(models.Model):
    """ Reply keywords
    """
    reply = models.ForeignKey(Reply, primary_key=True)
    keyword_id = models.BigIntegerField()
