from rest_framework.renderers import BaseRenderer


class PassthroughRenderer(BaseRenderer):
    '''Custom renderer. Returns data as it is. Could be applied for custom get operations on server'''
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data