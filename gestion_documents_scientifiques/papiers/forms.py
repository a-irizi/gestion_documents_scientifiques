from django import forms
from . import models


class PublicationRevueInternationalForm(forms.ModelForm):
    class Meta:
        model = models.PublicationRevueInternational
        fields = ['papier', 'titre', 'indexation', 'anneePublication',
                  'nomJournal', 'numeroJournal', 'volumeJournal', 'pageDébut', 'pageFin', ]

    def save(self, commit=True):
        pub = super().save(commit = False)
        pub.papierType = models.Papier.PapierType.PUBLICATION_REVUE_INTERNATIONAL
        if commit:
            pub.save()
        return pub