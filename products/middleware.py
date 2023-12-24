class StoreIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy địa chỉ IP từ request
        ip_address = request.META.get('REMOTE_ADDR', '')

        # Lưu địa chỉ IP vào session
        request.session['user_ip'] = ip_address

        response = self.get_response(request)
        return response