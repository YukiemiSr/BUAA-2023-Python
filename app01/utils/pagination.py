"""
    自定义分页组件
"""
import copy

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, pagesize, page_param="page", plus=5):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.pagesize = pagesize
        self.start = (page - 1) * pagesize
        self.end = page * pagesize

        self.page_queryset = queryset[self.start:self.end]

        # 数据条数-> 页数
        total_cnt = queryset.count()
        page_cnt, div = divmod(total_cnt, pagesize)
        if div:
            page_cnt += 1
        self.total_page_cnt = page_cnt

        start_page = page - int(plus / 2) if page > int(plus / 2) else 1
        end_page = start_page + plus - 1
        if end_page > page_cnt:
            end_page = page_cnt
            start_page = end_page - (plus - 1) if end_page > plus - 1 else 1

        self.start_page = start_page
        self.end_page = end_page

    def html(self):
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])
        ele = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Previous"><span ' \
              'aria-hidden="true">&laquo;</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        for i in range(self.start_page, self.end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="page-item active"><a class="page-link " href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        self.query_dict.setlist(self.page_param, [self.total_page_cnt])
        ele = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Next"><span ' \
              'aria-hidden="true">&raquo;</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)
        page_string = mark_safe("".join(page_str_list))
        return page_string
