from django.views.generic import TemplateView
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

from front.webcam import VideoCamera, gen


@gzip.gzip_page
def webcam_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        return context


class Login(TemplateView):
    template_name = 'login.html'

class Playing(TemplateView):
    template_name = 'playing.html'
