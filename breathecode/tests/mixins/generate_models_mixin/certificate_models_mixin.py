"""
Collections of mixins used to login in authorize microservice
"""
from breathecode.certificate.models import LayoutDesign, Specialty, UserSpecialty
from breathecode.tests.mixins.models_mixin import ModelsMixin
from mixer.backend.django import mixer

class CertificateModelsMixin(ModelsMixin):
    # TODO: Implement Badge
    user_specialty_token = '9e76a2ab3bd55454c384e0a5cdb5298d17285949'

    def get_specialty(self, id):
        return Specialty.objects.filter(id=id).first()

    def get_layout_design(self, id):
        return LayoutDesign.objects.filter(id=id).first()

    def get_user_specialty(self, id):
        return UserSpecialty.objects.filter(id=id).first()

    def get_specialty_dict(self, id):
        data = Specialty.objects.filter(id=id).first()
        return self.remove_dinamics_fields(data.__dict__.copy()) if data else None

    def get_layout_design_dict(self, id):
        data = LayoutDesign.objects.filter(id=id).first()
        return self.remove_dinamics_fields(data.__dict__.copy()) if data else None

    def get_user_specialty_dict(self, id):
        data = UserSpecialty.objects.filter(id=id).first()
        return self.remove_dinamics_fields(data.__dict__.copy()) if data else None

    def all_specialty_dict(self):
        return [self.remove_dinamics_fields(data.__dict__.copy()) for data in
            Specialty.objects.filter()]

    def all_layout_design_dict(self):
        return [self.remove_dinamics_fields(data.__dict__.copy()) for data in
            LayoutDesign.objects.filter()]

    def all_user_specialty_dict(self):
        return [self.remove_dinamics_fields(data.__dict__.copy()) for data in
            UserSpecialty.objects.filter()]

    def count_specialty(self):
        return Specialty.objects.count()

    def count_layout_design(self):
        return LayoutDesign.objects.count()

    def count_user_specialty(self):
        return UserSpecialty.objects.count()

    def generate_certificate_models(self, layout_design=False, specialty=False,
            certificate=False, user_specialty=False, layout_design_slug='',
            user_specialty_preview_url='', user_specialty_token='', models={},
            **kwargs):
        """Generate models"""
        self.maxDiff = None
        models = models.copy()

        if not 'layout_design' in models and layout_design:
            kargs = {
                'slug': 'default'
            }

            if layout_design_slug:
                kargs['slug'] = layout_design_slug

            models['layout_design'] = mixer.blend('certificate.LayoutDesign', **kargs)

        if not 'specialty' in models and specialty:
            kargs = {}

            if 'certificate' in models or certificate:
                kargs['certificate'] = models['certificate']
            
            models['specialty'] = mixer.blend('certificate.Specialty', **kargs)

        if not 'user_specialty' in models and user_specialty:
            kargs = {
                'token': self.user_specialty_token,
                'preview_url': 'https://asdasd.com',
            }

            if user_specialty_preview_url:
                kargs['preview_url'] = user_specialty_preview_url

            if user_specialty_token:
                kargs['token'] = user_specialty_token

            print(kargs)

            models['user_specialty'] = mixer.blend('certificate.UserSpecialty', **kargs)

        return models
