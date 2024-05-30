import json

from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.db.models import Q, F
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config.settings import GOOGLE_MAPS_KEY
from education_content.forms import ChapterForm, MaterialForm, MaterialUpdateForm, \
    MaterialPhotosForm
from education_content.models import Chapter, Material, MaterialPhotos
from education_content.templatetags.my_tags import mediapath_filter
from tests.models import Test
from unique_content.models import FigureFromP3din, FigureThinSection, Figure360View, LinkSpotCoordinates, \
    InfoSpotForPanorama, InfoSpotCoordinates
from users.services import update_last_activity


class LoginRequiredWithChoiceMixin(AccessMixin):
    """
    Mixin change LoginRequiredMixin functionality according to 'is_login_required'
    field in the model
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if login_required. If yes, apply LoginRequiredMixin functionality
        if self.get_object().is_login_required:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)


class GetPublicationStatusOrOwnerOrStaffMixin:
    """
        Mixin to control if user owner or Staff
    """

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published:
            raise PermissionDenied("Your material has been published. You must request unposting in order to edit it.")
        elif self.object.owner != self.request.user and self.request.user.is_staff is not True:
            raise PermissionDenied("You are not the author of this material. Editing is not possible for you.")
        return self.object


class GetLastUpdateMixin:
    """
    Mixin to update the "last_update" attribute
    """

    def form_valid(self, form):
        self.object = form.save()
        self.object.last_update = timezone.now()
        self.object.save()

        return super().form_valid(form)


class GetFinalConditionsMixin:
    """
    Mixin adding method filtering formset based on publication and belonging to an authenticated user
    """

    def get_final_conditions(self):
        # Make Q-objects for filtering
        published_condition = Q(is_published=True)
        owner_condition = Q(owner=self.request.user)
        # Combine them
        return published_condition | owner_condition


class GetChapterListMixin:
    """
    Add chapter list to context
    """

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        chapter_list = Chapter.objects.all().filter(is_published=True)
        context_data['chapter_list'] = chapter_list
        return context_data


class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    success_url = reverse_lazy('education_content:chapter_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ChapterUpdateView(LoginRequiredMixin, GetLastUpdateMixin, GetPublicationStatusOrOwnerOrStaffMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm

    def get_success_url(self):
        return reverse('education_content:chapter_view', args=[self.kwargs.get('pk')])


class ChapterListView(LoginRequiredMixin, GetFinalConditionsMixin, ListView):
    model = Chapter

    def get_queryset(self, *args, **kwargs):
        update_last_activity(self.request.user)
        queryset = super().get_queryset(*args, **kwargs)
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(self.get_final_conditions())
        return queryset


class ChapterDetailView(LoginRequiredMixin, GetFinalConditionsMixin, DetailView):
    model = Chapter

    def get_queryset(self, *args, **kwargs):
        update_last_activity(self.request.user)
        return super().get_queryset(*args, **kwargs).select_related('owner')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Increment the views count when viewing a Chapter
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_list = self.object.material_set.all().select_related('owner')
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            material_list = material_list.filter(self.get_final_conditions())
        material_list = material_list.order_by('pk')
        context_data['material_list'] = material_list
        return context_data


class ChapterDeleteView(LoginRequiredMixin, DeleteView):
    model = Chapter
    success_url = reverse_lazy(
        'education_content:chapter_list')  # Redirect to the list of Chapters after deleting a Chapter


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def change_published_status(request, model: str, pk: int):
    """
    Change publication or publication request status
    """
    got_model = apps.get_model('education_content', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    current_value = getattr(got_object, 'is_published')
    new_value = not current_value
    setattr(got_object, 'is_published', new_value)
    got_object.is_published_requested = False
    got_object.save()
    return redirect(reverse(f'education_content:{model.lower()}_view', kwargs={'pk': pk}))


@login_required
def change_published_requested_status(request, model: str, pk: int):
    """
    Change publication request status
    """
    got_model = apps.get_model('education_content', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    if not (got_object.owner == request.user or request.user.is_staff):
        raise Http404("Access denied")

    current_value = getattr(got_object, 'is_published_requested')
    new_value = not current_value
    setattr(got_object, 'is_published_requested', new_value)
    got_object.save()
    return redirect(reverse(f'education_content:{model.lower()}_view', kwargs={'pk': pk}))


class MaterialCreateView(LoginRequiredMixin, GetChapterListMixin, CreateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy('education_content:material_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MaterialCreateChapterView(LoginRequiredMixin, GetChapterListMixin, CreateView):
    model = Material
    form_class = MaterialForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['chapter_pk'] = self.kwargs['chapter_pk']
        return context_data

    def get_success_url(self):
        # We dynamically construct the URL using reverse_lazy and the value of chapter_pk
        chapter_pk = self.kwargs['chapter_pk']
        return reverse_lazy('education_content:chapter_view', kwargs={'pk': chapter_pk})


class MaterialUpdateView(LoginRequiredMixin, GetLastUpdateMixin, GetPublicationStatusOrOwnerOrStaffMixin, UpdateView):
    model = Material
    form_class = MaterialUpdateForm

    def get_success_url(self):
        return reverse('education_content:material_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_photos_list = self.object.materialphotos_set.all().select_related('thin_section', 'p3din_model', 'pano_view' )
        material_photos_list = material_photos_list.order_by('pk')
        context_data['material_photos_list'] = material_photos_list
        return context_data


class MaterialListView(LoginRequiredMixin, GetFinalConditionsMixin, ListView):
    model = Material

    def get_queryset(self, *args, **kwargs):
        update_last_activity(self.request.user)
        queryset = super().get_queryset(*args, **kwargs).select_related('owner', 'chapter')
        queryset = queryset.order_by('pk')
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(self.get_final_conditions())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['material_list'] = context_data['object_list']
        return context_data


class MaterialDetailView(LoginRequiredWithChoiceMixin, GetFinalConditionsMixin, DetailView):
    model = Material

    def get_queryset(self, *args, **kwargs):
        update_last_activity(self.request.user)
        return super().get_queryset(*args, **kwargs).select_related('owner')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Increment the views count when viewing a Material
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_photos_list = self.object.materialphotos_set.all().select_related('thin_section', 'p3din_model', 'pano_view')
        material_photos_list = material_photos_list.order_by('pk')
        context_data['material_photos_list'] = material_photos_list
        material_photos_list_json = serialize('json', material_photos_list)
        context_data['material_photos_list_json'] = material_photos_list_json
        pano_view_pks = [material_photo.pano_view.pk for material_photo in material_photos_list if material_photo.pano_view]
        pano_view_queryset = Figure360View.objects.filter(pk__in=pano_view_pks)
        pano_view_queryset_new = pano_view_queryset.values('pk', 'title', 'view', 'latitude', 'longitude', 'height', 'pano_type')
        pano_view_list = list(pano_view_queryset_new)
        # Edit view field to make it URL
        for item in pano_view_list:
            item['view'] = mediapath_filter(item['view'])
        pano_view_dict = {view['pk']: view for view in pano_view_list}
        context_data['pano_view_dict'] = json.dumps(pano_view_dict)
        link_spot_coordinates_list = list(LinkSpotCoordinates.objects.filter(panorama_to__in=pano_view_queryset).values())
        context_data['link_spot_coordinates_list'] = json.dumps(link_spot_coordinates_list)
        pano_view_ids = [pano_view['pk'] for pano_view in pano_view_list]
        info_spot_queryset = InfoSpotForPanorama.objects.all().annotate(
            figure_thin_section_preview=F('figure_thin_section__preview'),
            figure_3d_link_for_iframe=F('figure_3d__link_for_iframe'))
        info_spot_queryset_filtered = (info_spot_queryset.filter(
            Q(infospotcoordinates__panorama_id__in=pano_view_ids)))
        info_spot_list = list(info_spot_queryset_filtered.values())
        info_spot_dict = {view['id']: view for view in info_spot_list}
        info_spot_coordinates_list = list(InfoSpotCoordinates.objects.filter(info_spot__in=info_spot_queryset_filtered).values())
        context_data['info_spot_dict'] = json.dumps(info_spot_dict)
        context_data['info_spot_coordinates_list'] = json.dumps(info_spot_coordinates_list)


        try:
            context_data['test'] = Test.objects.get(material=self.object.pk)
        except Test.DoesNotExist:
            context_data['test'] = None

        return context_data


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material

    def get_success_url(self):
        chapter_pk = self.object.chapter.pk
        return reverse_lazy('education_content:chapter_view', kwargs={'pk': chapter_pk})


class MaterialPhotosCreateMaterialView(LoginRequiredMixin, CreateView):
    model = MaterialPhotos
    form_class = MaterialPhotosForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['material_pk'] = self.kwargs['material_pk']
        p3din_model_list = FigureFromP3din.objects.all()
        context_data['p3din_model_list'] = p3din_model_list
        thin_section_list = FigureThinSection.objects.all()
        context_data['thin_section_list'] = thin_section_list
        pano_view_list = Figure360View.objects.all()
        context_data['pano_view_list'] = pano_view_list
        return context_data

    def get_success_url(self):
        # We dynamically construct the URL using reverse_lazy and the value of chapter_pk
        material_pk = self.kwargs['material_pk']
        return reverse_lazy('education_content:material_edit', kwargs={'pk': material_pk})


class MaterialPhotosCreateView(LoginRequiredMixin, CreateView):
    model = MaterialPhotos
    form_class = MaterialPhotosForm
    success_url = reverse_lazy('education_content:materialphotos_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_list = Material.objects.all()
        context_data['material_list'] = material_list
        p3din_model_list = FigureFromP3din.objects.all()
        context_data['p3din_model_list'] = p3din_model_list
        thin_section_list = FigureThinSection.objects.all()
        context_data['thin_section_list'] = thin_section_list
        pano_view_list = Figure360View.objects.all()
        context_data['pano_view_list'] = pano_view_list
        return context_data


class MaterialPhotosListView(LoginRequiredMixin, GetFinalConditionsMixin, ListView):
    model = MaterialPhotos

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['material_photos_list'] = MaterialPhotos.objects.all()
        return context_data


class MaterialPhotosDetailView(LoginRequiredMixin, DetailView):
    model = MaterialPhotos


class MaterialPhotosDeleteView(LoginRequiredMixin, DeleteView):
    model = MaterialPhotos

    def get_success_url(self):
        material_pk = self.object.material.pk
        return reverse_lazy('education_content:material_edit', kwargs={'pk': material_pk})
