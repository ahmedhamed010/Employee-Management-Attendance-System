from rest_framework.pagination import PageNumberPagination


class EmployeePagination(PageNumberPagination):
    page_size              = 10
    page_size_query_param  = 'page_size'   # ← المستخدم يقدر يغير العدد
    max_page_size          = 100