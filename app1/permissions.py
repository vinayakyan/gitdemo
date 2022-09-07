from django.http import HttpResponseForbidden


class IsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.created_by == self.request.user:
            print("hello")
            return HttpResponseForbidden()
        return super(IsOwnerMixin, self).dispatch(request, *args, **kwargs)
