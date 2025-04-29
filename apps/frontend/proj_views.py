from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.referee_records_makegeojson import update_ref_info


class RefereeRecordsView(UserPassesTestMixin, TemplateView):
    template_name = 'projects/referee_records/index.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('http://wangjiayu.com/blog/')


@csrf_exempt
def update_ref_data(request):
    if request.method == 'POST':
        try:
            update_ref_info()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
