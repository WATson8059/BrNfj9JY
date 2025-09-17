# 代码生成时间: 2025-09-18 02:11:34
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest
from colander import Mapping, Schema, String, Invalid
from deform import Form, Button, ValidationFailure


# 数据验证器类
class MyFormSchema(Schema):
    """定义表单的数据验证规则"""
    name = String()
    email = String()
    age = String()

    def validate_name(self, node, value):
        """验证名字是否合法"""
        if not value:
            raise Invalid(node, 'Name is required.')
        if len(value) < 2:
            raise Invalid(node, 'Name must be at least 2 characters long.')

    def validate_email(self, node, value):
        """验证邮箱是否合法"""
        if not value:
            raise Invalid(node, 'Email is required.')
        if '@' not in value:
            raise Invalid(node, 'Invalid email address.')

    def validate_age(self, node, value):
        """验证年龄是否合法"""
        if not value:
            raise Invalid(node, 'Age is required.')
        try:
            int(value)
        except ValueError:
            raise Invalid(node, 'Age must be a digit.')


# Pyramid视图函数，用于处理表单提交
@view_config(route_name='form', request_method='POST', renderer='json')
def handle_form(request):
    """处理表单提交"""
    try:
        # 创建表单实例
        form = Form(MyFormSchema(), buttons=(Button.name,))
        # 解析表单数据
        controls = request.POST.items()
        appstruct = form.validate(controls)
        # 验证成功，返回成功消息
        return {'status': 'success', 'data': appstruct}
    except ValidationFailure as e:
        # 验证失败，返回错误信息
        return {'status': 'error', 'error_messages': e.asdict()}
    except Exception as e:
        # 处理其他异常
        return {'status': 'error', 'error_messages': str(e)}


# Pyramid视图函数，用于展示表单
@view_config(route_name='form', renderer='templates/form.pt')
def show_form(request):
    """展示表单"""
    return {}