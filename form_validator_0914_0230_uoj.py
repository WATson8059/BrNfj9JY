# 代码生成时间: 2025-09-14 02:30:40
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.renderers import render_to_response
from pyramid.response import Response
from colander import MappingSchema, SchemaNode, String, Invalid
# 增强安全性
from deform import Form, ValidationFailure


# 定义表单数据验证器
class MyFormSchema(MappingSchema):
    first_name = SchemaNode(String(),
                         missing=None,
                         validator=String().not_empty(),
                         description="First Name")
    last_name = SchemaNode(String(),
                        missing=None,
                        validator=String().not_empty(),
                        description="Last Name")
    email = SchemaNode(String(),
                      missing=None,
                      validator=String().email(),
                      description="Email Address")


# Pyramid视图函数，处理表单提交
@view_config(route_name='submit_form', renderer='json')
def handle_form_submission(request):
    """处理表单提交。

    :param request: Pyramid的当前请求对象。
    :return: 表单提交结果的JSON响应。
    """
    try:
# 改进用户体验
        # 从请求中获取表单数据
        form_data = request.json_body
        
        # 验证表单数据
        validated_data = MyFormSchema().deserialize(form_data)
# FIXME: 处理边界情况
        
        # 返回验证通过的数据
        return {'success': True, 'data': validated_data}
    
    except ValidationFailure as e:
        # 处理验证失败的情况
# NOTE: 重要实现细节
        return {'success': False, 'errors': e.asdict()}
    
    except Exception as e:
        # 处理其他异常情况
        request.response.status_code = 400
        return {'success': False, 'message': str(e)}


def includeme(config):
    # 配置路由
    config.add_route('submit_form', '/submit_form')
    # 添加视图
    config.scan()
