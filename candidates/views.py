from django.db.models import Q, F, Sum, Count, Case, When, Value, IntegerField
from django.db.models.functions import Length

from .models import Candidate
from .serializers import CandidateSerializer, CandidateUpdateSerializer, CandidateSearchSerializer

from rest_framework import generics
from functools import reduce


class CandidateCreateView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class CandidateUpdateView(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateUpdateSerializer
    lookup_field = 'id'

class CandidateSearchView(generics.ListAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        queryset = Candidate.objects.all()
        search_params = CandidateSearchSerializer(data=self.request.query_params)
        
        # return an empty queryset if the search parameters are invalid
        if not search_params.is_valid():
            return queryset.none()

        data = search_params.validated_data
        filters = {}

        # filtering conditions based on the validated data
        if data.get('min_salary') is not None:
            filters['current_salary__gte'] = data['min_salary']
        if data.get('max_salary') is not None:
            filters['current_salary__lte'] = data['max_salary']
        if data.get('min_age') is not None:
            filters['age__gte'] = data['min_age']
        if data.get('max_age') is not None:
            filters['age__lte'] = data['max_age']
        if data.get('min_exp') is not None:
            filters['years_of_exp__gte'] = data['min_exp']
        if data.get('phone_number'):
            filters['phone_number__icontains'] = data['phone_number']
        if data.get('email'):
            filters['email__icontains'] = data['email']
        if data.get('name'):
            filters['name__icontains'] = data['name']

        return queryset.filter(**filters)


class CandidateNameSearchView(generics.ListAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return Candidate.objects.none()

        query_words = query.split()
        queryset = Candidate.objects.annotate(
            relevance=Case(
                # exact match gets highest relevance
                When(name__iexact=query, then=Value(3)),
                # partial match with all words gets higher relevance
                When(reduce(lambda x, y: x & y, [Q(name__icontains=word) for word in query_words]), then=Value(2)),
                # partial match with some words gets lower relevance
                When(reduce(lambda x, y: x | y, [Q(name__icontains=word) for word in query_words]), then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).filter(relevance__gt=0).order_by('-relevance', 'name')

        return queryset