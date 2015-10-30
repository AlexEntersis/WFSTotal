__author__ = 'Alex'

from haystack import indexes
from basic_parser.models import Profile, Skills


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField()
    skills = indexes.MultiValueField(indexed=True, stored=True)

    def prepare_skills(self, obj):
        return [skills.id for skills in obj.skills.all()]

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


